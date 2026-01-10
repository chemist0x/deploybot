"""Sentiment Analysis Module"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from loguru import logger


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        logger.info("Sentiment analyzer initialized")
    
    def analyze(self, items):
        """Analyze sentiment for each item."""
        for item in items:
            text = item.get('text', '') or item.get('title', '')
            
            if text:
                scores = self.analyzer.polarity_scores(text)
                item['sentiment'] = scores['compound']
                item['sentiment_scores'] = scores
            else:
                item['sentiment'] = 0
                item['sentiment_scores'] = {'neg': 0, 'neu': 1, 'pos': 0, 'compound': 0}
        
        return items
