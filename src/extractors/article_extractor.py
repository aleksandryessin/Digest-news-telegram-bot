import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urlparse

class ArticleExtractor:
    """Extract article content and metadata from news URLs."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_article(self, url, source=None):
        """
        Extract article title, content, and metadata from URL.
        
        Args:
            url (str): Article URL
            source (str): Source name (for custom parsing rules)
            
        Returns:
            dict: Article data with title, content, summary, etc.
        """
        try:
            # Add delay to be respectful
            time.sleep(1)
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract based on source-specific rules
            if source:
                article_data = self._extract_by_source(soup, url, source.lower())
            else:
                article_data = self._extract_generic(soup, url)
            
            return article_data
            
        except Exception as e:
            print(f"Error extracting article from {url}: {e}")
            return {
                'url': url,
                'title': self._fallback_title_from_url(url),
                'content': '',
                'excerpt': '',
                'error': str(e)
            }
    
    def _extract_by_source(self, soup, url, source):
        """Extract using source-specific selectors."""
        
        extractors = {
            'techcrunch': self._extract_techcrunch,
            'wired': self._extract_wired,
            'the verge': self._extract_verge,
            'venturebeat': self._extract_venturebeat,
            'mit tech review': self._extract_mit_tech_review,
            'ars technica': self._extract_ars_technica,
            'zdnet': self._extract_zdnet,
            'forbes': self._extract_forbes,
            'bloomberg': self._extract_bloomberg,
        }
        
        extractor = extractors.get(source, self._extract_generic)
        return extractor(soup, url)
    
    def _extract_techcrunch(self, soup, url):
        """Extract TechCrunch article."""
        title = self._get_title(soup, [
            'h1.article__title',
            'h1[data-module="ArticleTitle"]',
            'h1.wp-block-post-title'
        ])
        
        content = self._get_content(soup, [
            '.article-content',
            '.entry-content',
            '.wp-block-post-content'
        ])
        
        return self._build_article_data(url, title, content)
    
    def _extract_wired(self, soup, url):
        """Extract Wired article."""
        title = self._get_title(soup, [
            'h1[data-testid="ContentHeaderHed"]',
            'h1.ContentHeaderHed',
            'h1.article-title'
        ])
        
        content = self._get_content(soup, [
            '[data-testid="BodyWrapper"]',
            '.ArticleBodyWrapper',
            '.content'
        ])
        
        return self._build_article_data(url, title, content)
    
    def _extract_verge(self, soup, url):
        """Extract The Verge article."""
        title = self._get_title(soup, [
            'h1[data-testid="headline"]',
            'h1.c-page-title',
            'h1.entry-title'
        ])
        
        content = self._get_content(soup, [
            '.c-entry-content',
            '.l-wrapper',
            '.entry-content'
        ])
        
        return self._build_article_data(url, title, content)
    
    def _extract_venturebeat(self, soup, url):
        """Extract VentureBeat article."""
        title = self._get_title(soup, [
            'h1.article-title',
            'h1.entry-title',
            'h1'
        ])
        
        content = self._get_content(soup, [
            '.article-content',
            '.entry-content',
            '.post-content'
        ])
        
        return self._build_article_data(url, title, content)
    
    def _extract_mit_tech_review(self, soup, url):
        """Extract MIT Technology Review article."""
        title = self._get_title(soup, [
            'h1.article-header__title',
            'h1.story-header__title',
            'h1'
        ])
        
        content = self._get_content(soup, [
            '.article-body',
            '.story-body',
            '.content'
        ])
        
        return self._build_article_data(url, title, content)
    
    def _extract_ars_technica(self, soup, url):
        """Extract Ars Technica article."""
        title = self._get_title(soup, [
            'h1[itemprop="headline"]',
            'h1.article-title',
            'h1'
        ])
        
        content = self._get_content(soup, [
            '.article-content',
            '[itemprop="articleBody"]',
            '.post-content'
        ])
        
        return self._build_article_data(url, title, content)
    
    def _extract_zdnet(self, soup, url):
        """Extract ZDNet article."""
        title = self._get_title(soup, [
            'h1.article-title',
            'h1',
            '.headline'
        ])
        
        content = self._get_content(soup, [
            '.article-body',
            '.content',
            '.storyBody'
        ])
        
        return self._build_article_data(url, title, content)
    
    def _extract_forbes(self, soup, url):
        """Extract Forbes article."""
        title = self._get_title(soup, [
            'h1[data-testid="article-headline"]',
            'h1.article-headline',
            'h1'
        ])
        
        content = self._get_content(soup, [
            '[data-testid="article-body"]',
            '.article-body',
            '.body'
        ])
        
        return self._build_article_data(url, title, content)
    
    def _extract_bloomberg(self, soup, url):
        """Extract Bloomberg article."""
        title = self._get_title(soup, [
            'h1[data-module="ArticleHeader"]',
            'h1.headline',
            'h1'
        ])
        
        content = self._get_content(soup, [
            '[data-module="ArticleBody"]',
            '.article-body',
            '.story-body'
        ])
        
        return self._build_article_data(url, title, content)
    
    def _extract_generic(self, soup, url):
        """Generic extraction for unknown sources."""
        # Try common selectors
        title = self._get_title(soup, [
            'h1',
            'title',
            '.title',
            '.headline',
            '[data-testid="headline"]'
        ])
        
        content = self._get_content(soup, [
            'article',
            '.article',
            '.content',
            '.post-content',
            '.entry-content',
            '.article-content',
            'main'
        ])
        
        return self._build_article_data(url, title, content)
    
    def _get_title(self, soup, selectors):
        """Try multiple selectors to find title."""
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        return "Title not found"
    
    def _get_content(self, soup, selectors):
        """Try multiple selectors to find content."""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # Clean up the content
                text = element.get_text(separator=' ', strip=True)
                # Remove extra whitespace
                text = re.sub(r'\s+', ' ', text)
                if len(text) > 100:  # Ensure we have substantial content
                    return text
        
        return "Content not found"
    
    def _build_article_data(self, url, title, content):
        """Build standardized article data structure."""
        # Create excerpt (first 200 characters)
        excerpt = content[:200] + "..." if len(content) > 200 else content
        
        return {
            'url': url,
            'title': title,
            'content': content,
            'excerpt': excerpt,
            'word_count': len(content.split()),
            'domain': urlparse(url).netloc
        }
    
    def _fallback_title_from_url(self, url):
        """Extract title from URL as fallback."""
        try:
            path = urlparse(url).path
            # Get last part of path
            title_part = path.split('/')[-1] if not path.endswith('/') else path.split('/')[-2]
            # Clean up
            title = title_part.replace('-', ' ').replace('_', ' ')
            return title.title()
        except:
            return "Article"

# Example usage
if __name__ == "__main__":
    extractor = ArticleExtractor()
    
    # Test with a sample URL
    test_url = "https://techcrunch.com/2025/01/28/chatgpt-everything-to-know-about-the-ai-chatbot/"
    article = extractor.extract_article(test_url, "TechCrunch")
    
    print(f"Title: {article['title']}")
    print(f"Content: {article['content'][:500]}...")
    print(f"Word count: {article['word_count']}") 