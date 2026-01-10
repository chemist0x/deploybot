# Narrative Detection Bot 🔍

An automated bot that monitors news sources, trending topics, and X (Twitter) to detect emerging narratives using AI-powered analysis.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

## 🚀 Features

- 📰 **Multi-source monitoring** (News APIs, X/Twitter, RSS feeds)
- 🤖 **AI-powered narrative detection** using sentiment analysis
- 📊 **Real-time trend clustering** and correlation
- 🔔 **Configurable alerts** for strong narratives
- 📈 **Historical narrative tracking** with SQLite database
- 🎯 **Customizable filters** for keywords and topics
- 🐳 **Docker support** for easy deployment
- 📦 **Systemd service** for production deployment
- 🔍 **Monitoring dashboard** with health checks

## 📋 Prerequisites

- Python 3.8+
- X (Twitter) API credentials (Elevated access recommended)
- News API key
- OpenAI API key (optional, for enhanced analysis)

## ⚡ Quick Start

### Using Setup Script (Recommended)

```bash
# Make setup script executable
chmod +x scripts/setup.sh

# Run setup
./scripts/setup.sh
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/narrative-detection-bot.git
cd narrative-detection-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"

# Copy and configure environment
cp .env.example .env
# Edit .env with your API credentials

# Run the bot
python main.py
```

## 🐳 Docker Deployment

```bash
# Build image
docker-compose build

# Run container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down
```

## 🔧 Configuration

Edit `config.yaml` to customize:
- Monitoring interval and sources
- Keywords and hashtags to track
- News sources and categories
- Narrative detection thresholds
- Alert settings

Example:
```yaml
monitoring:
  interval_minutes: 15
  sources:
    - twitter
    - news_api
    - rss_feeds

narrative_detection:
  min_mentions: 10
  min_sources: 3
  sentiment_threshold: 0.3
```

## 📊 Viewing Results

### Check Latest Narratives
```bash
python view_narratives.py
```

### Generate Report
```bash
python scripts/generate_report.py --date 2024-01-15
```

### Monitor Status
```bash
python scripts/health_check.py
```

## 🔄 Production Deployment

### Install as Systemd Service (Linux)

```bash
sudo ./scripts/install_service.sh
sudo systemctl start narrative-bot
sudo systemctl enable narrative-bot
sudo systemctl status narrative-bot
```

### Monitor Logs
```bash
# View live logs
sudo journalctl -u narrative-bot -f

# View logs from today
sudo journalctl -u narrative-bot --since today
```

## 📁 Output Structure

```
output/
├── narratives/          # JSON files with detected narratives
├── reports/             # HTML daily reports
└── database/            # SQLite database
logs/
├── bot.log             # Application logs
└── alerts.log          # Alert history
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=. tests/

# Run specific test
python -m pytest tests/test_collectors.py
```

## 📚 API Keys Setup

### Twitter/X API
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Create a new app
3. Get API keys and tokens
4. Add to `.env` file

### News API
1. Sign up at [newsapi.org](https://newsapi.org)
2. Get API key
3. Add to `.env` file

### OpenAI (Optional)
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create API key
3. Add to `.env` file

## 🔍 Monitoring & Alerts

The bot supports multiple alert methods:
- Console output
- Log files
- Email notifications
- Webhook integration (coming soon)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Tweepy](https://www.tweepy.org/) for Twitter API access
- [News API](https://newsapi.org/) for news aggregation
- [NLTK](https://www.nltk.org/) for natural language processing
- [scikit-learn](https://scikit-learn.org/) for machine learning

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check existing issues and discussions
- Review the documentation

## 🗺️ Roadmap

- [ ] Web dashboard for visualization
- [ ] Real-time WebSocket alerts
- [ ] Multi-language support
- [ ] Advanced ML models for narrative detection
- [ ] Integration with more data sources
- [ ] Sentiment analysis improvements
