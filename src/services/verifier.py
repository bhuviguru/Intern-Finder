from playwright.async_api import async_playwright
from src.scrapers.internshala_scraper import InternshalaScraper
from src.utils.logger import setup_logger

logger = setup_logger()

async def verify_top_jobs(jobs_to_verify, top_n=10):
    """
    Verifies eligibility for the top jobs.
    Returns a list of eligible jobs.
    """
    eligible_jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        internshala = InternshalaScraper(browser)
        # Other verification scrapers can be added here if needed
        
        for job in jobs_to_verify:
            if len(eligible_jobs) >= top_n:
                break
                
            if job.site == "Internshala":
                is_eligible, reason = await internshala.verify_eligibility(job.link)
                if is_eligible:
                    eligible_jobs.append(job)
                else:
                    logger.warning(f"Skipping ineligible job: {job.role} ({reason})")
            else:
                # Assume other sites are valid or implement their own verification
                eligible_jobs.append(job)
        
        await browser.close()
    return eligible_jobs
