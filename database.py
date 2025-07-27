import sqlite3
import hashlib
from datetime import datetime
import json

class NewsDatabase:
    """SQLite database for managing AI news articles and posting history."""
    
    def __init__(self, db_path="news_digest.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Articles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    url_hash TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT,
                    summary TEXT,
                    source TEXT NOT NULL,
                    relevance_score INTEGER,
                    word_count INTEGER,
                    excerpt TEXT,
                    domain TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Digest posts table (track what's been posted)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS digest_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE UNIQUE NOT NULL,
                    article_ids TEXT NOT NULL, -- JSON array of article IDs
                    telegram_message_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Source tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS source_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    date DATE NOT NULL,
                    articles_found INTEGER DEFAULT 0,
                    articles_processed INTEGER DEFAULT 0,
                    UNIQUE(source, date)
                )
            ''')
            
            conn.commit()
    
    def _generate_url_hash(self, url):
        """Generate a hash for URL to handle duplicates."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def add_article(self, article_data):
        """
        Add article to database if it doesn't exist.
        
        Args:
            article_data (dict): Article data
            
        Returns:
            int: Article ID, or existing ID if duplicate
        """
        url_hash = self._generate_url_hash(article_data['url'])
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if article already exists
            cursor.execute('SELECT id FROM articles WHERE url_hash = ?', (url_hash,))
            existing = cursor.fetchone()
            
            if existing:
                return existing[0]
            
            # Insert new article
            cursor.execute('''
                INSERT INTO articles (
                    url, url_hash, title, content, summary, source,
                    relevance_score, word_count, excerpt, domain
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article_data['url'],
                url_hash,
                article_data.get('title', ''),
                article_data.get('content', ''),
                article_data.get('summary', ''),
                article_data.get('source', ''),
                article_data.get('relevance_score', 0),
                article_data.get('word_count', 0),
                article_data.get('excerpt', ''),
                article_data.get('domain', '')
            ))
            
            return cursor.lastrowid
    
    def update_article_summary(self, article_id, summary):
        """Update article summary."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE articles 
                SET summary = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (summary, article_id))
            conn.commit()
    
    def get_articles_by_date(self, date=None, limit=50):
        """
        Get articles for a specific date.
        
        Args:
            date (str): Date in YYYY-MM-DD format (defaults to today)
            limit (int): Maximum number of articles
            
        Returns:
            list: List of article dicts
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # For dict-like access
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM articles 
                WHERE DATE(created_at) = ?
                ORDER BY relevance_score DESC, created_at DESC
                LIMIT ?
            ''', (date, limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_top_articles(self, days=1, limit=15):
        """
        Get top articles from last N days.
        
        Args:
            days (int): Number of days to look back
            limit (int): Maximum number of articles
            
        Returns:
            list: List of top articles
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM articles 
                WHERE created_at >= DATE('now', '-{} day')
                AND summary IS NOT NULL
                AND summary != ''
                ORDER BY relevance_score DESC, created_at DESC
                LIMIT ?
            '''.format(days), (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def has_digest_for_date(self, date=None):
        """Check if digest was already posted for date."""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM digest_posts WHERE date = ?', (date,))
            return cursor.fetchone() is not None
    
    def record_digest_post(self, article_ids, telegram_message_id=None, date=None):
        """Record that a digest was posted."""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO digest_posts (date, article_ids, telegram_message_id)
                VALUES (?, ?, ?)
            ''', (date, json.dumps(article_ids), telegram_message_id))
            conn.commit()
    
    def update_source_stats(self, source, articles_found, articles_processed, date=None):
        """Update statistics for a source."""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO source_stats (source, date, articles_found, articles_processed)
                VALUES (?, ?, ?, ?)
            ''', (source, date, articles_found, articles_processed))
            conn.commit()
    
    def get_stats(self, days=7):
        """Get statistics for last N days."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Article stats
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_articles,
                    COUNT(CASE WHEN summary IS NOT NULL AND summary != '' THEN 1 END) as summarized,
                    AVG(relevance_score) as avg_score
                FROM articles 
                WHERE created_at >= DATE('now', '-{} day')
            '''.format(days))
            article_stats = dict(cursor.fetchone())
            
            # Source stats
            cursor.execute('''
                SELECT source, SUM(articles_found) as found, SUM(articles_processed) as processed
                FROM source_stats 
                WHERE date >= DATE('now', '-{} day')
                GROUP BY source
            '''.format(days))
            source_stats = [dict(row) for row in cursor.fetchall()]
            
            return {
                'article_stats': article_stats,
                'source_stats': source_stats
            }

# Example usage
if __name__ == "__main__":
    db = NewsDatabase()
    
    # Test adding an article
    test_article = {
        'url': 'https://example.com/test-article',
        'title': 'Test Article',
        'content': 'This is test content.',
        'source': 'Test Source',
        'relevance_score': 75
    }
    
    article_id = db.add_article(test_article)
    print(f"Added article with ID: {article_id}")
    
    # Get stats
    stats = db.get_stats()
    print(f"Stats: {stats}") 