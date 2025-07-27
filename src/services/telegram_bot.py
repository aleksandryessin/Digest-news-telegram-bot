import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()

class TelegramDigestBot:
    """Telegram bot for posting AI news digests to channels."""
    
    def __init__(self, bot_token=None, channel_id=None):
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.channel_id = channel_id or os.getenv('TELEGRAM_CHANNEL_ID')
        
        if not self.bot_token:
            raise ValueError("Telegram bot token is required")
        if not self.channel_id:
            raise ValueError("Telegram channel ID is required")
        
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def format_digest_message(self, articles, date=None):
        """
        Format articles into a Telegram message with Russian summaries.
        
        Args:
            articles (list): List of article dicts
            date (str): Date for the digest
            
        Returns:
            str: Formatted message
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Header
        message = f"🤖 **Дайджест новостей ИИ - {date}**\n"
        message += f"🚀 _Будущее уже здесь: главные события в мире искусственного интеллекта_\n"
        message += f"📊 Топ {len(articles)} новостей из {len(set(a.get('source', '') for a in articles))} источников\n\n"
        
        # Articles - optimized for Telegram limits
        for i, article in enumerate(articles[:10], 1):  # Limit to 10 for message length
            title = article.get('title', 'Без заголовка')
            summary = article.get('summary', 'Резюме недоступно')
            url = article.get('url', '')
            source = article.get('source', 'Неизвестно')
            score = article.get('relevance_score', 0)
            
            # Truncate title if too long
            if len(title) > 60:
                title = title[:57] + "..."
            
            # Ensure summary is in reasonable length
            if len(summary) > 150:
                summary = summary[:147] + "..."
            
            message += f"**{i}. {title}**\n"
            message += f"📰 _{source}_ • Рейтинг: {score}\n"
            message += f"📝 {summary}\n"
            message += f"🔗 [Читать полностью]({url})\n\n"
        
        # Footer with channel and hashtags
        message += f"@LetsTalkAI\n"
        message += f"#AI #ИИ #OpenAI #Google #ChatGPT #TechNews #ИскусственныйИнтеллект"
        
        return message
    
    def format_short_digest(self, articles, date=None):
        """
        Format a shorter version with enhanced Russian summaries.
        
        Args:
            articles (list): List of article dicts
            date (str): Date for the digest
            
        Returns:
            str: Formatted short message
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        message = f"🤖 **Дайджест ИИ - {date}**\n"
        message += f"📈 _Самые важные новости искусственного интеллекта за сегодня_\n\n"
        
        for i, article in enumerate(articles[:8], 1):  # Limit to 8 for shorter format
            title = article.get('title', 'Без заголовка')
            summary = article.get('summary', 'Резюме недоступно')
            url = article.get('url', '')
            source = article.get('source', 'Неизвестно')
            
            # Truncate title
            if len(title) > 45:
                title = title[:42] + "..."
            
            # Longer summary - up to 120 characters
            if len(summary) > 120:
                # Try to end at sentence boundary
                truncated = summary[:120]
                last_period = truncated.rfind('.')
                if last_period > 80:  # If there's a reasonable sentence break
                    enhanced_summary = summary[:last_period + 1]
                else:
                    enhanced_summary = truncated + "..."
            else:
                enhanced_summary = summary
            
            message += f"**{i}. {title}**\n"
            message += f"📰 _{source}_ • {enhanced_summary}\n"
            message += f"🔗 [Читать]({url})\n\n"
        
        # Footer with channel and hashtags
        message += f"@LetsTalkAI\n"
        message += f"#AI #ИИ #OpenAI #Google #ChatGPT #TechNews #ИскусственныйИнтеллект"
        
        return message
    
    def send_digest(self, articles, use_short_format=False, date=None):
        """
        Send digest to Telegram channel using requests (synchronous).
        
        Args:
            articles (list): List of article dicts
            use_short_format (bool): Use shorter format
            date (str): Date for the digest
            
        Returns:
            dict: Response with message_id and success status
        """
        try:
            if use_short_format:
                message = self.format_short_digest(articles, date)
            else:
                message = self.format_digest_message(articles, date)
            
            # Check message length (Telegram limit is ~4096 characters)
            if len(message) > 3800:  # More conservative limit
                print("Сообщение слишком длинное, использую короткий формат...")
                message = self.format_short_digest(articles, date)
            
            # Send message using requests
            url = f"{self.api_url}/sendMessage"
            payload = {
                'chat_id': self.channel_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, data=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('ok'):
                return {
                    'success': True,
                    'message_id': result['result']['message_id'],
                    'message': message
                }
            else:
                return {
                    'success': False,
                    'error': result.get('description', 'Unknown error'),
                    'message': message
                }
            
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': message if 'message' in locals() else None
            }
    
    def send_simple_message(self, text):
        """Send a simple text message to the channel."""
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                'chat_id': self.channel_id,
                'text': text,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, data=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                return result['result']['message_id']
            else:
                print(f"Error sending simple message: {result.get('description')}")
                return None
        except Exception as e:
            print(f"Error sending simple message: {e}")
            return None
    
    def test_connection(self):
        """Test if the bot can access the channel."""
        try:
            # Try to get chat info
            url = f"{self.api_url}/getChat"
            payload = {'chat_id': self.channel_id}
            
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                chat = result['result']
                return {
                    'success': True,
                    'chat_title': chat.get('title', 'Unknown'),
                    'chat_type': chat.get('type', 'Unknown')
                }
            else:
                return {
                    'success': False,
                    'error': result.get('description', 'Unknown error')
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_digest_sync(self, articles, use_short_format=False, date=None):
        """Send digest (now synchronous)."""
        return self.send_digest(articles, use_short_format, date)
    
    def test_connection_sync(self):
        """Test connection (now synchronous)."""
        return self.test_connection()

# Example usage
if __name__ == "__main__":
    # You'll need to set these in your .env file:
    # TELEGRAM_BOT_TOKEN=your_bot_token
    # TELEGRAM_CHANNEL_ID=@your_channel_username or channel_id
    
    bot = TelegramDigestBot()
    
    # Test connection
    result = bot.test_connection_sync()
    print(f"Connection test: {result}")
    
    # Test with sample articles
    sample_articles = [
        {
            'title': 'OpenAI Unveils ChatGPT Agent',
            'summary': 'OpenAI has announced a new ChatGPT agent that can autonomously use your email and web applications, marking a significant step forward in AI automation.',
            'url': 'https://example.com/article1',
            'source': 'TechCrunch',
            'relevance_score': 85
        },
        {
            'title': 'Google Launches New AI Model',
            'summary': 'Google has released Gemini 2.0, featuring improved reasoning capabilities and faster processing speeds.',
            'url': 'https://example.com/article2',
            'source': 'The Verge',
            'relevance_score': 80
        }
    ]
    
    # Send test digest
    # result = bot.send_digest_sync(sample_articles)
    # print(f"Send result: {result}") 