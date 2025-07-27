from extract_links import extract_links
import urllib.request
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
import time

def calculate_relevance_score(article_url, title=""):
    """
    Calculate relevance score for an AI article based on keywords and other factors.
    Enhanced to work with multiple sources.
    
    Args:
        article_url (str): URL of the article
        title (str): Article title if available
        
    Returns:
        tuple: (score, breakdown) where breakdown shows how score was calculated
    """
    score = 0
    breakdown = {}
    
    # Combine URL and title for analysis
    content_to_analyze = (article_url + " " + title).lower()
    
    # High-value AI keywords (worth more points)
    high_value_keywords = {
        'openai': 20, 'chatgpt': 20, 'gpt': 15, 'claude': 15,
        'gemini': 15, 'llm': 12, 'transformer': 12, 'neural': 10,
        'breakthrough': 15, 'launch': 10, 'release': 8, 'announces': 8
    }
    
    # Medium-value AI keywords
    medium_value_keywords = {
        'artificial-intelligence': 10, 'machine-learning': 10, 'deep-learning': 10,
        'automation': 8, 'robot': 8, 'algorithm': 6, 'data': 4,
        'startup': 5, 'funding': 6, 'investment': 6, 'acquisition': 8
    }
    
    # AI company names (high relevance)
    ai_companies = {
        'google': 10, 'microsoft': 10, 'amazon': 8, 'meta': 8, 'facebook': 8,
        'nvidia': 12, 'anthropic': 15, 'mistral': 12, 'huggingface': 10,
        'tesla': 8, 'apple': 8, 'samsung': 6, 'intel': 6
    }
    
    # Technology/research terms
    tech_terms = {
        'model': 4, 'training': 5, 'dataset': 4, 'performance': 4,
        'research': 5, 'paper': 4, 'study': 4, 'experiment': 4
    }
    
    # Check for high-value keywords
    for keyword, points in high_value_keywords.items():
        if keyword in content_to_analyze:
            score += points
            breakdown[f"High-value: {keyword}"] = points
    
    # Check for medium-value keywords
    for keyword, points in medium_value_keywords.items():
        if keyword in content_to_analyze:
            score += points
            breakdown[f"Medium-value: {keyword}"] = points
    
    # Check for AI company mentions
    for company, points in ai_companies.items():
        if company in content_to_analyze:
            score += points
            breakdown[f"Company: {company}"] = points
    
    # Check for tech terms
    for term, points in tech_terms.items():
        if term in content_to_analyze:
            score += points
            breakdown[f"Tech: {term}"] = points
    
    # Recency bonus (try to extract date from URL or estimate)
    current_year = datetime.now().year
    if str(current_year) in article_url:
        recency_bonus = 8
        score += recency_bonus
        breakdown[f"Current year"] = recency_bonus
    elif str(current_year - 1) in article_url:
        recency_bonus = 4
        score += recency_bonus
        breakdown[f"Recent year"] = recency_bonus
    
    # Source quality bonus
    domain = urlparse(article_url).netloc.lower()
    source_bonus = {
        'techcrunch.com': 8,
        'wired.com': 10,
        'theverge.com': 8,
        'venturebeat.com': 7,
        'technologyreview.com': 12,
        'arstechnica.com': 9,
        'zdnet.com': 6,
        'forbes.com': 7,
        'bloomberg.com': 10
    }
    
    for source, bonus in source_bonus.items():
        if source in domain:
            score += bonus
            breakdown[f"Source: {source}"] = bonus
            break
    
    # Base AI relevance
    base_ai_score = 5
    score += base_ai_score
    breakdown["Base AI relevance"] = base_ai_score
    
    return score, breakdown

