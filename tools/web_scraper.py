import requests
from bs4 import BeautifulSoup
import re
import time
import random

class TwitterWebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_latest_tweets(self, username, retries=1):
        try:
            # Try to get tweets from public profile
            url = f"https://twitter.com/{username}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                # Parse HTML for tweet content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for tweet content in various possible selectors
                tweet_selectors = [
                    '[data-testid="tweet"]',
                    '.tweet-text',
                    '[data-testid="tweetText"]',
                    '.TweetTextSize'
                ]
                
                tweets = []
                for selector in tweet_selectors:
                    tweet_elements = soup.select(selector)
                    for element in tweet_elements[:5]:  # Get first 5
                        text = element.get_text(strip=True)
                        if text and len(text) > 10:  # Filter out empty/short tweets
                            tweets.append(text)
                
                if tweets:
                    return tweets[:5]
                else:
                    # If no tweets found, try alternative approach
                    print(f"Could not find tweets for @{username}, trying alternative method...")
                    return self._get_tweets_alternative(username)
            else:
                return self._get_tweets_alternative(username)
                
        except Exception as e:
            if retries > 0:
                print(f"Retrying scrape due to error: {e}")
                time.sleep(random.uniform(1, 3))
                return self.get_latest_tweets(username, retries-1)
            else:
                return self._get_tweets_alternative(username)
    
    def _get_tweets_alternative(self, username):
        """Try alternative methods to get tweets"""
        try:
            # Try using nitter or other public Twitter mirrors
            nitter_url = f"https://nitter.net/{username}"
            response = self.session.get(nitter_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                tweet_elements = soup.select('.tweet-content')
                tweets = []
                for element in tweet_elements[:5]:
                    text = element.get_text(strip=True)
                    if text and len(text) > 10:
                        tweets.append(text)
                
                if tweets:
                    print(f"Found {len(tweets)} tweets from alternative source")
                    return tweets
        except:
            pass
        
        # Final fallback: return empty list so we can still analyze
        print(f"Could not retrieve tweets for @{username}")
        return []
