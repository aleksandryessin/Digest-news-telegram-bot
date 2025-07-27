# 🤖 AI News Digest System

A comprehensive AI news aggregation system that fetches, analyzes, and ranks the most relevant AI articles from 8 major tech news sources.

## 🎯 What It Does

This system automatically:
1. **Fetches** articles from 8 major AI news sources
2. **Analyzes** hundreds of articles for relevance using intelligent scoring
3. **Ranks** them based on keywords, companies, recency, and source quality
4. **Selects** the top 15 most relevant articles globally
5. **Displays** results with transparency (shows why each article scored highly)
6. **Saves** to a clean digest file for easy consumption

## 📊 News Sources

- **TechCrunch AI** - Latest AI startup and technology news
- **Wired AI** - In-depth AI analysis and features  
- **The Verge AI** - Consumer-focused AI technology coverage
- **VentureBeat AI** - Enterprise and business AI news
- **MIT Technology Review** - Academic and research AI developments
- **Ars Technica AI** - Technical AI analysis and reviews
- **ZDNet AI** - Business technology and AI implementation
- **Forbes AI** - Business and investment AI coverage
- **Bloomberg AI** - Financial and market AI news

## 📁 Project Structure

```
news digest/
├── extract_links.py              # Core link extraction function
├── filter_links.py               # Link filtering utilities  
├── multi_source_ai_digest.py     # 🎯 MAIN SYSTEM (run this!)
├── requirements.txt              # Dependencies
├── comprehensive_ai_digest.txt   # Latest output
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- No external dependencies needed (uses only built-in Python libraries)

### Run the System
```bash
python3 multi_source_ai_digest.py
```

### Sample Output
```
🤖 COMPREHENSIVE AI NEWS DIGEST
================================================================================
🔄 Fetching articles from all sources...
  📰 Fetching from TechCrunch...
    ✅ Found 39 articles
  📰 Fetching from Wired...
    ✅ Found 27 articles
  [... more sources ...]

📊 Total articles collected: 261
🔍 Calculating relevance scores...

🏆 TOP 15 MOST RELEVANT AI ARTICLES
================================================================================
#1 | Score: 75 | [Forbes]
    📰 Google may launch low-cost AI plan to rival ChatGPT
    🔗 https://www.forbes.com/sites/paulmonckton/2025/07/26/google-may-launch-low-cost-ai-plan-to-rival-chatgpt/
    📊 Top factors: High-value: chatgpt: +20, High-value: gpt: +15, High-value: launch: +10

#2 | Score: 71 | [VentureBeat]
    📰 ChatGPT router that automatically selects the right OpenAI model
    🔗 https://venturebeat.com/ai/a-chatgpt-router-that-automatically-selects-the-right-openai-model/
    📊 Top factors: High-value: openai: +20, High-value: chatgpt: +20, High-value: gpt: +15
```

## 🧠 Relevance Scoring System

The system uses a sophisticated scoring algorithm based on:

### High-Value Keywords (15-20 points)
- `openai`, `chatgpt`, `gpt`, `claude`, `gemini`
- `breakthrough`, `launch`, `release`, `announces`

### AI Companies (6-15 points)  
- `google`, `microsoft`, `nvidia`, `anthropic`, `meta`
- `tesla`, `apple`, `amazon`, `mistral`

### Technical Terms (4-10 points)
- `artificial-intelligence`, `machine-learning`, `llm`
- `automation`, `robot`, `algorithm`, `neural`

### Source Quality Bonus (6-12 points)
- MIT Tech Review: +12, Wired: +10, Bloomberg: +10
- Ars Technica: +9, TechCrunch: +8, The Verge: +8

### Recency Bonus (4-8 points)
- Current year articles get bonus points
- Recent articles ranked higher

## ⚙️ Customization

### Change Number of Articles
Edit `multi_source_ai_digest.py`:
```python
articles = create_comprehensive_ai_digest(top_n=15)  # Change 15 to any number
```

### Modify Scoring Keywords
Edit the keyword dictionaries in `calculate_relevance_score()` function:
```python
high_value_keywords = {
    'your_keyword': 20,  # Add your own high-value terms
    # ... existing keywords
}
```

## 📄 File Descriptions

### Core Files
- **`multi_source_ai_digest.py`** - Main system that fetches from all sources and ranks articles
- **`extract_links.py`** - Core HTML link extraction using regex
- **`filter_links.py`** - Utility functions for filtering links by substring, domain, etc.

### Output Files
- **`comprehensive_ai_digest.txt`** - Latest digest with top 15 articles and scoring breakdown

### Configuration
- **`requirements.txt`** - Dependencies (currently none - uses only Python built-ins)

## 🛠️ Development

### Running Individual Components
```bash
# Test link extraction
python3 extract_links.py

# Test link filtering
python3 filter_links.py

# Run full digest
python3 multi_source_ai_digest.py
```

### Adding New Sources
1. Create a new extraction function in `multi_source_ai_digest.py`
2. Add it to the `sources` list in `fetch_all_ai_sources()`
3. Update the source bonus scoring in `calculate_relevance_score()`

## 📋 Usage Patterns

### Daily News Digest
```bash
# Run every morning for fresh AI news
python3 multi_source_ai_digest.py
```

### Weekly Deep Dive
```bash
# Modify top_n=30 for weekly comprehensive overview
python3 multi_source_ai_digest.py
```

### Research Mode
```bash
# Use filter_links.py to find specific topics
python3 filter_links.py
```

## 🎯 Goals Achieved

- ✅ **Multi-source aggregation** from 8 major AI news sites
- ✅ **Intelligent relevance ranking** with transparent scoring
- ✅ **Automated daily digest** generation
- ✅ **Clean output format** for easy consumption
- ✅ **Zero external dependencies** - runs anywhere Python runs
- ✅ **Customizable scoring** for different AI interests

## 🚧 Known Limitations

- **Bloomberg**: May be blocked with 403 errors (paywall protection)
- **Rate Limiting**: 1-second delays between sources to be respectful
- **Dynamic Content**: Some sites use JavaScript loading (may miss some articles)
- **Language**: Currently optimized for English-language sources

## 🔄 Automation Ideas

### Cron Job (Daily at 8 AM)
```bash
0 8 * * * cd /path/to/news-digest && python3 multi_source_ai_digest.py
```

### GitHub Actions (Weekly)
Set up automated weekly digests and commit results to repository.

## 📈 Future Enhancements

- [ ] Email digest automation
- [ ] Sentiment analysis scoring
- [ ] Article summary generation  
- [ ] RSS feed output
- [ ] Web dashboard interface
- [ ] Historical trending analysis

---

**Built for AI enthusiasts who want to stay on top of the rapidly evolving AI landscape! 🚀** 