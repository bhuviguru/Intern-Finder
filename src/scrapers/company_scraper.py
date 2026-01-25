from .base_scraper import BaseScraper
from src.utils.date_parser import parse_posted_date, is_recent
from datetime import datetime
import json

class CompanyScraper(BaseScraper):
    """
    Generic scraper for company career pages.
    Uses common patterns to extract job listings from various company websites.
    """
    
    def __init__(self, browser_instance=None):
        super().__init__(browser_instance)
        self.companies = self._load_companies()
    
    def _load_companies(self):
        """Load company configurations from companies.json"""
        try:
            with open('config/companies.json', 'r') as f:
                data = json.load(f)
                # Flatten all company categories into one list
                all_companies = []
                
                # Iterate through all keys except _comment
                for key, value in data.items():
                    if key.startswith('_'):
                        continue  # Skip metadata keys
                    if isinstance(value, list):
                        all_companies.extend(value)
                
                self.logger.info(f"Loaded {len(all_companies)} companies to scrape")
                return all_companies
        except Exception as e:
            self.logger.error(f"Error loading companies: {e}")
            return []
    
    async def scrape(self, keywords=None):
        """
        Scrape all configured company career pages
        keywords parameter is kept for compatibility but not used here
        """
        jobs = []
        if not self.browser:
            self.logger.error("Browser instance not set")
            return jobs
        
        page = await self.browser.new_page()
        
        for company in self.companies:
            try:
                company_jobs = await self._scrape_company(page, company)
                jobs.extend(company_jobs)
                self.logger.info(f"Found {len(company_jobs)} jobs from {company['name']}")
            except Exception as e:
                self.logger.error(f"Error scraping {company['name']}: {e}")
        
        await page.close()
        return jobs
    
    async def _scrape_company(self, page, company):
        """Scrape a single company's career page"""
        jobs = []
        company_name = company['name']
        careers_url = company['careers_url']
        search_keywords = company.get('keywords', ['intern'])
        
        self.logger.info(f"Scraping {company_name} careers page...")
        
        try:
            # Navigate to careers page
            await page.goto(careers_url, timeout=60000, wait_until='domcontentloaded')
            await page.wait_for_timeout(2000)  # Wait for dynamic content
            
            # Try multiple generic selectors for job listings
            job_selectors = [
                'div[class*="job"]',
                'div[class*="position"]',
                'div[class*="opening"]',
                'div[class*="role"]',
                'li[class*="job"]',
                'article',
                'a[href*="job"]',
                'a[href*="career"]'
            ]
            
            job_cards = []
            for selector in job_selectors:
                try:
                    cards = await page.query_selector_all(selector)
                    if len(cards) > 3:  # If we found a reasonable number
                        job_cards = cards[:20]  # Limit to first 20
                        break
                except:
                    continue
            
            if not job_cards:
                self.logger.warning(f"No job cards found for {company_name}")
                return jobs
            
            # Extract job details from cards
            for card in job_cards:
                try:
                    # Get all text content
                    text_content = await card.inner_text()
                    text_lower = text_content.lower()
                    
                    # Check if this is an internship/student opportunity
                    is_relevant = any(kw in text_lower for kw in search_keywords)
                    if not is_relevant:
                        continue
                    
                    # Try to extract role/title
                    role_selectors = ['h2', 'h3', 'h4', 'strong', 'a']
                    role = "Unknown Role"
                    for role_sel in role_selectors:
                        try:
                            role_elem = await card.query_selector(role_sel)
                            if role_elem:
                                role_text = await role_elem.inner_text()
                                if len(role_text.strip()) > 5 and len(role_text.strip()) < 100:
                                    role = role_text.strip()
                                    break
                        except:
                            continue
                    
                    # Try to extract link
                    link = careers_url
                    try:
                        link_elem = await card.query_selector('a')
                        if link_elem:
                            href = await link_elem.get_attribute('href')
                            if href:
                                if href.startswith('http'):
                                    link = href
                                elif href.startswith('/'):
                                    base_url = careers_url.split('/')[0] + '//' + careers_url.split('/')[2]
                                    link = base_url + href
                                else:
                                    link = careers_url + '/' + href
                    except:
                        pass
                    
                    # Extract location if available
                    location = "Not Specified"
                    location_keywords = ['location', 'office', 'city', 'remote']
                    lines = text_content.split('\n')
                    for line in lines:
                        if any(kw in line.lower() for kw in location_keywords):
                            location = line.strip()
                            break
                    
                    posted_date = None
                    # Try to find "Posted X days ago" in text
                    date_match = None
                    if "posted" in text_lower:
                        # Extract lines with "posted"
                        for line in text_content.split('\n'):
                            if "posted" in line.lower():
                                parsed = parse_posted_date(line)
                                if parsed:
                                    posted_date = parsed
                                    break
                    
                    # Filter by date
                    if not is_recent(posted_date, max_days=3):
                        # Strict check only if we actually found a date.
                        # If posted_date is None, is_recent returns True (safe).
                        # But if we found a date and it's old, skip.
                        if posted_date: # Explicit check to be sure
                             continue

                    job = {
                        "site": company_name,
                        "source_type": "company_direct",
                        "company": company_name,
                        "role": role,
                        "stipend": "Check Website",
                        "location": location,
                        "link": link,
                        "deadline": None,
                        "posted_date": posted_date or datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    jobs.append(job)
                    
                except Exception as e:
                    self.logger.error(f"Error parsing job card from {company_name}: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error navigating to {company_name} careers: {e}")
        
        return jobs
