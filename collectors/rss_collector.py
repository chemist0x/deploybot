"""RSS Feed Collector"""

import feedparser
from datetime import datetime
from loguru import logger


class RSSCollector:
    def __init__(self, config):
        self.feeds = config.get('rss_feeds', [])
    
    def collect(self):
        """Collect items from RSS feeds."""
        items_data = []
        
        for feed_config in self.feeds:
            try:
                feed = feedparser.parse(feed_config['url'])
                
                for entry in feed.entries[:50]:
                    items_data.append({
                        'source': 'rss',
                        'title': entry.get('title', ''),
                        'text': entry.get('summary', '') + ' ' + entry.get('description', ''),
                        'created_at': entry.get('published', datetime.now().isoformat()),
                        'url': entry.get('link', ''),
                        'source_name': feed_config['name']
                    })
                
            except Exception as e:
                logger.error(f"Error collecting from {feed_config['name']}: {e}")
        
        return items_data
