import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterScraper:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=os.getenv('BEARER_TOKEN'),
            consumer_key=os.getenv('API_KEY'),
            consumer_secret=os.getenv('API_SECRET'),
            access_token=os.getenv('ACCESS_TOKEN'),
            access_token_secret=os.getenv('ACCESS_SECRET'),
            wait_on_rate_limit=True
        )
    
    def get_latest_tweets(self, username, retries=1):
        try:
            # Get user by username
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
                print("Retrying scrape due to error:", e)
                return self.get_latest_tweets(username, retries-1)
            else:
                raise e
