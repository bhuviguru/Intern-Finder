from .base_scraper import BaseScraper
from src.utils.date_parser import parse_posted_date, is_recent
from datetime import datetime
import time

class InternshalaScraper(BaseScraper):
    def __init__(self, browser_instance=None):
        super().__init__(browser_instance)
        self.base_url = "https://internshala.com/internships"

    async def scrape(self, keywords):
        jobs = []
        if not self.browser:
            self.logger.error("Browser instance not set")
            return jobs

        page = await self.browser.new_page()
        
        try:
            # Construct search URL (simple version, can be enhanced with filters)
            # Internshala URL structure: /internships/keywords-internship
            # For multiple keywords, it's tricky, so we might need multiple passes or broad search
            
            # Let's try to search for the first keyword or construct a search query
            # For simplicity, we loop through keywords or join them if supported. 
            # Internshala supports format: https://internshala.com/internships/<keyword>-internship
            
            for keyword in keywords:
                search_term = keyword.lower().replace(" ", "-")
                url = f"{self.base_url}/{search_term}-internship"
                self.logger.info(f"Scraping {url}")
                
                await page.goto(url, timeout=60000)
                await page.wait_for_load_state("networkidle")
                
                # Check for popup and close if necessary
                try:
                     await page.click(".login-modal .close_action", timeout=2000)
                except:
                    pass

                job_cards = await page.query_selector_all(".individual_internship")
                
                for card in job_cards:
                    try:
                        role_elem = await card.query_selector(".job-title-href")
                        company_elem = await card.query_selector(".company-name")
                        location_elem = await card.query_selector(".locations")
                        stipend_elem = await card.query_selector(".stipend_container .stipend")
                        link_elem = await card.query_selector(".job-title-href")
                        
                        if not role_elem: continue # Ad or invalid card

                        role = (await role_elem.inner_text()).strip()
                        company = (await company_elem.inner_text()).strip() if company_elem else "Unknown"
                        location = (await location_elem.inner_text()).strip() if location_elem else "Remote" # Default or parse
                        stipend = (await stipend_elem.inner_text()).strip() if stipend_elem else "Not disclosed"
                        link = "https://internshala.com" + await link_elem.get_attribute("href")
                        
                        # Extract Posted Date
                        # Usually in .status-success or .status-container span containing "Posted"
                        # We'll try to find text referencing "Posted" in the card
                        posted_date = None
                        try:
                            status_elem = await card.query_selector(".status-success") or await card.query_selector(".status")
                            if status_elem:
                                status_text = await status_elem.inner_text()
                                if "Posted" in status_text:
                                    posted_date = parse_posted_date(status_text)
                        except:
                            pass
                            
                        # Filter by date (Max 3 days)
                        if not is_recent(posted_date, max_days=3):
                            self.logger.info(f"Skipping old job: {role} (Posted: {posted_date})")
                            continue

                        job = {
                            "site": "Internshala",
                            "company": company,
                            "role": role,
                            "stipend": stipend,
                            "location": location,
                            "link": link,
                            "deadline": None, 
                            "posted_date": posted_date or datetime.now().strftime("%Y-%m-%d")
                        }
                        jobs.append(job)
                        
                    except Exception as e:
                        self.logger.error(f"Error parsing job card: {e}")
            
        except Exception as e:
            self.logger.error(f"Error scraping Internshala: {e}")
        finally:
            await page.close()
            
        return jobs

    async def verify_eligibility(self, link):
        """
        Visits the job detail page to check for specific ineligibility criteria.
        Returns Tuple (is_eligible, reason)
        """
        if not self.browser:
            return True, "No browser"

        page = await self.browser.new_page()
        try:
            self.logger.info(f"Verifying eligibility for: {link}")
            await page.goto(link, timeout=30000)
            await page.wait_for_load_state("domcontentloaded")
            
            content = await page.content()
            content_lower = content.lower()
            
            # Check 1: Women only
            if "women expecting to start/restart their career" in content_lower:
                # Assuming general user is a student, and this category is restrictive
                return False, "Women returning to work only"
            
            # Check 2: "Who can apply" heavy restrictions
            # This is harder to parse generally without specific user profile gender/etc.
            # But the "Women" one is the most common cause of "Not Eligible" for general male students
            
            return True, "Eligible"
            
        except Exception as e:
            self.logger.error(f"Error verifying eligibility: {e}")
            return True, "Error verifying" # Fail open to avoid blocking valid jobs on error
        finally:
            await page.close()
