#!/usr/bin/env python3
"""
Narrative Detection Bot - Main Orchestrator
"""

import os
import sys
import time
import yaml
import schedule
from datetime import datetime
from loguru import logger

from collectors.twitter_collector import TwitterCollector
from collectors.news_collector import NewsCollector
from collectors.rss_collector import RSSCollector
from analyzers.sentiment_analyzer import SentimentAnalyzer
from analyzers.clustering import NarrativeClustering
from analyzers.narrative_detector import NarrativeDetector
from utils.data_processor import DataProcessor
from utils.alert_manager import AlertManager
from utils.database import Database
from utils.health_server import HealthServer


class NarrativeBot:
    def __init__(self, config_path='config.yaml'):
        """Initialize the narrative detection bot."""
        logger.info("Initializing Narrative Detection Bot...")
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Setup logging
        self._setup_logging()
        
        # Initialize database
        if self.config.get('database', {}).get('enabled', True):
            self.db = Database(self.config)
        else:
            self.db = None
        
        # Initialize collectors
        self.collectors = {}
        if 'twitter' in self.config['monitoring']['sources']:
            self.collectors['twitter'] = TwitterCollector(self.config)
        if 'news_api' in self.config['monitoring']['sources']:
            self.collectors['news'] = NewsCollector(self.config)
        if 'rss_feeds' in self.config['monitoring']['sources']:
            self.collectors['rss'] = RSSCollector(self.config)
        
        # Initialize analyzers
        self.sentiment = SentimentAnalyzer()
        self.clustering = NarrativeClustering(self.config)
        self.detector = NarrativeDetector(self.config)
        
        # Initialize utilities
        self.processor = DataProcessor()
        self.alerts = AlertManager(self.config)
        
        # Start health check server
        if self.config.get('health_check', {}).get('enabled', True):
            self.health_server = HealthServer(self.config)
            self.health_server.start()
        
        logger.success("Bot initialized successfully!")
    
    def _setup_logging(self):
        """Configure logging."""
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        log_file = os.getenv('LOG_FILE', 'logs/bot.log')
        
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # Configure logger
        logger.remove()
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            level=log_level
        )
        logger.add(
            log_file,
            rotation="500 MB",
            retention="30 days",
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}"
        )
    
    def collect_data(self):
        """Collect data from all sources."""
        logger.info("Starting data collection cycle...")
        
        all_data = []
        
        for name, collector in self.collectors.items():
            try:
                data = collector.collect()
                logger.info(f"Collected {len(data)} items from {name}")
                all_data.extend(data)
            except Exception as e:
                logger.error(f"Error collecting from {name}: {e}")
        
        logger.success(f"Total items collected: {len(all_data)}")
        return all_data
    
    def analyze_narratives(self, data):
        """Analyze collected data for emerging narratives."""
        logger.info("Analyzing data for narratives...")
        
        if not data:
            return []
        
        # Process and clean data
        processed = self.processor.process(data)
        
        # Perform sentiment analysis
        with_sentiment = self.sentiment.analyze(processed)
        
        # Cluster similar content
        clusters = self.clustering.cluster(with_sentiment)
        
        # Detect narratives
        narratives = self.detector.detect(clusters)
        
        logger.success(f"Detected {len(narratives)} narratives")
        return narratives
    
    def handle_narratives(self, narratives):
        """Process and alert on detected narratives."""
        if not narratives:
            logger.info("No significant narratives detected")
            return
        
        # Filter strong narratives
        strong = [n for n in narratives if n['strength'] >= 0.7]
        
        if strong:
            logger.warning(f"Found {len(strong)} strong narratives!")
            
            # Send alerts
            for narrative in strong:
                self.alerts.send(narrative)
            
            # Save to database
            if self.db:
                for narrative in strong:
                    self.db.save_narrative(narrative)
        
        # Save all results
        self.save_results(narratives)
    
    def save_results(self, narratives):
        """Save detected narratives to disk."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = 'output/narratives'
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON
        import json
        json_path = f"{output_dir}/narratives_{timestamp}.json"
        with open(json_path, 'w') as f:
            json.dump(narratives, f, indent=2)
        
        logger.info(f"Results saved to {json_path}")
    
    def run_cycle(self):
        """Run a complete monitoring cycle."""
        try:
            logger.info("=" * 60)
            logger.info(f"Starting cycle at {datetime.now()}")
            
            # Collect data
            data = self.collect_data()
            
            if data:
                # Analyze for narratives
                narratives = self.analyze_narratives(data)
                
                # Handle results
                self.handle_narratives(narratives)
            else:
                logger.warning("No data collected in this cycle")
            
            logger.info("Cycle completed successfully")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"Error in cycle: {e}", exc_info=True)
    
    def start(self):
        """Start the bot with scheduled monitoring."""
        logger.info("Starting Narrative Detection Bot...")
        
        interval = self.config['monitoring']['interval_minutes']
        
        # Schedule the monitoring cycle
        schedule.every(interval).minutes.do(self.run_cycle)
        
        # Run first cycle immediately
        self.run_cycle()
        
        # Keep running
        logger.info(f"Bot running. Monitoring every {interval} minutes...")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            if hasattr(self, 'health_server'):
                self.health_server.stop()


if __name__ == "__main__":
    bot = NarrativeBot()
    bot.start()
