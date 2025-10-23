from dotenv import load_dotenv
from agent import run_twitter_analysis

# Load environment variables
load_dotenv()

def main():
    print("Twitter Insights Agent")
    print("=" * 50)
    
    username = input("Enter Twitter username (without @): ").strip()
    
    if not username:
        print("Please enter a valid username.")
        return
    
    try:
        print(f"\nAnalyzing tweets for @{username}...")
        insights = run_twitter_analysis(username)
        print(f"\nInsights from @{username}'s last 5 tweets:")
        print("-" * 40)
        for i, ins in enumerate(insights, 1):
            print(f"{i}. {ins}")
        print("-" * 40)
        print("Analysis completed successfully!")
        
    except Exception as e:
        print(f"\nError analyzing tweets: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your Twitter API credentials")
        print("2. Ensure the username exists and is public")
        print("3. Verify you have the correct API permissions")

if __name__ == "__main__":
    main()
