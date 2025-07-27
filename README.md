# 🤖 AI News Digest Bot

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://docker.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991.svg)](https://openai.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4.svg)](https://telegram.org)

Автоматизированный бот для сбора, анализа и публикации дайджестов новостей ИИ в Telegram каналах на русском языке.

**English**: An automated bot that collects, analyzes, and publishes AI news digests to Telegram channels in Russian.

## ✨ Features

- 🌍 **Multi-source collection** from 9 major tech news sites
- 🧠 **AI-powered summarization** using OpenAI GPT-4o-mini
- 🇷🇺 **Russian language** summaries and interface
- 📱 **Telegram integration** with beautiful formatting
- 🗄️ **Smart deduplication** with SQLite database
- ⏰ **Scheduled posting** with configurable timing
- 🐳 **Docker deployment** for easy hosting
- 📊 **Comprehensive logging** and monitoring

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key
- Telegram Bot Token and Channel ID

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd ai-news-digest-bot
cp config/.env.example .env
```

### 2. Configure Environment
Edit `.env` file with your credentials:
```bash
OPENAI_API_KEY=your_openai_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_username
```

### 3. Deploy
```bash
cd scripts/
./deploy.sh start
```

### 4. Test
```bash
./deploy.sh test    # Run immediate test
./deploy.sh logs    # View real-time logs
./deploy.sh status  # Check bot status
```

## 📁 Project Structure

```
ai-news-digest-bot/
├── src/                    # Source code
│   ├── main.py            # Main entry point
│   ├── extractors/        # News collection modules
│   ├── services/          # Core business logic
│   └── utils/             # Utility functions
├── config/                # Configuration files
├── scripts/               # Deployment scripts
├── docs/                  # Documentation
└── Dockerfile             # Docker configuration
```

For detailed structure, see [Project Structure](docs/project_structure.md).

## 🎯 How It Works

1. **🔍 Collection**: Scrapes articles from 9 major AI news sources
2. **📊 Scoring**: Ranks articles by relevance using keyword analysis
3. **📄 Extraction**: Downloads full article content with source-specific parsers
4. **🤖 Summarization**: Generates concise Russian summaries using OpenAI
5. **💾 Storage**: Saves to SQLite database with deduplication
6. **📱 Publishing**: Posts formatted digest to Telegram channel
7. **⏰ Automation**: Runs daily at configured time

## 📱 Sample Output

```
🤖 Дайджест ИИ - 2025-01-27
📈 Самые важные новости искусственного интеллекта за сегодня

1. Google May Launch Low-Cost AI Plan To Rival ChatGPT
📰 Forbes • Google разрабатывает новый более доступный тариф "Gemini AI Lite"...
🔗 Читать

2. OpenAI unveils 'ChatGPT agent' that gives ChatGPT its own...
📰 VentureBeat • OpenAI представила новый функционал ChatGPT agent...
🔗 Читать

@LetsTalkAI
#AI #ИИ #OpenAI #Google #ChatGPT #TechNews
```

## 🛠️ Commands

### Docker Commands
```bash
./deploy.sh start     # Start the bot
./deploy.sh stop      # Stop the bot
./deploy.sh restart   # Restart the bot
./deploy.sh test      # Run test digest
./deploy.sh logs      # View logs
./deploy.sh status    # Check status
./deploy.sh build     # Rebuild image
```

### Local Development
```bash
python src/main.py run-once    # One-time execution
python src/main.py collect     # Collect articles only
python src/main.py digest      # Create digest only
python src/main.py schedule    # Start scheduler
```

## ⚙️ Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for summarization | Required |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | Required |
| `TELEGRAM_CHANNEL_ID` | Channel username or ID | Required |
| `MAX_ARTICLES_PER_DIGEST` | Max articles in digest | 15 |
| `SUMMARY_MAX_WORDS` | Max words per summary | 100 |
| `DIGEST_TIME` | Daily posting time (24h format) | 09:00 |

### News Sources
- **TechCrunch** - AI category
- **Wired** - Artificial Intelligence
- **The Verge** - AI coverage
- **VentureBeat** - AI section
- **MIT Technology Review** - AI topic
- **Ars Technica** - AI articles
- **ZDNet** - AI news
- **Forbes** - AI section
- **Bloomberg** - AI topics

## 📊 Monitoring

### View Statistics
```bash
./deploy.sh status
```

### Check Logs
```bash
./deploy.sh logs
```

### Database Stats
```python
from src.services.database import NewsDatabase
db = NewsDatabase()
stats = db.get_stats(days=7)
print(stats)
```

## 🔧 Development

### Setup Development Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r config/requirements.txt
```

### Run Tests
```bash
python src/main.py run-once
```

### Add New Sources
1. Edit `src/extractors/source_extractor.py`
2. Add extraction logic to `src/extractors/article_extractor.py`
3. Test with new source

## 🐳 Production Deployment

### Using systemd (Linux)
```bash
sudo cp scripts/ai-digest-bot.service /etc/systemd/system/
sudo systemctl enable ai-digest-bot
sudo systemctl start ai-digest-bot
```

### Using Docker Swarm
```bash
docker stack deploy -c scripts/docker-compose.yml ai-digest
```

### Cloud Deployment
- Works on any Docker-compatible platform
- AWS ECS, Google Cloud Run, Azure Container Instances
- Requires persistent volume for database

## 🔍 Troubleshooting

### Common Issues

**Bot not posting to channel:**
- Verify bot is admin in channel
- Check `TELEGRAM_CHANNEL_ID` format
- Test with `./deploy.sh test`

**OpenAI API errors:**
- Verify API key is correct
- Check account has credits
- Bot uses fallback summaries if API fails

**No articles collected:**
- Check internet connectivity
- Some sources may be temporarily unavailable
- Review logs for specific errors

### Getting Help
1. Check [Setup Guide](docs/setup_guide.md)
2. Review logs: `./deploy.sh logs`
3. Test individual components: `./deploy.sh test`

## 📝 Documentation

- [Setup Guide](docs/setup_guide.md) - Detailed installation instructions
- [Project Structure](docs/project_structure.md) - Code organization
- [API Documentation](docs/api.md) - Service interfaces

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4o-mini API
- Telegram for Bot API
- All the news sources for their content
- Open source community for the tools and libraries

---

**Made with ❤️ for the AI community**

For support or questions, please open an issue on GitHub. 