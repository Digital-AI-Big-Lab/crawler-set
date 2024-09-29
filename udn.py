import requests
from bs4 import BeautifulSoup
import time
import json
from typing import Optional, List, Dict

class UDN:
    """
    Crawler for UDN news articles.

    Attributes
    ----------
    page : int
        Number of articles to scrape.
    start_url : str
        Base URL of the news section.
    start_id : int
        ID of the latest article to start scraping from.
    article_list : List[Dict]
        List to store scraped articles.
    """
    
    def __init__(self, page: int, start_url: str, start_id: int) -> None:
        """
        Initialize the UDN Crawler.

        Parameters
        ----------
        page : int
            Number of articles to scrape.
        start_url : str
            Base URL for scraping.
        start_id : int
            ID of the latest article to start scraping from.
        """
        self.page = page
        self.start_url = start_url
        self.start_id = start_id
        self.article_list: List[Dict] = []

    def fetch_data(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch webpage content using BeautifulSoup.

        Parameters
        ----------
        url : str
            URL of the article to fetch.

        Returns
        -------
        Optional[BeautifulSoup]
            Parsed HTML page as BeautifulSoup object, or None if request fails.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None

    def get_content(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the main content of the article, excluding <a> tags.

        Parameters
        ----------
        soup : BeautifulSoup
            Parsed HTML page.

        Returns
        -------
        Optional[str]
            The main content of the article, or None if not found.
        """
        content_tag = soup.find("section", class_="article-content__editor")
        
        if not content_tag:
            return None

        # Find all paragraph tags but skip the <a> tag content
        contents = content_tag.findAll('p', class_=None)
        
        if contents:
            result = []
            for content in contents:
                # Remove all <a> tags within the paragraph
                for a_tag in content.findAll('a'):
                    a_tag.decompose()  # This removes the <a> tag from the content

                # Append the remaining text to the result list
                result.append(content.get_text(strip=True))

            return " ".join(result)

        return None

    def get_datetime(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the publication date of the article.

        Parameters
        ----------
        soup : BeautifulSoup
            Parsed HTML page.

        Returns
        -------
        Optional[str]
            The publication date in "YYYY-MM-DD" format, or None if not found.
        """
        datetime_tag = soup.find(class_='article-content__time')
        return datetime_tag.text.split(" ")[0] if datetime_tag else None

    def get_category(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the category of the article.

        Parameters
        ----------
        soup : BeautifulSoup
            Parsed HTML page.

        Returns
        -------
        Optional[str]
            The category of the article, or None if not found.
        """
        category_tag = soup.find('meta', {'property': 'article:section'})
        return category_tag['content'] if category_tag else None

    def get_subtitle(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the subtitle of the article (e.g., financial news).

        Parameters
        ----------
        soup : BeautifulSoup
            Parsed HTML page.

        Returns
        -------
        Optional[str]
            The subtitle of the article, or None if not found.
        """
        subtitle_tag = soup.find('a', class_='breadcrumb-items', href=False)
        return subtitle_tag.text.strip() if subtitle_tag else None

    def get_title(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the title of the article.

        Parameters
        ----------
        soup : BeautifulSoup
            Parsed HTML page.

        Returns
        -------
        Optional[str]
            The title of the article, or None if not found.
        """
        title_tag = soup.find('h1')
        return title_tag.text.strip() if title_tag else None

    def get_info(self) -> List[Dict]:
        """
        Loop through articles and extract relevant information.

        Returns
        -------
        List[Dict]
            List of dictionaries containing article information.
        """
        for i in range(self.start_id - self.page, self.start_id):
            article_url = self.start_url + str(i)
            soup = self.fetch_data(article_url)

            if soup:
                category = self.get_category(soup)
                title = self.get_title(soup)
                datetime = self.get_datetime(soup)
                link = article_url
                content = self.get_content(soup)
                subtitle = self.get_subtitle(soup)
                
                if not title or not content:
                    print(f"Skipping article ID {i} due to missing title or content.")
                    continue  # Skip articles with missing title or content
                    
                article_content = {
                    "category": category,
                    "subtitle": subtitle,
                    "title": title,
                    "datetime": datetime,
                    "link": link,
                    "content": content,
                }

                self.article_list.append(article_content)
            time.sleep(0.1)  # Add delay to prevent overloading the server

        return self.article_list

# Example usage
if __name__ == "__main__":
    udn = UDN(30, "https://udn.com/news/story/124222/", 8243941)  # Scrape 10 articles
    articles = udn.get_info()
    # Print results as formatted JSON
    with open('udn.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
