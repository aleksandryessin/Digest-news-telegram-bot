#!/usr/bin/env python3
"""
AI News Digest Bot - Main Entry Point
Integrates all components to create and post daily AI news digests to Telegram.
"""

import os
import sys
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import our custom modules
from src.extractors import fetch_all_ai_sources, calculate_relevance_score, ArticleExtractor
from src.services import AISummarizer, NewsDatabase, TelegramDigestBot
from src.utils import setup_logging, get_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

class DailyDigestBot:
    """Main bot that orchestrates the daily digest creation and posting."""
    
    def __init__(self):
        self.db = NewsDatabase()
        self.extractor = ArticleExtractor()
        self.summarizer = AISummarizer()
        self.telegram_bot = TelegramDigestBot()
        
        # Configuration
        self.max_articles = int(os.getenv('MAX_ARTICLES_PER_DIGEST', 15))
        self.summary_max_words = int(os.getenv('SUMMARY_MAX_WORDS', 100))
        self.digest_time = os.getenv('DIGEST_TIME', '09:00')
    
    def collect_and_process_articles(self, limit_per_source=10):
        """
        Collect articles from all sources and process them.
        
        Args:
            limit_per_source (int): Max articles to process per source
            
        Returns:
            int: Number of new articles processed
        """
        logger.info("🔄 Starting article collection and processing...")
        
        # Fetch articles from all sources
        all_articles = fetch_all_ai_sources()
        
        if not all_articles:
            logger.warning("❌ No articles found from any source")
            return 0
        
        logger.info(f"📊 Found {len(all_articles)} total articles")
        
        new_articles_count = 0
        processed_by_source = {}
        
        # Process articles by source
        for source, url, title in all_articles:
            if source not in processed_by_source:
                processed_by_source[source] = 0
            
            # Limit articles per source to avoid overwhelming
            if processed_by_source[source] >= limit_per_source:
                continue
            
            try:
                # Calculate relevance score first
                score, breakdown = calculate_relevance_score(url, title)
                
                # Skip low-relevance articles
                if score < 30:
                    continue
                
                logger.info(f"  📰 Processing: {title[:50]}... (Score: {score})")
                
                # Extract full article content
                article_data = self.extractor.extract_article(url, source)
                article_data['source'] = source
                article_data['relevance_score'] = score
                
                # Add to database
                article_id = self.db.add_article(article_data)
                
                # Generate summary if we have content
                if article_data.get('content') and len(article_data['content']) > 100:
                    summary = self.summarizer.summarize_article(
                        article_data['title'],
                        article_data['content'],
                        self.summary_max_words
                    )
                    
                    # Update database with summary
                    self.db.update_article_summary(article_id, summary)
                    logger.info(f"    ✅ Summarized and saved (ID: {article_id})")
                    new_articles_count += 1
                else:
                    logger.warning(f"    ⚠️ Skipped (insufficient content)")
                
                processed_by_source[source] += 1
                
                # Add delay to be respectful
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"    ❌ Error processing {url}: {e}")
                continue
        
        # Update source statistics
        for source, count in processed_by_source.items():
            self.db.update_source_stats(source, count, count)
        
        logger.info(f"✅ Processed {new_articles_count} new articles")
        return new_articles_count
    
    def create_daily_digest(self, date=None):
        """
        Create and post daily digest.
        
        Args:
            date (str): Date in YYYY-MM-DD format (defaults to today)
            
        Returns:
            dict: Result of digest creation and posting
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📋 Creating daily digest for {date}...")
        
        # For manual testing, allow reposting same day
        if self.db.has_digest_for_date(date):
            logger.info(f"ℹ️ Digest already posted for {date} - posting anyway for test")
            # Don't return early for manual tests
        
        # Get top articles
        top_articles = self.db.get_top_articles(days=1, limit=self.max_articles)
        
        if not top_articles:
            logger.warning("❌ No articles found for digest")
            return {'success': False, 'reason': 'no_articles'}
        
        logger.info(f"📊 Selected {len(top_articles)} articles for digest")
        
        # Post to Telegram
        try:
            result = self.telegram_bot.send_digest_sync(top_articles, date=date)
            
            if result['success']:
                # Record successful post
                article_ids = [article['id'] for article in top_articles]
                self.db.record_digest_post(
                    article_ids, 
                    result['message_id'], 
                    date
                )
                
                logger.info(f"✅ Digest posted successfully! Message ID: {result['message_id']}")
                return {
                    'success': True,
                    'message_id': result['message_id'],
                    'articles_count': len(top_articles)
                }
            else:
                logger.error(f"❌ Failed to post digest: {result['error']}")
                return {'success': False, 'reason': 'telegram_error', 'error': result['error']}
                
        except Exception as e:
            logger.error(f"❌ Error posting digest: {e}")
            return {'success': False, 'reason': 'exception', 'error': str(e)}
    
    def run_daily_job(self):
        """Run the complete daily job: collect articles and create digest."""
        print(f"\n{'='*60}")
        print(f"🚀 Starting daily digest job at {datetime.now()}")
        print(f"{'='*60}")
        
        try:
            # Step 1: Collect and process new articles
            new_articles = self.collect_and_process_articles()
            
            # Step 2: Create and post digest (even if no new articles, use recent ones)
            result = self.create_daily_digest()
            
            # Step 3: Print summary
            print(f"\n📈 Daily job summary:")
            print(f"   • New articles processed: {new_articles}")
            print(f"   • Digest posted: {'✅ Success' if result['success'] else '❌ Failed'}")
            
            if result['success']:
                print(f"   • Articles in digest: {result['articles_count']}")
                print(f"   • Message ID: {result['message_id']}")
            elif 'error' in result:
                print(f"   • Error: {result['error']}")
            
            # Step 4: Print database stats
            stats = self.db.get_stats(days=7)
            print(f"\n📊 Week stats:")
            print(f"   • Total articles: {stats['article_stats']['total_articles']}")
            print(f"   • Summarized: {stats['article_stats']['summarized']}")
            print(f"   • Average score: {stats['article_stats']['avg_score']:.1f}")
            
        except Exception as e:
            print(f"❌ Daily job failed: {e}")
            # Send error notification
            try:
                self.telegram_bot.send_simple_message(
                    f"🚨 Daily digest job failed: {str(e)}"
                )
            except:
                pass
        
        print(f"{'='*60}")
        print(f"🏁 Daily job completed at {datetime.now()}")
        print(f"{'='*60}\n")
    
    def setup_scheduler(self):
        """Setup the daily scheduler."""
        print(f"⏰ Setting up daily scheduler for {self.digest_time}")
        schedule.every().day.at(self.digest_time).do(self.run_daily_job)
        print("✅ Scheduler configured")
    
    def run_scheduler(self):
        """Run the scheduler loop."""
        self.setup_scheduler()
        
        print("🔄 Starting scheduler loop...")
        print("   Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n👋 Scheduler stopped by user")
    
    def test_setup(self):
        """Test all components."""
        print("🧪 Testing setup...")
        
        # Test database
        try:
            stats = self.db.get_stats()
            print("✅ Database connection OK")
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
        
        # Test Telegram bot
        try:
            result = self.telegram_bot.test_connection_sync()
            if result['success']:
                print(f"✅ Telegram bot OK (Channel: {result['chat_title']})")
            else:
                print(f"❌ Telegram bot error: {result['error']}")
                return False
        except Exception as e:
            print(f"❌ Telegram bot error: {e}")
            return False
        
        # Test OpenAI (optional)
        try:
            test_summary = self.summarizer.summarize_article(
                "Test Title", 
                "This is a test article content to verify OpenAI API connection."
            )
            print("✅ OpenAI API OK")
        except Exception as e:
            print(f"⚠️ OpenAI API warning: {e} (will use fallback summaries)")
        
        print("✅ Setup test completed")
        return True

def main():
    """Main entry point."""
    print("🤖 AI News Digest Bot")
    print("=" * 40)
    
    # Create bot instance
    bot = DailyDigestBot()
    
    # Test setup
    if not bot.test_setup():
        print("❌ Setup test failed. Please check your configuration.")
        return
    
    # Check command line arguments
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'run-once':
            print("🚀 Running digest job once...")
            bot.run_daily_job()
            
        elif command == 'collect':
            print("📥 Collecting articles only...")
            bot.collect_and_process_articles()
            
        elif command == 'digest':
            print("📋 Creating digest only...")
            result = bot.create_daily_digest()
            print(f"Result: {result}")
            
        elif command == 'schedule':
            print("⏰ Starting scheduler...")
            bot.run_scheduler()
            
        else:
            print(f"Unknown command: {command}")
            print("Available commands: run-once, collect, digest, schedule")
    else:
        print("Starting scheduler by default...")
        bot.run_scheduler()

if __name__ == "__main__":
    main() 