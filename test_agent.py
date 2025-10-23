#!/usr/bin/env python3

from agent import run_twitter_analysis

def test_twitter_analysis():
    """Test the Twitter analysis functionality"""
    try:
        # Test with a known Twitter username
        username = "trikcode"
        print(f"Testing Twitter analysis for @{username}...")
        
        insights = run_twitter_analysis(username)
        
        print(f"\nInsights from @{username}'s last 5 tweets:")
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
            
        print("\nTwitter analysis completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_twitter_analysis()
