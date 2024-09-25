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

class FSC:
    def __init__(self, page: int, url: str) -> None:
        """
        Initializes the FSC class, setting the number of articles to scrape
        and the target URL.

        Parameters
        ----------
        page : int
            Number of articles to scrape.
        url : str
            Target base URL.
        """
        self.page = page 
        self.url = url 
        self.article_list = []  # Store the list of article links

    def fetch_data(self, url: str):
        """
        Sends a request to the given URL and returns the parsed HTML document
        as a BeautifulSoup object.

        Parameters
        ----------
        url : str
            The target URL to fetch the webpage from.

        Returns
        -------
        BeautifulSoup
            Parsed HTML document as a BeautifulSoup object.
        """
        try:
            response = requests.get(url)  # Send GET request to the target URL
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML
            return soup

        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None

    def get_article_link(self, soup: BeautifulSoup):
        """
        Extracts article links from the parsed HTML document.

        Parameters
        ----------
        soup : BeautifulSoup
            Parsed HTML document.

        Returns
        -------
        list[str]
            A list of article links extracted from the page.
        """
        url_list = []  # Initialize an empty list to store article links
        try:
            contents = soup.find('div', class_="newslist").find_all("a")
            for content in contents:
                url_list.append(content["href"])  # Append each article's href (link) to the list
        
        except AttributeError as e:
            print(f"Error parsing content: {e}")
        
        return url_list 

# Create an instance of the FSC class, specifying the number of pages and target URL
fsc = FSC(1, "https://www.fsc.gov.tw/ch/home.jsp?id=2&parentpath=0")

# Call the get_article_link method and print the extracted article links
print(fsc.get_article_link(fsc.fetch_data("https://www.fsc.gov.tw/ch/home.jsp?id=2&parentpath=0")))
