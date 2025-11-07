import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from app.config import Config
from app.exceptions import ScrapingError
from app.logger import logger

def scrape_with_requests(url: str) -> BeautifulSoup:
    """Scrape webpage using requests and BeautifulSoup"""
    try:
        response = requests.get(url, timeout=Config.SCRAPING_TIMEOUT)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        logger.error("scraping_failed", error=str(e), url=url, method="requests")
        raise ScrapingError(f"Failed to scrape {url}: {str(e)}")

def scrape_with_selenium(url: str) -> BeautifulSoup:
    """Scrape webpage using Selenium (for JavaScript-heavy sites)"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return BeautifulSoup(html, 'html.parser')
    except Exception as e:
        logger.error("scraping_failed", error=str(e), url=url, method="selenium")
        raise ScrapingError(f"Failed to scrape {url} with Selenium: {str(e)}")

def scrape_interest_rates(url: str) -> dict:
    """Scrape current interest rates from a bank's website"""
    try:
        if Config.USE_SELENIUM:
            soup = scrape_with_selenium(url)
        else:
            soup = scrape_with_requests(url)
            
        # This is a placeholder implementation
        # You would need to customize this based on the specific website's structure
        rates = {
            'savings': 0.0,
            'checking': 0.0,
            'cd': 0.0
        }
        
        logger.info("interest_rates_scraped", url=url, rates=rates)
        return rates
        
    except Exception as e:
        logger.error("interest_rate_scraping_failed", error=str(e), url=url)
        raise ScrapingError(f"Failed to scrape interest rates: {str(e)}")

def scrape_bank_info(url: str) -> dict:
    """Scrape bank information from a website"""
    try:
        if Config.USE_SELENIUM:
            soup = scrape_with_selenium(url)
        else:
            soup = scrape_with_requests(url)
            
        # This is a placeholder implementation
        # You would need to customize this based on the specific website's structure
        info = {
            'name': '',
            'description': '',
            'contact': '',
            'address': ''
        }
        
        logger.info("bank_info_scraped", url=url)
        return info
        
    except Exception as e:
        logger.error("bank_info_scraping_failed", error=str(e), url=url)
        raise ScrapingError(f"Failed to scrape bank info: {str(e)}")