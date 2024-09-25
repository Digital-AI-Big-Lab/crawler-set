import requests
from bs4 import BeautifulSoup
import time

"""
1.需要的資料：分類("category")、標題("title")、日期("datetime")、連結("link")、內文("content")、留言("comments")
2.產出JSON格式：
    [
        article_content = {
            "category": category,
            "title": title,
            "datetime": YYYY-MM-DD",
            "link": link,
            "content": content,
            "comments": comments,
        },
        article_content = {
            ...
    ]
"""

class UDN:
    def __init__(self, page: int, start_url: str, start_id: int) -> None:
        """
        Initializes the UDN scraper class with the number of pages, the base URL, and the starting article ID.

        Parameters
        ----------
        page : int
            Number of articles to scrape.
        start_url : str
            Base URL of the target website.
        start_id : int
            Starting article ID for scraping.
        """
        self.page = page  # Number of articles to scrape
        self.start_url = start_url  # Base URL to fetch articles from
        self.start_id = start_id  # Starting article ID
        self.article_list = []  # List to store scraped articles

    def fetch_data(self, url: str):
        """
        Fetches the webpage data and returns the unprocessed BeautifulSoup object.

        Parameters
        ----------
        url : str
            The target URL of the webpage to scrape.

        Returns
        -------
        BeautifulSoup
            Returns the parsed HTML document in a BeautifulSoup object.
            Returns None in case of a request failure.
        """
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None

    def get_content(self, soup: BeautifulSoup):
        """
        Extracts the article's body content from the parsed webpage.

        Parameters
        ----------
        soup : BeautifulSoup
            The parsed HTML document.

        Returns
        -------
        list or None
            A list of strings representing the article's content if found.
            Returns None if no content is found.
        """
        contents = soup.findAll('p', class_=None)
        if contents:
            result = [content.text for content in contents]  # Using list comprehension to simplify the loop
            return result
        else:
            return None

    def get_datetime(self, soup: BeautifulSoup):
        """
        Extracts the publication date from the parsed webpage.

        Parameters
        ----------
        soup : BeautifulSoup
            The parsed HTML document.

        Returns
        -------
        str or None
            The article's publication date in the 'YYYY-MM-DD' format if found.
            Returns None if no date is found.
        """
        datetime_tag = soup.find(class_='article-content__time')
        return datetime_tag.text.split(" ")[0] if datetime_tag else None

    def get_info(self):
        """
        Loops through articles, fetches the data, and prints the publication date.

        Loops through a range of articles based on the starting ID and the number of pages. 
        Fetches each article's webpage, extracts the relevant information (like the date), 
        and prints it.

        Returns
        -------
        None
        """
        for i in range(self.start_id - self.page, self.start_id):
            soup = self.fetch_data(self.start_url + str(i))
            # print(self.get_content(soup))
            print(self.get_datetime(soup))
            time.sleep(0.3)

        return None

# Create an instance of UDN scraper and get article info
udn = UDN(1000000, "https://udn.com/news/story/124222/", 8243941)
udn.get_info()
