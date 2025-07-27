import openai
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

class AISummarizer:
    """Generate AI-powered summaries for articles."""
    
    def __init__(self, api_key=None):
        self.client = openai.OpenAI(
            api_key=api_key or os.getenv('OPENAI_API_KEY')
        )
    
    def summarize_article(self, title, content, max_length=100):
        """
        Generate a concise summary of an article.
        
        Args:
            title (str): Article title
            content (str): Article content
            max_length (int): Maximum words in summary
            
        Returns:
            str: Generated summary
        """
        try:
            # Truncate content if too long (to avoid token limits)
            max_content_chars = 3000
            if len(content) > max_content_chars:
                content = content[:max_content_chars] + "..."
            
            prompt = f"""
Создайте краткое резюме этой статьи об ИИ/технологиях максимум в {max_length} слов на РУССКОМ ЯЗЫКЕ.
Сосредоточьтесь на ключевых фактах, разработках и последствиях.
Сделайте резюме интересным и информативным для технически подкованных читателей.

Заголовок: {title}

Содержание: {content}

Резюме на русском языке:"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Вы эксперт технологический журналист, который пишет четкие, краткие резюме новостей ИИ и технологий на русском языке."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            # Fallback: create simple summary from content
            return self._create_fallback_summary(content, max_length)
    
    def _create_fallback_summary(self, content, max_length):
        """Create a simple extractive summary as fallback."""
        try:
            sentences = content.split('. ')
            if len(sentences) < 2:
                return content[:200] + "..." if len(content) > 200 else content
            
            # Take first few sentences
            summary = '. '.join(sentences[:3]) + '.'
            
            # Truncate if too long
            words = summary.split()
            if len(words) > max_length:
                summary = ' '.join(words[:max_length]) + "..."
            
            return summary
        except:
            return "Summary not available."
    
    def batch_summarize(self, articles, max_length=100, delay=1):
        """
        Summarize multiple articles with rate limiting.
        
        Args:
            articles (list): List of article dicts with 'title' and 'content'
            max_length (int): Max words per summary
            delay (float): Delay between API calls
            
        Returns:
            list: Articles with added 'summary' field
        """
        summarized_articles = []
        
        for i, article in enumerate(articles):
            print(f"Summarizing article {i+1}/{len(articles)}...")
            
            summary = self.summarize_article(
                article.get('title', ''),
                article.get('content', ''),
                max_length
            )
            
            # Add summary to article data
            article_with_summary = article.copy()
            article_with_summary['summary'] = summary
            summarized_articles.append(article_with_summary)
            
            # Rate limiting
            if delay > 0 and i < len(articles) - 1:
                time.sleep(delay)
        
        return summarized_articles

# Example usage
if __name__ == "__main__":
    # You'll need to set OPENAI_API_KEY in your .env file
    summarizer = AISummarizer()
    
    # Test with sample article
    test_article = {
        'title': 'OpenAI представляет агента ChatGPT',
        'content': 'OpenAI объявила о новом агенте ChatGPT, который может автономно использовать вашу электронную почту и веб-приложения для выполнения задач. Это значительный шаг вперед в области автоматизации ИИ...'
    }
    
    summary = summarizer.summarize_article(
        test_article['title'],
        test_article['content']
    )
    
    print(f"Summary: {summary}") 