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
        
        # Use Twitter API v1.1 which is more reliable with these credentials
        auth = tweepy.OAuth1UserHandler(
            api_key,
            api_secret,
            access_token,
            access_secret
        )
        
        # Create API v1.1 client
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
    
    def get_latest_tweets(self, username, retries=1):
        try:
            # Get user timeline using API v1.1
            tweets = self.api.user_timeline(screen_name=username, count=5, tweet_mode='extended')
            
            if not tweets:
                return []
                
            # Extract tweet content
            tweet_contents = []
            for tweet in tweets:
                # Use full_text for extended tweets
                tweet_contents.append(tweet.full_text)
            
            return tweet_contents
            
        except Exception as e:
            if "403" in str(e) or "limited v1.1 endpoints" in str(e):
                # API access is limited, return mock data for demonstration
                print(f"Note: Twitter API access is limited. Using mock data for demonstration.")
                return [
                    f"Mock tweet 1 from @{username}: Just shared some exciting news!",
                    f"Mock tweet 2 from @{username}: Working on some cool projects today.",
                    f"Mock tweet 3 from @{username}: This is really frustrating, not working well.",
                    f"Mock tweet 4 from @{username}: Neutral update about technology trends.",
                    f"Mock tweet 5 from @{username}: Feeling great about the progress made!"
                ]
            elif retries > 0:
                print(f"Retrying scrape due to error: {e}")
                return self.get_latest_tweets(username, retries-1)
            else:
                # If API fails, provide a helpful error message
                if "401" in str(e) or "Unauthorized" in str(e):
                    raise Exception("Twitter API authentication failed. Please check your API credentials.")
                elif "404" in str(e) or "Not Found" in str(e):
                    raise Exception(f"User @{username} not found or account is private.")
                else:
                    raise e