def extract_techcrunch_ai():
    """Extract AI articles from TechCrunch."""
    try:
        req = urllib.request.Request(
            'https://techcrunch.com/tag/ai/',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        all_links = extract_links(html_content)
        article_links = [link for link in all_links if re.search(r'/202[4-5]/', link)]
        
        # Convert relative URLs to absolute
        articles = []
        for link in set(article_links):
            if link.startswith('/'):
                full_url = f"https://techcrunch.com{link}"
            else:
                full_url = link
            articles.append(('TechCrunch', full_url, ""))
        
        return articles
    except Exception as e:
        print(f"Error fetching TechCrunch: {e}")
        return []

def extract_wired_ai():
    """Extract AI articles from Wired."""
    try:
        req = urllib.request.Request(
            'https://www.wired.com/tag/artificial-intelligence/',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        all_links = extract_links(html_content)
        # Filter for story links
        article_links = [link for link in all_links if '/story/' in link or '/gallery/' in link]
        
        articles = []
        for link in set(article_links):
            if link.startswith('/'):
                full_url = f"https://www.wired.com{link}"
            elif link.startswith('https://www.wired.com'):
                full_url = link
            else:
                continue
            articles.append(('Wired', full_url, ""))
        
        return articles
    except Exception as e:
        print(f"Error fetching Wired: {e}")
        return []

def extract_verge_ai():
    """Extract AI articles from The Verge."""
    try:
        req = urllib.request.Request(
            'https://www.theverge.com/ai-artificial-intelligence',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        all_links = extract_links(html_content)
        # Filter for article links (usually contain year)
        article_links = [link for link in all_links if re.search(r'/202[4-5]/', link)]
        
        articles = []
        for link in set(article_links):
            if link.startswith('/'):
                full_url = f"https://www.theverge.com{link}"
            elif link.startswith('https://www.theverge.com'):
                full_url = link
            else:
                continue
            articles.append(('The Verge', full_url, ""))
        
        return articles
    except Exception as e:
        print(f"Error fetching The Verge: {e}")
        return []

def extract_venturebeat_ai():
    """Extract AI articles from VentureBeat."""
    try:
        req = urllib.request.Request(
            'https://venturebeat.com/ai/',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        all_links = extract_links(html_content)
        # Filter for article links
        article_links = [link for link in all_links if 'venturebeat.com' in link and '/ai/' in link]
        
        articles = []
        for link in set(article_links):
            if link.startswith('https://venturebeat.com'):
                articles.append(('VentureBeat', link, ""))
        
        return articles
    except Exception as e:
        print(f"Error fetching VentureBeat: {e}")
        return []

def extract_mit_tech_review_ai():
    """Extract AI articles from MIT Technology Review."""
    try:
        req = urllib.request.Request(
            'https://www.technologyreview.com/topic/artificial-intelligence/',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        all_links = extract_links(html_content)
        # Filter for article links
        article_links = [link for link in all_links if 'technologyreview.com' in link and '/202' in link]
        
        articles = []
        for link in set(article_links):
            if link.startswith('https://www.technologyreview.com'):
                articles.append(('MIT Tech Review', link, ""))
        
        return articles
    except Exception as e:
        print(f"Error fetching MIT Tech Review: {e}")
        return []

def extract_ars_technica_ai():
    """Extract AI articles from Ars Technica."""
    try:
        req = urllib.request.Request(
            'https://arstechnica.com/information-technology/artificial-intelligence/',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        all_links = extract_links(html_content)
        # Filter for article links
        article_links = [link for link in all_links if 'arstechnica.com' in link and '/202' in link]
        
        articles = []
        for link in set(article_links):
            if link.startswith('https://arstechnica.com'):
                articles.append(('Ars Technica', link, ""))
        
        return articles
    except Exception as e:
        print(f"Error fetching Ars Technica: {e}")
        return []

def extract_zdnet_ai():
    """Extract AI articles from ZDNet."""
    try:
        req = urllib.request.Request(
            'https://www.zdnet.com/topic/artificial-intelligence/',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        all_links = extract_links(html_content)
        # Filter for article links
        article_links = [link for link in all_links if 'zdnet.com' in link and ('/article/' in link or '/story/' in link)]
        
        articles = []
        for link in set(article_links):
            if link.startswith('https://www.zdnet.com'):
                articles.append(('ZDNet', link, ""))
        
        return articles
    except Exception as e:
        print(f"Error fetching ZDNet: {e}")
        return []

def extract_forbes_ai():
    """Extract AI articles from Forbes."""
    try:
        req = urllib.request.Request(
            'https://www.forbes.com/ai/',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        all_links = extract_links(html_content)
        # Filter for article links
        article_links = [link for link in all_links if 'forbes.com' in link and '/sites/' in link]
        
        articles = []
        for link in set(article_links):
            if link.startswith('https://www.forbes.com'):
                articles.append(('Forbes', link, ""))
        
        return articles
    except Exception as e:
        print(f"Error fetching Forbes: {e}")
        return []

def extract_bloomberg_ai():
    """Extract AI articles from Bloomberg."""
    try:
        req = urllib.request.Request(
            'https://www.bloomberg.com/topics/artificial-intelligence',
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
        
        all_links = extract_links(html_content)
        # Filter for article links
        article_links = [link for link in all_links if 'bloomberg.com' in link and '/news/' in link]
        
        articles = []
        for link in set(article_links):
            if link.startswith('https://www.bloomberg.com'):
                articles.append(('Bloomberg', link, ""))
        
        return articles
    except Exception as e:
        print(f"Error fetching Bloomberg: {e}")
        return []

def fetch_all_ai_sources():
    """Fetch articles from all AI news sources."""
    print("🔄 Fetching articles from all sources...")
    
    all_articles = []
    
    sources = [
        ("TechCrunch", extract_techcrunch_ai),
        ("Wired", extract_wired_ai),
        ("The Verge", extract_verge_ai),
        ("VentureBeat", extract_venturebeat_ai),
        ("MIT Tech Review", extract_mit_tech_review_ai),
        ("Ars Technica", extract_ars_technica_ai),
        ("ZDNet", extract_zdnet_ai),
        ("Forbes", extract_forbes_ai),
        ("Bloomberg", extract_bloomberg_ai),
    ]
    
    for source_name, extract_func in sources:
        print(f"  📰 Fetching from {source_name}...")
        try:
            articles = extract_func()
            all_articles.extend(articles)
            print(f"    ✅ Found {len(articles)} articles")
            time.sleep(1)  # Be polite to servers
        except Exception as e:
            print(f"    ❌ Failed: {e}")
    
    return all_articles

def create_comprehensive_ai_digest(top_n=15):
    """
    Create a comprehensive AI news digest from multiple sources.
    """
    print("🤖 COMPREHENSIVE AI NEWS DIGEST")
    print("=" * 80)
    
    # Fetch articles from all sources
    all_articles = fetch_all_ai_sources()
    
    if not all_articles:
        print("❌ No articles found from any source")
        return []
    
    print(f"\n📊 Total articles collected: {len(all_articles)}")
    
    # Calculate relevance scores for all articles
    print("🔍 Calculating relevance scores...")
    scored_articles = []
    
    for source, url, title in all_articles:
        score, breakdown = calculate_relevance_score(url, title)
        scored_articles.append((source, url, title, score, breakdown))
    
    # Sort by score and get top N
    top_articles = sorted(scored_articles, key=lambda x: x[3], reverse=True)[:top_n]
    
    # Display results
    print(f"\n🏆 TOP {len(top_articles)} MOST RELEVANT AI ARTICLES")
    print("=" * 80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Sources: TechCrunch, Wired, The Verge, VentureBeat, MIT Tech Review, Ars Technica, ZDNet, Forbes, Bloomberg")
    print("=" * 80)
    
    for i, (source, url, title, score, breakdown) in enumerate(top_articles, 1):
        # Extract title from URL if not provided
        if not title:
            title_part = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
            title = title_part.replace('-', ' ').title()
        
        print(f"#{i} | Score: {score} | [{source}]")
        print(f"    📰 {title}")
        print(f"    🔗 {url}")
        
        # Show top 3 relevance factors
        if breakdown:
            top_factors = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)[:3]
            factors_str = ", ".join([f"{k}: +{v}" for k, v in top_factors])
            print(f"    📊 Top factors: {factors_str}")
        print()
    
    return top_articles

def save_comprehensive_digest(filename="comprehensive_ai_digest.txt", top_n=15):
    """Save comprehensive digest to file."""
    try:
        # Fetch and score articles
        all_articles = fetch_all_ai_sources()
        
        if not all_articles:
            print("❌ No articles to save")
            return
        
        scored_articles = []
        for source, url, title in all_articles:
            score, breakdown = calculate_relevance_score(url, title)
            scored_articles.append((source, url, title, score, breakdown))
        
        top_articles = sorted(scored_articles, key=lambda x: x[3], reverse=True)[:top_n]
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("🤖 COMPREHENSIVE AI NEWS DIGEST\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Total Articles Analyzed: {len(all_articles)}\n")
            f.write(f"Top {len(top_articles)} Most Relevant Selected\n")
            f.write(f"Sources: TechCrunch, Wired, The Verge, VentureBeat, MIT Tech Review, Ars Technica, ZDNet, Forbes, Bloomberg\n")
            f.write("=" * 80 + "\n\n")
            
            for i, (source, url, title, score, breakdown) in enumerate(top_articles, 1):
                if not title:
                    title_part = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
                    title = title_part.replace('-', ' ').title()
                
                f.write(f"#{i} | Score: {score} | [{source}]\n")
                f.write(f"    📰 {title}\n")
                f.write(f"    🔗 {url}\n")
                
                if breakdown:
                    top_factors = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)[:3]
                    factors_str = ", ".join([f"{k}: +{v}" for k, v in top_factors])
                    f.write(f"    📊 Top factors: {factors_str}\n")
                f.write("\n")
        
        print(f"✅ Comprehensive digest saved to {filename}")
        
    except Exception as e:
        print(f"Error saving comprehensive digest: {e}")

if __name__ == "__main__":
    # Create comprehensive digest
    articles = create_comprehensive_ai_digest(top_n=15)
    
    if articles:
        print("\n" + "="*80)
        save_comprehensive_digest(top_n=15) 