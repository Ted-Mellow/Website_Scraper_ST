"""
Flexible Website Scraper
Extracts company names and profile links from JSON-LD structured data or HTML patterns
"""

import requests
import json
import csv
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional, Tuple
import logging
import asyncio
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FlexibleScraper:
    def __init__(self, base_url: str, output_file: Optional[str] = None):
        self.base_url = base_url
        self.output_file = output_file
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.exhibitors: List[Dict[str, str]] = []
        self.extraction_method = "unknown"

    def fetch_page(self, page_num: int = 1, use_page_param: bool = True, use_browser: bool = False) -> Optional[str]:
        """Fetch a single page and return HTML content"""
        if use_browser:
            return self._fetch_page_with_browser(page_num, use_page_param)

        try:
            if use_page_param:
                # Try common page parameter patterns
                for param in ['?page=', '?p=', '?page_num=']:
                    url = f"{self.base_url}{param}{page_num}"
                    try:
                        response = self.session.get(url, timeout=10)
                        response.raise_for_status()
                        return response.text
                    except:
                        continue
                # If all params fail, try with &
                url = f"{self.base_url}&page={page_num}"
            else:
                url = self.base_url

            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.warning(f"Error fetching page {page_num}: {e}")
            return None

    def _fetch_page_with_browser(self, page_num: int = 1, use_page_param: bool = True) -> Optional[str]:
        """Fetch page using headless browser (Playwright) for JavaScript-rendered content"""
        try:
            # Build URL
            if use_page_param:
                for param in ['?page=', '?p=', '?page_num=']:
                    url = f"{self.base_url}{param}{page_num}"
                    try:
                        # Try this URL
                        html = asyncio.run(self._async_fetch_browser(url))
                        if html:
                            return html
                    except:
                        continue
                # Fallback
                url = f"{self.base_url}&page={page_num}"
            else:
                url = self.base_url

            html = asyncio.run(self._async_fetch_browser(url))
            return html

        except Exception as e:
            logger.warning(f"Error fetching with browser: {e}")
            return None

    async def _async_fetch_browser(self, url: str) -> Optional[str]:
        """Async helper to fetch page with Playwright"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()

                # Set timeout and navigate
                await page.goto(url, timeout=30000, wait_until='networkidle')

                # Get rendered HTML
                html = await page.content()

                await browser.close()
                return html
        except Exception as e:
            logger.warning(f"Browser fetch failed for {url}: {e}")
            return None

    def parse_html_fallback(self, html: str, base_url: str) -> List[Dict[str, str]]:
        """Fallback: Extract companies from HTML pattern matching"""
        companies = []
        soup = BeautifulSoup(html, 'html.parser')

        # Common selectors for company listings
        selectors = [
            ('a[href*="company"], a[href*="profile"], a[href*="exhibitor"]', 'href'),
            ('.company a, .exhibitor a, .vendor a, .listing a, .card a', 'href'),
            ('article a[href], section a[href]:not([class*="nav"])', 'href'),
            ('li a[href]:not([class*="nav"], [class*="footer"])', 'href'),
            ('h2 a, h3 a', 'href'),
        ]

        found_links = set()

        for selector, attr in selectors:
            try:
                elements = soup.select(selector)
                for elem in elements:
                    href = elem.get(attr, '').strip()
                    text = elem.get_text(strip=True)

                    if not href or not text or len(text) < 2:
                        continue

                    # Skip navigation/footer links
                    skip_keywords = ['home', 'about', 'contact', 'privacy', 'terms', 'register', 'login', 'sign', 'menu', 'nav']
                    if any(kw in text.lower() or kw in href.lower() for kw in skip_keywords):
                        continue

                    # Make absolute URL
                    abs_url = urljoin(base_url, href)

                    # Deduplicate
                    link_tuple = (text, abs_url)
                    if link_tuple not in found_links:
                        found_links.add(link_tuple)
                        companies.append({
                            'name': text,
                            'url': abs_url
                        })
            except Exception as e:
                logger.warning(f"Error with selector '{selector}': {e}")
                continue

        return companies

    def parse_jsonld_companies(self, html: str) -> List[Dict[str, str]]:
        """Extract companies from JSON-LD structured data"""
        companies = []
        soup = BeautifulSoup(html, 'html.parser')

        # Find all JSON-LD script tags
        script_tags = soup.find_all('script', type='application/ld+json')

        for script in script_tags:
            try:
                data = json.loads(script.string)

                # Handle ProfilePage schema (single company)
                if data.get('@type') == 'ProfilePage':
                    company = self._extract_from_profile_page(data)
                    if company and company.get('name') and company.get('url'):
                        companies.append(company)

                # Handle ItemList schema (multiple companies)
                elif data.get('@type') == 'ItemList':
                    items = data.get('itemListElement', [])
                    for item in items:
                        company = self._extract_from_item(item)
                        if company and company.get('name') and company.get('url'):
                            companies.append(company)

            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON-LD block: {e}")
                continue

        return companies

    def _extract_from_profile_page(self, data: Dict) -> Optional[Dict[str, str]]:
        """Extract company info from ProfilePage schema"""
        try:
            entity = data.get('mainEntity', {})
            if entity.get('@type') != 'Organization':
                return None

            return {
                'name': entity.get('name', '').strip(),
                'url': entity.get('url', '').strip()
            }
        except Exception as e:
            logger.warning(f"Error extracting from ProfilePage: {e}")
            return None

    def _extract_from_item(self, item: Dict) -> Optional[Dict[str, str]]:
        """Extract company info from ItemList item"""
        try:
            # Handle different schema patterns
            url = item.get('url') or item.get('link')
            name = item.get('name') or item.get('title')

            if not url or not name:
                return None

            return {
                'name': name.strip(),
                'url': url.strip()
            }
        except Exception as e:
            logger.warning(f"Error extracting from item: {e}")
            return None

    def scrape_all_pages(self, start_page: int = 1, max_pages: int = 20, use_browser: bool = False) -> Tuple[int, str]:
        """Scrape multiple pages with auto-stop when empty"""
        successful_pages = 0
        pages_scraped = 0

        for page in range(start_page, start_page + max_pages):
            logger.info(f"Scraping page {page}{'(browser)' if use_browser else ''}...")
            html = self.fetch_page(page, use_browser=use_browser)

            if not html:
                logger.warning(f"Failed to fetch page {page}, stopping")
                break

            # Try JSON-LD first
            companies = self.parse_jsonld_companies(html)

            if companies:
                self.exhibitors.extend(companies)
                logger.info(f"Found {len(companies)} companies on page {page} (JSON-LD)")
                self.extraction_method = "JSON-LD"
                successful_pages += 1
                pages_scraped += 1
            else:
                # Try HTML fallback
                companies = self.parse_html_fallback(html, self.base_url)
                if companies:
                    self.exhibitors.extend(companies)
                    logger.info(f"Found {len(companies)} companies on page {page} (HTML fallback)")
                    self.extraction_method = "HTML fallback"
                    successful_pages += 1
                    pages_scraped += 1
                else:
                    logger.info(f"No companies found on page {page}, stopping")
                    break

        return successful_pages, self.extraction_method

    def get_unique_exhibitors(self) -> List[Dict[str, str]]:
        """Return deduplicated exhibitors"""
        unique = {}
        for exhibitor in self.exhibitors:
            url = exhibitor['url']
            if url not in unique:
                unique[url] = exhibitor
        return list(unique.values())

    def save_to_csv(self) -> bool:
        """Save exhibitors to CSV file"""
        if not self.output_file or not self.exhibitors:
            return False

        try:
            unique = self.get_unique_exhibitors()
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'url'])
                writer.writeheader()
                writer.writerows(unique)

            logger.info(f"Saved {len(unique)} unique exhibitors to {self.output_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            return False

    def run(self, start_page: int = 1, max_pages: int = 20, use_browser: bool = False) -> Tuple[List[Dict[str, str]], str]:
        """Run the complete scraping workflow, return results instead of writing CSV"""
        mode = "browser" if use_browser else "fast"
        logger.info(f"Starting scrape from page {start_page}, max {max_pages} pages ({mode} mode)")

        successful, method = self.scrape_all_pages(start_page, max_pages, use_browser=use_browser)

        if successful == 0:
            logger.warning("No companies found")
            return [], "none"

        unique = self.get_unique_exhibitors()
        logger.info(f"Extracted {len(unique)} unique companies using {method}")

        # Save to CSV if output file is set
        if self.output_file:
            self.save_to_csv()

        return unique, method


# Backward compatibility alias
ExhibitorScraper = FlexibleScraper


if __name__ == "__main__":
    # Configuration
    BASE_URL = "https://www.retailtechnologyshow.com/exhibitors"
    OUTPUT_FILE = "exhibitors.csv"

    # Run scraper
    scraper = FlexibleScraper(BASE_URL, OUTPUT_FILE)
    results, method = scraper.run(start_page=1, max_pages=20)

    if results:
        print(f"\n✓ Found {len(results)} companies using {method}")
        print(f"✓ Saved to {OUTPUT_FILE}")
    else:
        print("\n✗ No companies found")
