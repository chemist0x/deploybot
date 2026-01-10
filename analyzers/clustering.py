"""Narrative Clustering Module"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from loguru import logger
import numpy as np


class NarrativeClustering:
    def __init__(self, config):
        self.config = config['narrative_detection']['clustering']
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    
    def cluster(self, items):
        """Cluster items by similarity."""
        if len(items) < 2:
            return {0: items}
        
        try:
            # Extract text
            texts = [item.get('text', '') or item.get('title', '') for item in items]
            
            # Vectorize
            X = self.vectorizer.fit_transform(texts)
            
            # Cluster
            clustering = DBSCAN(
                eps=self.config.get('eps', 0.3),
                min_samples=self.config.get('min_cluster_size', 5),
                metric='cosine'
            )
            
            labels = clustering.fit_predict(X)
            
            # Group by cluster
            clusters = {}
            for idx, label in enumerate(labels):
                if label == -1:  # Noise
                    continue
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(items[idx])
            
            logger.info(f"Created {len(clusters)} clusters from {len(items)} items")
            return clusters
            
        except Exception as e:
            logger.error(f"Clustering error: {e}")
            return {0: items}
