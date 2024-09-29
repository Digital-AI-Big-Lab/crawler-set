
# Scrawler-Set

**Scrawler-Set** 是一個多功能的網頁爬蟲框架，旨在從多個來源（如 UDN、TVBS 和 FSC）抓取文章數據。爬取結果將以結構化的 JSON 格式輸出，包含類別、標題、發布日期、內容以及評論（如有）。該爬蟲集非常適合用於收集輿情、新聞或文章以供進一步分析或存儲。

**Scrawler-Set** is a versatile web scraping framework designed to fetch article data from multiple sources such as UDN, TVBS, and FSC. The scraping results are output in a structured JSON format, with categories, titles, publication dates, content, and comments (if available). This set of scrapers is ideal for gathering public opinion, news, or articles for further analysis or storage.

## 特點 / Features
1. **多來源爬取**：支持從 UDN、TVBS 和 FSC 網站抓取結構化文章數據。
   **Multi-source scraping**: Supports UDN, TVBS, and FSC websites for structured article extraction.
2. **可定制的輸出**：提取並存儲關鍵信息，如類別、標題、日期、內容和評論。
   **Customizable output**: Extracts and stores key information such as category, title, date, content, and comments.
3. **JSON 輸出**：文章將以 JSON 格式輸出，便於下游應用使用。
   **JSON Output**: Articles are output in JSON format for easy consumption by downstream applications.

### 爬取流程 / Scraping Flow
1. **URL 抓取**：每個爬蟲根據提供的基礎 URL 和文章 ID 抓取數據。
   **URL fetching**: Each scraper fetches data from the specified website using the given base URL and article IDs.
2. **HTML 解析**：頁面將通過 `BeautifulSoup` 進行解析，並提取相關部分的內容。
   **HTML parsing**: The page is parsed using `BeautifulSoup`, and relevant sections of the page are extracted.
3. **內容提取**：提取標題、類別、日期時間、文章內容及評論（如有）。
   **Content extraction**: Extracts the title, category, datetime, article content, and comments (if available).
4. **可選控制**：您可以設置爬取文章的數量，並從特定文章 ID 開始。
   **Optional controls**: You can set the number of articles to scrape and start from a specific article ID.
5. **速率限制**：引入延遲以確保不會過度加載服務器。
   **Rate-limiting**: Ensures the server is not overloaded by introducing a delay between requests.

### 數據輸出格式 / Data Output
每篇文章將以以下結構輸出：  
Each article is output in the following structure:

```python
{
    "category": category,      # 文章類別 (例如: 新聞、財經)
    "title": title,            # 文章標題
    "datetime": YYYY-MM-DD,    # 發布日期
    "link": link,              # 文章 URL
    "content": content,        # 文章正文
    "comments": comments       # 用戶評論（可選）
}
```

---

## 爬蟲模塊 / Scraper Modules

### 1. UDN 爬蟲 / UDN Scraper
UDN 爬蟲從 UDN 新聞中提取文章。它提取文章標題、類別、發布日期以及主要內容，並忽略頁面上的任何評論或廣告。  
The UDN scraper extracts articles from UDN news. It fetches the article title, category, publication date, and the main content, ignoring any comments or advertisements present on the page.

**用法示例 / Example Usage:**
```python
udn = UDN(10, "https://udn.com/news/story/124222/", 8243941)
articles = udn.get_info()

with open('udn_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)
```
**主要特點 / Key Features:**
- 提供起始文章 ID，爬取 UDN 文章。  
  Scrapes UDN articles by providing a starting article ID.
- 提取主要文章正文，過濾掉無用的標籤如 `<a>`。  
  Extracts main article body while filtering out unwanted tags like `<a>`.

### 2. TVBS 爬蟲 / TVBS Scraper
TVBS 爬蟲設計用於提取 TVBS 新聞中的財經文章。它提取文章標題、發布日期、類別、內容及評論（如有）。該爬蟲還會避免提取廣告中的無用文本。  
The TVBS scraper is built to extract financial articles from TVBS news. It fetches article titles, publication dates, categories, content, and comments (if any). The scraper also avoids extracting unnecessary text from advertisements.

**用法示例 / Example Usage:**
```python
tvbs = TVBS(100, "https://news.tvbs.com.tw/money/", 2628359)
articles = tvbs.get_info()

with open('tvbs_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)
```
**主要特點 / Key Features:**
- 使用 `BeautifulSoup` 提取財經文章的相關部分。  
  Uses `BeautifulSoup` to extract relevant sections of financial articles.
- 處理缺少標題或內容的錯誤，並跳過這些文章。  
  Handles errors like missing titles or content by skipping such articles.

### 3. FSC 爬蟲 / FSC Scraper
FSC 爬蟲從金融監督管理委員會的網站上提取重要公告。它抓取每個公告的標題、發布日期、類別和內容，並支持多頁爬取。  
The FSC scraper extracts important announcements from the Financial Supervisory Commission's website. It fetches titles, publication dates, categories, and content for each announcement, and supports multi-page scraping.

**用法示例 / Example Usage:**
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
**主要特點 / Key Features:**
- 支持多頁爬取，並且可以自定義頁數限制。  
  Supports multi-page scraping with customizable page limits.
- 過濾掉無用的內部鏈接和廣告等元素。  
  Filters out irrelevant elements like internal links and advertisements.

---

## 安裝 / Installation
確保你已經安裝了以下 Python 套件：  
Ensure that you have the following Python packages installed:

```bash
pip install requests beautifulsoup4
```

## 使用 / Usage
每個爬蟲可以作為其各自新聞來源的獨立類來使用。根據需求自定義爬取參數（如頁數、文章 ID）。  
Each scraper can be used as a standalone class for its respective news source. Customize the scraping parameters (e.g., number of pages, article IDs) based on your needs.

---

## 未來改進 / Future Improvements
- **分頁支持**：實現動態檢測總頁數，以便在無需手動輸入的情況下爬取所有可用文章。  
  **Pagination Support**: Implement dynamic detection of total pages to scrape all available articles without manual input.
- **改進錯誤處理**：改進錯誤報告和網絡故障的重試邏輯。  
  **Improved Error Handling**: Better error reporting and retry logic for network failures.
- **多線程支持**：對於大規模爬取項目，實現多線程以加快爬取過程。  
  **Multi-threading**: For larger-scale scraping projects, implement multi-threading to speed up the scraping process.

---

## 許可證 / License
MIT License
