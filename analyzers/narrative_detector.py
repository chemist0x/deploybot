"""Narrative Detection Engine"""

from datetime import datetime
from collections import Counter
from loguru import logger
import re


class NarrativeDetector:
    def __init__(self, config):
        self.config = config['narrative_detection']
    
    def detect(self, clusters):
        """Detect narratives from clustered data."""
        narratives = []
        
        for cluster_id, items in clusters.items():
            if len(items) < self.config['min_mentions']:
                continue
            
            sources = set(item['source'] for item in items)
            if len(sources) < self.config['min_sources']:
                continue
            
            sentiments = [item.get('sentiment', 0) for item in items]
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            
            strength = self.calculate_strength(items, sources, avg_sentiment)
            themes = self.extract_themes(items)
            
            timestamps = []
            for item in items:
                if 'created_at' in item:
                    try:
                        ts = datetime.fromisoformat(item['created_at'].replace('Z', '+00:00'))
                        timestamps.append(ts)
                    except:
                        pass
            
            narrative = {
                'id': f'narrative_{cluster_id}_{int(datetime.now().timestamp())}',
                'detected_at': datetime.now().isoformat(),
                'strength': strength,
                'mention_count': len(items),
                'source_count': len(sources),
                'sources': list(sources),
                'sentiment': {
                    'average': round(avg_sentiment, 3),
                    'positive': sum(1 for s in sentiments if s > 0.1),
                    'negative': sum(1 for s in sentiments if s < -0.1),
                    'neutral': sum(1 for s in sentiments if -0.1 <= s <= 0.1)
                },
                'themes': themes,
                'time_range': {
                    'start': min(timestamps).isoformat() if timestamps else None,
                    'end': max(timestamps).isoformat() if timestamps else None
                },
                'sample_content': [item.get('text', '')[:200] for item in items[:3]],
                'urls': [item.get('url') for item in items[:5] if item.get('url')]
            }
            
            narratives.append(narrative)
        
