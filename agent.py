from crewai import Agent, Task, Crew
from textblob import TextBlob
from tools.twitter_scraper import TwitterScraper

def analyze_tweets(tweets):
    insights = []
    for tweet in tweets:
        polarity = TextBlob(tweet).sentiment.polarity
        if polarity > 0.2:
            insights.append("Positive sentiment tweet.")
        elif polarity < -0.2:
            insights.append("Negative or critical tone.")
        else:
            insights.append("Neutral or informative.")
    unique = list(set(insights))
    return unique[:3]

def create_twitter_insight_crew():
    # Initialize the Twitter scraper
    scraper = TwitterScraper()
    
    # Create the Twitter Insight Agent
    twitter_agent = Agent(
        role='Twitter Data Analyst',
        goal='Analyze Twitter posts and extract meaningful insights from the last 5 tweets',
        backstory='You are an expert social media analyst who specializes in extracting insights from Twitter content using sentiment analysis.',
        verbose=True,
        allow_delegation=False
    )
    
    # Create the analysis task
    analysis_task = Task(
        description="""Analyze the sentiment of the last 5 tweets from a given Twitter username.
        Use the provided TwitterScraper to fetch the tweets, then analyze their sentiment using TextBlob.
        Return exactly 3 unique insights about the sentiment patterns found in the tweets.
        
        Input: Twitter username (without @)
        Output: List of 3 insights about the tweet sentiment patterns""",
        agent=twitter_agent,
        expected_output="A list of exactly 3 unique insights about the sentiment patterns in the user's last 5 tweets"
    )
    
    # Create the crew
    crew = Crew(
        agents=[twitter_agent],
        tasks=[analysis_task],
        verbose=2
    )
    
    return crew, scraper

def run_twitter_analysis(username):
    crew, scraper = create_twitter_insight_crew()
    
    # Get the tweets first
    tweets = scraper.get_latest_tweets(username)
    
    # Analyze tweets using our sentiment function
    insights = analyze_tweets(tweets)
    
    return insights
