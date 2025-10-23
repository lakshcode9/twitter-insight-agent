#!/usr/bin/env python3

from textblob import TextBlob

def analyze_tweets(tweets):
    """Analyze tweet sentiment and return insights"""
    if not tweets:
        return ["No tweets found for this user."]
    
    insights = []
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    
    for tweet in tweets:
        polarity = TextBlob(tweet).sentiment.polarity
        if polarity > 0.2:
            sentiment_counts["positive"] += 1
            insights.append("Positive sentiment tweet.")
        elif polarity < -0.2:
            sentiment_counts["negative"] += 1
            insights.append("Negative or critical tone.")
        else:
            sentiment_counts["neutral"] += 1
            insights.append("Neutral or informative.")
    
    # Generate unique insights
    unique_insights = []
    
    # Add sentiment distribution insights
    if sentiment_counts["positive"] > 0:
        unique_insights.append(f"User shows positive sentiment in {sentiment_counts['positive']} tweet(s).")
    if sentiment_counts["negative"] > 0:
        unique_insights.append(f"User shows negative sentiment in {sentiment_counts['negative']} tweet(s).")
    if sentiment_counts["neutral"] > 0:
        unique_insights.append(f"User shows neutral sentiment in {sentiment_counts['neutral']} tweet(s).")
    
    # Ensure we have exactly 3 insights
    while len(unique_insights) < 3:
        unique_insights.append("Overall sentiment analysis completed.")
    
    return unique_insights[:3]

def test_mock_twitter_analysis():
    """Test the Twitter analysis functionality with mock data"""
    try:
        # Mock tweet data for testing
        mock_tweets = [
            "I love this new feature! It's amazing!",
            "This is terrible, I hate it.",
            "Just sharing some news about technology.",
            "Great day today, feeling positive!",
            "Neutral comment about the weather."
        ]
        
        print("Testing Twitter analysis with mock data...")
        print("\nMock tweets:")
        for i, tweet in enumerate(mock_tweets, 1):
            print(f"{i}. {tweet}")
        
        insights = analyze_tweets(mock_tweets)
        
        print(f"\nInsights from mock tweets:")
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
            
        print("\nMock Twitter analysis completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_mock_twitter_analysis()
