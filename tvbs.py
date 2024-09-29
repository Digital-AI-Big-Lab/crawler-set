import requests
from bs4 import BeautifulSoup
import time
import json
import re
from typing import Optional, List, Dict


class TVBS:
    """
    Crawler for scraping articles from TVBS News.
    
    Attributes
    ----------
    page : int
        Number of articles to scrape.
    start_url : str
        Base URL to start scraping from.
    start_id : int
        The ID of the latest article to start scraping from.
    article_list : list
        A list to store all the scraped article information.
    """
    
    def __init__(self, page: int, start_url: str, start_id: int) -> None:
        """
        Initializes the TVBS crawler with the number of articles to scrape, start URL, and article ID.
        
        Parameters
        ----------
        page : int
            Number of articles to scrape.
        start_url : str
            The base URL for scraping.
        start_id : int
            The latest article ID to start scraping from.
        """
        self.page = page
        self.start_url = start_url
        self.start_id = start_id
        self.article_list = []

    def fetch_data(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch the data from a given URL and return a BeautifulSoup object.
        
        Parameters
        ----------
        url : str
            The URL of the article to fetch.
        
        Returns
        -------
        Optional[BeautifulSoup]
            Parsed BeautifulSoup object, or None if there's an error.
        """
        try:
            response = requests.get(url)
            response.encoding = 'utf-8'  # Set response encoding to UTF-8
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None

    def get_main_data(self, soup: BeautifulSoup) -> Optional[Dict]:
        """
        Extract and decode the main data of the article from the soup object.
        
        Parameters
        ----------
        soup : BeautifulSoup
            The BeautifulSoup object containing the HTML content.
        
        Returns
        -------
        Optional[Dict]
            The decoded JSON data containing the article's details, or None if decoding fails.
        """
        script_tag = soup.find('script', type="application/ld+json")
        if script_tag:
            try:
                # Clean any invalid control characters
                json_data = re.sub(r'[\x00-\x1f\x7f]', '', script_tag.string)
                main_data = json.loads(json_data)
                return main_data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from script: {e}")
                return None
        return None

    def get_title(self, main_data: Dict) -> str:
        """
        Extract the article title from the main data.
        
        Parameters
        ----------
        main_data : dict
            The decoded data containing the article's details.
        
        Returns
        -------
        str
            The title of the article except garbage information, or a default message if the title is unavailable.
        """
        title = main_data.get("headline", "No title available")
        return title[:-8]

    def get_datetime(self, main_data: Dict) -> str:
        """
        Extract the publication date of the article.
        
        Parameters
        ----------
        main_data : dict
            The decoded data containing the article's details.
        
        Returns
        -------
        str
            The publication date in "YYYY-MM-DD" format, or a default message if unavailable.
        """
        full_datetime = main_data.get("datePublished", "No date available")
        return full_datetime[:10] if full_datetime != "No date available" else full_datetime

    def get_link(self, url: str) -> str:
        """
        Return the article URL.
        
        Parameters
        ----------
        url : str
            The URL of the article.
        
        Returns
        -------
        str
            The article URL.
        """
        return url

    def get_content(self, main_data: Dict) -> str:
        """
        Extract the main content of the article.
        
        Parameters
        ----------
        main_data : dict
            The decoded data containing the article's details.
        
        Returns
        -------
        str
            The main content of the article, or a default message if unavailable.
        """
        return main_data.get("articleBody", "No content available")[:-19]

    def get_info(self) -> List[Dict]:
        """
        Scrape article information including title, publication date, link, and content.
        
        Returns
        -------
        List[Dict]
            A list of dictionaries, each containing information for one article.
        """
        for i in range(self.start_id - self.page, self.start_id):
            article_url = self.start_url + str(i)
            soup = self.fetch_data(article_url)
            if soup:
                main_data = self.get_main_data(soup)
                if main_data:
                    # Extract necessary information
                    title = self.get_title(main_data)
                    datetime = self.get_datetime(main_data)
                    link = self.get_link(article_url)
                    content = self.get_content(main_data)

                    # Store article information
                    article_info = {
                        "title": title,
                        "datetime": datetime,
                        "link": link,
                        "content": content
                    }

                    self.article_list.append(article_info)
                else:
                    print(f"Failed to extract main data from {article_url}")
            else:
                print(f"Failed to fetch data from {article_url}")
            
            time.sleep(0.05)  # Add delay to prevent rate-limiting or server overload
        return self.article_list


# Example usage
tvbs = TVBS(10, "https://news.tvbs.com.tw/money/", 2628359)

# Write the scraped data to a JSON file
with open('tvbs.json', 'w', encoding='utf-8') as f:
    json.dump(tvbs.get_info(), f, ensure_ascii=False, indent=4)
