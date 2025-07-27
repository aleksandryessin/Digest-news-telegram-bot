# AI News Digest Bot Setup Guide

This guide will help you set up and run the daily AI news digest bot that posts to Telegram.

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **OpenAI API key** (for article summarization)
3. **Telegram Bot Token** and **Channel ID**

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Environment File

Create a `.env` file in the project root:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Telegram Bot Configuration  
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=@your_channel_username

# Optional Configuration
MAX_ARTICLES_PER_DIGEST=15
SUMMARY_MAX_WORDS=100
DIGEST_TIME=09:00
```

### 3. Telegram Setup

#### Create a Telegram Bot:
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot`
3. Follow instructions to create your bot
4. Copy the bot token to your `.env` file

#### Create a Channel:
1. Create a new Telegram channel
2. Add your bot as an administrator with "Post Messages" permission
3. Use the channel username (e.g., `@your_channel_name`) in the `.env` file

### 4. Get OpenAI API Key

1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your `.env` file

## 🧪 Testing the Setup

Test your configuration:

```bash
python daily_digest_bot.py run-once
```

This will:
- Test database connection
- Test Telegram bot connection  
- Test OpenAI API
- Collect articles from news sources
- Generate summaries
- Post a digest to your Telegram channel

## 🔧 Running the Bot

### Run Once (Manual)
```bash
python daily_digest_bot.py run-once
```

### Collect Articles Only
```bash
python daily_digest_bot.py collect
```

### Create Digest Only (from existing articles)
```bash
python daily_digest_bot.py digest
```

### Start Daily Scheduler
```bash
python daily_digest_bot.py schedule
```

The scheduler will run continuously and post digests at the configured time daily.

## 🗂️ File Structure

```
news digest/
├── daily_digest_bot.py       # Main bot orchestrator
├── multi_source_ai_digest.py # Article collection from news sources
├── article_extractor.py      # Web scraping and content extraction
├── ai_summarizer.py          # OpenAI-powered summarization
├── database.py               # SQLite database management
├── telegram_bot.py           # Telegram posting functionality
├── requirements.txt          # Python dependencies
├── .env                      # Configuration (create this)
└── news_digest.db            # SQLite database (auto-created)
```

## ⚙️ Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for summarization | Required |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | Required |
| `TELEGRAM_CHANNEL_ID` | Channel username or ID | Required |
| `MAX_ARTICLES_PER_DIGEST` | Max articles in daily digest | 15 |
| `SUMMARY_MAX_WORDS` | Max words per article summary | 100 |
| `DIGEST_TIME` | Daily posting time (24h format) | 09:00 |
| `DATABASE_PATH` | SQLite database file path | news_digest.db |

### News Sources

The bot collects from these sources:
- TechCrunch
- Wired  
- The Verge
- VentureBeat
- MIT Technology Review
- Ars Technica
- ZDNet
- Forbes
- Bloomberg

## 🎯 How It Works

1. **Collection**: Scrapes AI-related articles from major tech news sources
2. **Scoring**: Ranks articles by relevance using keyword analysis
3. **Extraction**: Downloads full article content using web scraping
4. **Summarization**: Generates concise summaries using OpenAI API
5. **Storage**: Saves articles and summaries in SQLite database
6. **Posting**: Formats and posts top articles to Telegram channel
7. **Scheduling**: Runs automatically at configured time daily

## 🔍 Troubleshooting

### Common Issues

**"Telegram bot error"**
- Check bot token is correct
- Ensure bot is admin in the channel
- Try using channel ID instead of username

**"OpenAI API error"**  
- Verify API key is correct
- Check you have credits in your OpenAI account
- Bot will use fallback summaries if OpenAI fails

**"No articles found"**
- Check internet connection
- Some sources may be temporarily unavailable
- Try running `collect` command manually

**"Database error"**
- Ensure write permissions in directory
- Delete `news_digest.db` to reset

### Getting Help

1. Check the console output for specific error messages
2. Run test command: `python daily_digest_bot.py run-once`  
3. Verify all environment variables are set correctly

## 📊 Monitoring

### View Statistics
```python
from database import NewsDatabase
db = NewsDatabase()
stats = db.get_stats(days=7)
print(stats)
```

### Check Recent Articles  
```python
articles = db.get_top_articles(days=1, limit=10)
for article in articles:
    print(f"{article['title']} - Score: {article['relevance_score']}")
```

## 🚀 Production Deployment

### Using systemd (Linux)

1. Create service file `/etc/systemd/system/ai-digest-bot.service`:
```ini
[Unit]
Description=AI News Digest Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/news digest
ExecStart=/usr/bin/python3 daily_digest_bot.py schedule
Restart=always
RestartSec=10

[Install]  
WantedBy=multi-user.target
```

2. Enable and start:
```bash
sudo systemctl enable ai-digest-bot
sudo systemctl start ai-digest-bot
```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "daily_digest_bot.py", "schedule"]
```

Build and run:
```bash
docker build -t ai-digest-bot .
docker run -d --name ai-digest-bot --env-file .env ai-digest-bot
```

## 🎉 You're Ready!

Your AI news digest bot is now configured and ready to automatically post daily AI news summaries to your Telegram channel! 