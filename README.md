
# Scrawler-Set

**Scrawler-Set** is a versatile web scraping framework designed to fetch article data from multiple sources such as UDN, TVBS, and FSC. The scraping results are output in a structured JSON format, with categories, titles, publication dates, content, and comments (if available). This set of scrapers is ideal for gathering public opinion, news, or articles for further analysis or storage.

## Features
1. **Multi-source scraping**: Supports UDN, TVBS, and FSC websites for structured article extraction.
2. **Customizable output**: Extracts and stores key information such as category, title, date, content, and comments.
3. **JSON Output**: Articles are output in JSON format for easy consumption by downstream applications.

### Scraping Flow
1. **URL fetching**: Each scraper fetches data from the specified website using the given base URL and article IDs.
2. **HTML parsing**: The page is parsed using `BeautifulSoup`, and relevant sections of the page are extracted.
3. **Content extraction**: Extracts the title, category, datetime, article content, and comments (if available).
4. **Optional controls**: You can set the number of articles to scrape and start from a specific article ID.
5. **Rate-limiting**: Ensures the server is not overloaded by introducing a delay between requests.

### Data Output
Each article is output in the following structure:

```python
{
    "category": category,      # Article category (e.g., news, financial)
    "title": title,            # Title of the article
    "datetime": YYYY-MM-DD,    # Publication date
    "link": link,              # URL of the article
    "content": content,        # Main article content
    "comments": comments       # User comments (optional)
}
```

---

## Scraper Modules

### 1. UDN Scraper
The UDN scraper extracts articles from UDN news. It fetches the article title, category, publication date, and the main content, ignoring any comments or advertisements present on the page.

**Example Usage:**
```python
udn = UDN(10, "https://udn.com/news/story/124222/", 8243941)
articles = udn.get_info()

with open('udn_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)
```
**Key Features:**
- Scrapes UDN articles by providing a starting article ID.
- Extracts main article body while filtering out unwanted tags like `<a>`.

### 2. TVBS Scraper
The TVBS scraper is built to extract financial articles from TVBS news. It fetches article titles, publication dates, categories, content, and comments (if any). The scraper also avoids extracting unnecessary text from advertisements.

**Example Usage:**
```python
tvbs = TVBS(100, "https://news.tvbs.com.tw/money/", 2628359)
articles = tvbs.get_info()

with open('tvbs_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)
```
**Key Features:**
- Uses `BeautifulSoup` to extract relevant sections of financial articles.
- Handles errors like missing titles or content by skipping such articles.

### 3. FSC Scraper
The FSC scraper extracts important announcements from the Financial Supervisory Commission's website. It fetches titles, publication dates, categories, and content for each announcement, and supports multi-page scraping.

**Example Usage:**
```python
urls = {
    "重要公告": "https://www.fsc.gov.tw/ch/home.jsp?id=97&parentpath=0%2C2",
    "新聞稿": "https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0%2C2"
}

fsc = FSC(urls, max_pages=5)
articles = fsc.scrape_all()

with open('fsc_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)
```
**Key Features:**
- Supports multi-page scraping with customizable page limits.
- Filters out irrelevant elements like internal links and advertisements.

---

## Installation
Ensure that you have the following Python packages installed:

```bash
pip install requests beautifulsoup4
```

## Usage
Each scraper can be used as a standalone class for its respective news source. Customize the scraping parameters (e.g., number of pages, article IDs) based on your needs.

---

## Future Improvements
- **Pagination Support**: Implement dynamic detection of total pages to scrape all available articles without manual input.
- **Improved Error Handling**: Better error reporting and retry logic for network failures.
- **Multi-threading**: For larger-scale scraping projects, implement multi-threading to speed up the scraping process.

---

## License
MIT License
