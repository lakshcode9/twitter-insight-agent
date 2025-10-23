import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterScraper:
    def __init__(self):
        # Try to get credentials from environment variables first
        api_key = os.getenv('API_KEY')
        api_secret = os.getenv('API_SECRET')
        access_token = os.getenv('ACCESS_TOKEN')
        access_secret = os.getenv('ACCESS_SECRET')
        
        # If env vars are not set, use the hardcoded values as fallback
        if not api_key:
            api_key = "JRjucqq1MH6uaZDdErc82e6MS"
            api_secret = "m5Tl1l8sYNP7vG5b4WdRrYtSIJfE17HZyO50nKAuVaZEbMmeJT"
            access_token = "1912214357637033984-k0iIT8s4h9Hm7WtF1B0iCrXgSGezdc"
            access_secret = "Lh96Zz0O3nfuW95EfcB82D4MWWq0YTXRz463GY7zLU2tp"
        
        # For Twitter API v2, we need to use OAuth 1.0a User Context
        auth = tweepy.OAuth1UserHandler(
            api_key,
            api_secret,
            access_token,
            access_secret
        )
        
        self.client = tweepy.Client(
            bearer_token=None,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
            wait_on_rate_limit=True
        )
    
    def get_latest_tweets(self, username, retries=1):
        try:
            # Try API v2 first
            user = self.client.get_user(username=username)
            if not user.data:
                raise ValueError(f"User @{username} not found")
            
            # Get user's tweets
            tweets = self.client.get_users_tweets(
                id=user.data.id,
                max_results=5,
                tweet_fields=['created_at', 'public_metrics']
            )
            
            if not tweets.data:
                return []
                
            # Extract tweet content
            tweet_contents = []
            for tweet in tweets.data:
                tweet_contents.append(tweet.text)
            
            return tweet_contents
            
        except Exception as e:
            if retries > 0:
                print(f"Retrying scrape due to error: {e}")
                return self.get_latest_tweets(username, retries-1)
            else:
                # If API v2 fails, provide a helpful error message
                if "401" in str(e) or "Unauthorized" in str(e):
                    raise Exception("Twitter API authentication failed. Please check your API credentials.")
                else:
                    raise e
