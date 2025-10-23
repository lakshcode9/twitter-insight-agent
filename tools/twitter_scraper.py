from .web_scraper import TwitterWebScraper

class TwitterScraper:
    def __init__(self):
        # Use web scraping instead of limited API
        self.web_scraper = TwitterWebScraper()
    
    def get_latest_tweets(self, username, retries=1):
        """Get latest tweets using web scraping"""
        return self.web_scraper.get_latest_tweets(username, retries)
