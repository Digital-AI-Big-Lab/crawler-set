import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Optional

class FSC:
    """Crawler for scraping announcements on the Financial Supervisory Commission website."""
    
    def __init__(self, urls: Dict[str, str], max_pages: Optional[int] = None):
        """
        Initialize the FSC Crawler.
        
        Parameters
        ----------
        urls : Dict[str, str]
            Dictionary containing URL and corresponding category.
        max_pages : Optional[int], optional
            Max pages to scrape, by default None (scrape all pages).
        """
        self.urls = urls
        self.base_url = "https://www.fsc.gov.tw/ch/"
        self.max_pages = max_pages

    def fetch_data(self, url: str, page: Optional[int] = None) -> Optional[BeautifulSoup]:
        """
        Fetch webpage content using BeautifulSoup.
        
        Parameters
        ----------
        url : str
            URL for scraping.
        page : Optional[int], optional
            Page number for scraping, by default None.
        
        Returns
        -------
        Optional[BeautifulSoup]
            Parsed HTML page as BeautifulSoup object, or None if request fails.
        """
        try:
            if page:
                url += f"&page={page}"  # Append page number to the URL
            
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for bad status
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None

    def extract_content(self, soup: BeautifulSoup) -> str:
        """
        Extract main content from the article page.
        
        Parameters
        ----------
        soup : BeautifulSoup
            Parsed HTML page.
        
        Returns
        -------
        str
            Main content or "無內文" if no content is found.
        """
        content_tag = soup.find('div', class_='page-edit')
        return content_tag.get_text(strip=True) if content_tag else '無內文'

    def get_article_details(self, soup: BeautifulSoup, category: str) -> List[Dict[str, Optional[str]]]:
        """
        Extract article details from the page.
        
        Parameters
        ----------
        soup : BeautifulSoup
            Parsed HTML page.
        category : str
            The category from the URL's dictionary key.
        
        Returns
        -------
        List[Dict[str, Optional[str]]]
            List of dictionaries containing article details.
        """
        articles = []
        rows = soup.find_all('li', role='row')
        
        if not rows:
            print(f"No articles found for {category}.")
            return articles

        print(f"Found {len(rows)} articles in {category}.")

        for row in rows:
            source = row.find('span', class_='unit').get_text(strip=True) if row.find('span', class_='unit') else '未分類'
            title_tag = row.find('a')
            title = title_tag['title'] if title_tag else '無標題'
            link = self.base_url + title_tag['href'] if title_tag else None
            datetime = row.find('span', class_='date').get_text(strip=True) if row.find('span', class_='date') else '未知日期'

            # Fetch article content if link is valid
            content = '無內文'
            if link:
                article_soup = self.fetch_data(link)
                content = self.extract_content(article_soup) if article_soup else '無內文'

            if title != '無標題':
                article = {
                    "category": category,
                    "source": source,
                    "title": title,
                    "datetime": datetime if datetime != '未知日期' else None,
                    "link": link,
                    "content": content if content != '無內文' else None
                }
                articles.append(article)

        return articles

    def scrape_all(self) -> List[Dict[str, Optional[str]]]:
        """
        Scrape all articles from the given URLs.
        
        Returns
        -------
        List[Dict[str, Optional[str]]]
            List of all scraped articles.
        """
        all_articles = []
        for category, url in self.urls.items():
            page = 1
            total_pages = self.max_pages if self.max_pages else float('inf')

            while page <= total_pages:
                soup = self.fetch_data(url, page)
                if not soup:
                    print(f"Failed to retrieve page {page} for {category}.")
                    break

                articles = self.get_article_details(soup, category)
                all_articles.extend(articles)

                if len(articles) == 0:
                    print(f"No more articles found for {category} on page {page}.")
                    break

                page += 1

        return all_articles
    
if __name__ == "__main__":

    # URLs and categories
    urls = {
        "重要公告": "https://www.fsc.gov.tw/ch/home.jsp?id=97&parentpath=0%2C2",
        "新聞稿": "https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0%2C2",
        "即時新聞澄清": "https://www.fsc.gov.tw/ch/home.jsp?id=609&parentpath=0,2&mcustomize=disputearea_list.jsp"
    }
    # User input for max pages
    max_pages_input = input("請輸入要爬取的最大頁數（或按 Enter 繼續抓取所有頁面）：")
    max_pages = int(max_pages_input) if max_pages_input.isdigit() else None

    # Initialize and run the scraper
    scraper = FSC(urls, max_pages)
    all_articles = scraper.scrape_all()

    # Save results to JSON file
    with open('fsc_articles.json', 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    print("爬取完成，結果已保存到 fsc_articles.json")
