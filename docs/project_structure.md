# AI News Digest Bot - Project Structure

This document outlines the project structure and organization of the AI News Digest Bot.

## 📁 Directory Structure

```
ai-news-digest-bot/
├── src/                          # Source code
│   ├── __init__.py              # Main package
│   ├── main.py                  # Entry point and main orchestrator
│   ├── extractors/              # News extraction modules
│   │   ├── __init__.py
│   │   ├── article_extractor.py # Individual article content extraction
│   │   └── source_extractor.py  # Multi-source news collection
│   ├── services/                # Core business services
│   │   ├── __init__.py
│   │   ├── ai_summarizer.py     # OpenAI summarization service
│   │   ├── database.py          # SQLite database management
│   │   └── telegram_bot.py      # Telegram posting service
│   └── utils/                   # Utility modules
│       ├── __init__.py
│       ├── extract_links.py     # HTML link extraction
│       └── logger_config.py     # Logging configuration
├── config/                      # Configuration files
│   ├── .env.example            # Environment variables template
│   └── requirements.txt        # Python dependencies
├── scripts/                     # Deployment and utility scripts
│   ├── deploy.sh               # Docker deployment script
│   └── docker-compose.yml      # Docker Compose configuration
├── docs/                        # Documentation
│   ├── README.md               # Main project documentation
│   ├── setup_guide.md          # Setup and installation guide
│   └── project_structure.md    # This file
├── Dockerfile                   # Docker image configuration
├── .gitignore                  # Git ignore rules
├── .env                        # Environment variables (excluded from git)
└── data/                       # Persistent data (created by Docker)
    ├── news_digest.db          # SQLite database
    └── logs/                   # Application logs
```

## 🏗️ Architecture Overview

### **Core Components**

1. **Main Orchestrator** (`src/main.py`)
   - Entry point for the application
   - Coordinates all services
   - Handles scheduling and command-line interface

2. **Extractors** (`src/extractors/`)
   - **Source Extractor**: Collects articles from 9 news sources
   - **Article Extractor**: Downloads and parses individual article content

3. **Services** (`src/services/`)
   - **AI Summarizer**: Generates Russian summaries using OpenAI
   - **Database**: Manages article storage and deduplication
   - **Telegram Bot**: Formats and posts digests to channels

4. **Utilities** (`src/utils/`)
   - **Link Extractor**: Parses HTML for article URLs
   - **Logger**: Structured logging configuration

### **Data Flow**

```
News Sources → Source Extractor → Article Extractor → AI Summarizer → Database → Telegram Bot → Channel
```

1. **Collection**: Fetch article URLs from news sources
2. **Extraction**: Download full article content
3. **Summarization**: Generate Russian summaries
4. **Storage**: Save to database with deduplication
5. **Publishing**: Format and post to Telegram

## 🔧 Configuration

### **Environment Variables** (`.env`)
- `OPENAI_API_KEY`: OpenAI API key for summarization
- `TELEGRAM_BOT_TOKEN`: Telegram bot authentication
- `TELEGRAM_CHANNEL_ID`: Target channel for posting
- `MAX_ARTICLES_PER_DIGEST`: Articles per digest (default: 15)
- `SUMMARY_MAX_WORDS`: Max words per summary (default: 100)
- `DIGEST_TIME`: Daily posting time (default: 09:00 UTC)

### **Dependencies** (`config/requirements.txt`)
- `beautifulsoup4`: HTML parsing
- `requests`: HTTP requests
- `openai`: AI summarization
- `python-telegram-bot`: Telegram integration
- `schedule`: Task scheduling
- `python-dotenv`: Environment management

## 🚀 Deployment

### **Docker Deployment**
```bash
cd scripts/
./deploy.sh start    # Start the bot
./deploy.sh test     # Run test digest
./deploy.sh logs     # View logs
./deploy.sh status   # Check status
```

### **Local Development**
```bash
python src/main.py run-once    # One-time run
python src/main.py collect     # Collect articles only
python src/main.py digest      # Create digest only
python src/main.py schedule    # Start scheduler
```

## 📊 Database Schema

### **Articles Table**
- `id`: Primary key
- `url`: Article URL (unique)
- `url_hash`: URL hash for deduplication
- `title`: Article title
- `content`: Full article text
- `summary`: Russian summary
- `source`: News source name
- `relevance_score`: AI relevance score
- `created_at`: Creation timestamp

### **Digest Posts Table**
- `id`: Primary key
- `date`: Digest date
- `article_ids`: JSON array of posted articles
- `telegram_message_id`: Telegram message ID
- `created_at`: Creation timestamp

### **Source Stats Table**
- `source`: News source name
- `date`: Processing date
- `articles_found`: Articles discovered
- `articles_processed`: Articles successfully processed

## 🔍 News Sources

The bot collects from these sources:
- **TechCrunch**: `https://techcrunch.com/tag/ai/`
- **Wired**: `https://www.wired.com/tag/artificial-intelligence/`
- **The Verge**: `https://www.theverge.com/ai-artificial-intelligence`
- **VentureBeat**: `https://venturebeat.com/ai/`
- **MIT Tech Review**: `https://www.technologyreview.com/topic/artificial-intelligence/`
- **Ars Technica**: `https://arstechnica.com/information-technology/artificial-intelligence/`
- **ZDNet**: `https://www.zdnet.com/topic/artificial-intelligence/`
- **Forbes**: `https://www.forbes.com/ai/`
- **Bloomberg**: `https://www.bloomberg.com/topics/artificial-intelligence`

## 📈 Monitoring

### **Logs**
- Console output with timestamps
- File logging to `/app/logs/bot.log`
- Structured logging with log levels

### **Statistics**
- Articles processed per source
- Success/failure rates
- Average relevance scores
- Database growth metrics

## 🛠️ Development

### **Adding New Sources**
1. Add URL and extraction logic to `src/extractors/source_extractor.py`
2. Add source-specific parsing to `src/extractors/article_extractor.py`
3. Update relevance scoring if needed

### **Modifying Summarization**
1. Edit prompts in `src/services/ai_summarizer.py`
2. Adjust OpenAI model parameters
3. Test with different content types

### **Changing Telegram Format**
1. Modify message templates in `src/services/telegram_bot.py`
2. Adjust character limits and formatting
3. Test with various article counts

## 🔐 Security

- API keys stored in environment variables
- Database file excluded from version control
- Docker secrets management
- Rate limiting for external APIs
- Input validation and sanitization 