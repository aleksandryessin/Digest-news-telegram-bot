#!/bin/bash

# AI News Digest Bot - Deployment Script

set -e

echo "🤖 AI News Digest Bot - Docker Deployment"
echo "=========================================="

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.production .env
    echo "📝 Please edit .env file with your API keys and tokens:"
    echo "   - OPENAI_API_KEY"
    echo "   - TELEGRAM_BOT_TOKEN" 
    echo "   - TELEGRAM_CHANNEL_ID"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs

# Function to show usage
show_usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start       - Start the bot (default)"
    echo "  stop        - Stop the bot"
    echo "  restart     - Restart the bot"
    echo "  logs        - Show bot logs"
    echo "  status      - Show bot status"
    echo "  test        - Run a test digest"
    echo "  build       - Build Docker image"
    echo "  update      - Pull latest code and restart"
    echo ""
}

# Get command line argument
COMMAND=${1:-start}

case $COMMAND in
    "start")
        echo "🚀 Starting AI News Digest Bot..."
        docker-compose up -d
        echo "✅ Bot started successfully!"
        echo "📊 Check logs with: $0 logs"
        ;;
    
    "stop")
        echo "🛑 Stopping AI News Digest Bot..."
        docker-compose down
        echo "✅ Bot stopped successfully!"
        ;;
    
    "restart")
        echo "🔄 Restarting AI News Digest Bot..."
        docker-compose down
        docker-compose up -d
        echo "✅ Bot restarted successfully!"
        ;;
    
    "logs")
        echo "📋 Bot logs (press Ctrl+C to exit):"
        docker-compose logs -f ai-digest-bot
        ;;
    
    "status")
        echo "📊 Bot status:"
        docker-compose ps
        echo ""
        echo "🔍 Health check:"
        docker-compose exec ai-digest-bot python -c "
import sys; sys.path.append('/app')
from src.services.database import NewsDatabase
import os
db = NewsDatabase('/app/data/news_digest.db')
stats = db.get_stats(days=7)
print(f'Articles in last 7 days: {stats[\"article_stats\"][\"total_articles\"]}')
print(f'Summarized articles: {stats[\"article_stats\"][\"summarized\"]}')
print(f'Average relevance score: {stats[\"article_stats\"][\"avg_score\"]:.1f}')
" 2>/dev/null || echo "Bot not running or database not accessible"
        ;;
    
    "test")
        echo "🧪 Running test digest..."
        docker-compose exec ai-digest-bot python src/main.py run-once
        ;;
    
    "build")
        echo "🔨 Building Docker image..."
        docker-compose build
        echo "✅ Build completed!"
        ;;
    
    "update")
        echo "📥 Updating bot..."
        git pull || echo "⚠️  Git pull failed (continuing anyway)"
        docker-compose build
        docker-compose down
        docker-compose up -d
        echo "✅ Bot updated and restarted!"
        ;;
    
    "help"|"-h"|"--help")
        show_usage
        ;;
    
    *)
        echo "❌ Unknown command: $COMMAND"
        show_usage
        exit 1
        ;;
esac 