"""News API Data Collector"""

import os
import requests
from datetime import datetime, timedelta
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class NewsCollector:
    def __init__(self, config):
        self.config = config['news']
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = 'https://newsapi.org/v2'
        
        if not self.api_key:
            logger.warning("News API key not found. News collection disabled.")
    
    def collect(self):
        """Collect news articles from News API."""
        if not self.api_key:
            return []
        
        articles_data = []
        
        try:
            from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            params = {
                'apiKey': self.api_key,
                'from': from_date,
                'sortBy': 'popularity',
                'language': 'en',
                'pageSize': min(self.config.get('max_articles_per_cycle', 100), 100)
            }
            
            if self.config.get('sources'):
                params['sources'] = ','.join(self.config['sources'][:20])
                response = requests.get(f'{self.base_url}/everything', params=params, timeout=10)
            else:
                params['country'] = self.config.get('countries', ['us'])[0]
                response = requests.get(f'{self.base_url}/top-headlines', params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for article in data.get('articles', []):
                    if article.get('title') and article.get('title') != '[Removed]':
                        articles_data.append({
                            'source': 'news_api',
                            'title': article.get('title'),
                            'text': (article.get('description', '') + ' ' + article.get('content', '')).strip(),
                            'author': article.get('author'),
                            'created_at': article.get('publishedAt'),
                            'url': article.get('url'),
                            'source_name': article.get('source', {}).get('name')
                        })
            else:
                logger.error(f"News API error: {response.status_code}")
        
        except Exception as e:
            logger.error(f"Error collecting news: {e}")
        
        return articles_data
