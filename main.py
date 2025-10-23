import os
from dotenv import load_dotenv
from agent import run_twitter_analysis

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    username = input("Enter Twitter username (without @): ")
    
    try:
        insights = run_twitter_analysis(username)
        print(f"\nInsights from @{username}'s last 5 tweets:")
        for i, ins in enumerate(insights, 1):
            print(f"{i}. {ins}")
    except Exception as e:
        print(f"Error analyzing tweets: {e}")
        print("Please check your Twitter API credentials and ensure the username exists.")
