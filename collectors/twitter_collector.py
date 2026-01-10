"""Twitter/X Data Collector"""

import os
import tweepy
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class TwitterCollector:
    def __init__(self, config):
        self.config = config['twitter']
        
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        if not bearer_token:
            logger.warning("Twitter Bearer Token not found. Twitter collection disabled.")
            self.client = None
            return
        
        try:
            self.client = tweepy.Client(
                bearer_token=bearer_token,
                wait_on_rate_limit=True
            )
            logger.success("Twitter client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")
            self.client = None
    
    def collect(self):
        """Collect recent tweets based on configuration."""
        if not self.client:
            logger.warning("Twitter client not available")
            return []
        
        tweets_data = []
        
        try:
            keywords = self.config.get('track_keywords', [])
            hashtags = self.config.get('track_hashtags', [])
            
            query_parts = keywords + hashtags
            query = ' OR '.join(query_parts) if query_parts else 'breaking news'
            
            max_results = min(self.config.get('max_tweets_per_cycle', 100), 100)
            
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'lang'],
                expansions=['author_id'],
                user_fields=['username', 'verified']
            )
            
            if tweets.data:
                for tweet in tweets.data:
                    tweets_data.append({
                        'source': 'twitter',
                        'id': str(tweet.id),
                        'text': tweet.text,
                        'created_at': tweet.created_at.isoformat(),
                        'metrics': tweet.public_metrics,
                        'lang': tweet.lang,
                        'url': f'https://twitter.com/i/web/status/{tweet.id}'
                    })
            
        except Exception as e:
            logger.error(f"Error collecting tweets: {e}")
        
        return tweets_data
