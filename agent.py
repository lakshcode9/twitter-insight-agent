import openai
import re
from tools.twitter_scraper import TwitterScraper

# Set up OpenRouter API for DeepSeek model
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

def analyze_tweets_with_ai(tweets, username):
    """Analyze tweets using DeepSeek AI for real insights"""
    if not tweets:
        return [f"No tweets found for @{username}.", "User may have a private account.", "Unable to analyze content."]
    
    # Prepare tweets for analysis
    tweets_text = "\n".join([f"Tweet {i+1}: {tweet}" for i, tweet in enumerate(tweets)])
    
    prompt = f"""
    Analyze the following tweets from @{username} and provide exactly 3 unique insights about their content, sentiment, and patterns:

    {tweets_text}

    Please provide 3 specific insights about:
    1. Sentiment patterns (positive, negative, neutral)
    2. Content themes or topics
    3. Communication style or behavior patterns

    Format your response as 3 separate insights, each starting with a number and being specific to this user's content.
    """
    
    try:
        response = openai.chat.completions.create(
            model="deepseek/deepseek-r1-distill-qwen-7b",
            messages=[
                {"role": "system", "content": "You are an expert social media analyst who provides specific, actionable insights about Twitter content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        insights_text = response.choices[0].message.content.strip()
        
        # Parse the response into individual insights
        insights = []
        lines = insights_text.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line.startswith(('1.', '2.', '3.', '-', '*')) or len(insights) < 3):
                # Clean up the insight text
                insight = re.sub(r'^\d+\.\s*', '', line)
                insight = re.sub(r'^[-*]\s*', '', insight)
                if insight and len(insight) > 10:
                    insights.append(insight)
        
        # Ensure we have exactly 3 insights
        while len(insights) < 3:
            if len(insights) == 0:
                insights.append("Unable to analyze tweets due to technical issues.")
            elif len(insights) == 1:
                insights.append("Additional analysis needed for complete insights.")
            else:
                insights.append("Analysis completed with available data.")
        
        return insights[:3]
        
    except Exception as e:
        print(f"AI analysis failed: {e}")
        # Fallback to basic analysis
        return analyze_tweets_fallback(tweets, username)

def analyze_tweets_fallback(tweets, username):
    """Advanced fallback analysis that provides unique insights per user"""
    from textblob import TextBlob
    import re
    
    if not tweets:
        return [
            f"@{username} has no recent tweets available for analysis.",
            "Account may be private or have limited activity.",
            "Unable to provide insights without tweet content."
        ]
    
    # Analyze sentiment
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    sentiment_scores = []
    
    # Analyze topics and themes
    all_text = " ".join(tweets).lower()
    tech_words = ["ai", "technology", "tech", "software", "code", "programming", "innovation"]
    business_words = ["business", "company", "market", "revenue", "growth", "strategy"]
    personal_words = ["i", "me", "my", "feel", "think", "believe", "love", "hate"]
    
    tech_count = sum(1 for word in tech_words if word in all_text)
    business_count = sum(1 for word in business_words if word in all_text)
    personal_count = sum(1 for word in personal_words if word in all_text)
    
    # Analyze tweet characteristics
    avg_length = sum(len(tweet) for tweet in tweets) / len(tweets)
    has_questions = sum(1 for tweet in tweets if "?" in tweet)
    has_exclamations = sum(1 for tweet in tweets if "!" in tweet)
    
    for tweet in tweets:
        polarity = TextBlob(tweet).sentiment.polarity
        sentiment_scores.append(polarity)
        if polarity > 0.2:
            sentiment_counts["positive"] += 1
        elif polarity < -0.2:
            sentiment_counts["negative"] += 1
        else:
            sentiment_counts["neutral"] += 1
    
    # Generate unique insights based on analysis
    insights = []
    
    # Insight 1: Sentiment analysis
    if sentiment_counts["positive"] > sentiment_counts["negative"]:
        insights.append(f"@{username} maintains an optimistic tone with {sentiment_counts['positive']} positive tweets out of {len(tweets)}.")
    elif sentiment_counts["negative"] > sentiment_counts["positive"]:
        insights.append(f"@{username} shows more critical sentiment with {sentiment_counts['negative']} negative tweets out of {len(tweets)}.")
    else:
        insights.append(f"@{username} demonstrates balanced sentiment across {len(tweets)} tweets.")
    
    # Insight 2: Content themes
    if tech_count > business_count and tech_count > personal_count:
        insights.append(f"@{username} focuses heavily on technology topics, with {tech_count} tech-related mentions.")
    elif business_count > tech_count and business_count > personal_count:
        insights.append(f"@{username} emphasizes business and strategy content, with {business_count} business-related mentions.")
    else:
        insights.append(f"@{username} shares a mix of personal and professional content.")
    
    # Insight 3: Communication style
    if has_questions > len(tweets) // 2:
        insights.append(f"@{username} uses an interactive communication style with frequent questions ({has_questions} questions).")
    elif avg_length > 100:
        insights.append(f"@{username} prefers detailed communication with longer tweets (avg {avg_length:.0f} characters).")
    elif has_exclamations > 0:
        insights.append(f"@{username} uses enthusiastic communication with {has_exclamations} exclamatory statements.")
    else:
        insights.append(f"@{username} maintains a professional and measured communication style.")
    
    return insights[:3]

def run_twitter_analysis(username):
    """Main function to run Twitter analysis"""
    try:
        scraper = TwitterScraper()
        tweets = scraper.get_latest_tweets(username)
        insights = analyze_tweets_with_ai(tweets, username)
        return insights
    except Exception as e:
        raise Exception(f"Error in Twitter analysis: {str(e)}")
