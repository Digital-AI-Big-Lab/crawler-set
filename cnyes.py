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
            "datetime": YYYY-MM-DDD,
            "link": link,
            "content": content,
            "comments": comments,
        },
        article_content = {
            ...
    ]
"""

class CNYES:
    def __init__(self, page: int, start_url: str, start_id: int) -> None:
        """
        Initializes the CNYES class with aritcle count, starting URL, and the latest article ID.

        Parameters
        ----------
        page : int
            The number of articles to scrape.
        start_url : str
            The base URL without the article ID.
        start_id : int
            The ID of the latest article to start scraping from.
        """
        self.page = page  # 爬的文章數
        self.start_url = start_url  # 開始的URL
        self.start_id = start_id  # 開始的文章ID
        self.article_list = []  # 儲存爬取的文章信息

    def fetch_data(self, url: str) -> BeautifulSoup:
        """
        Requests the target URL and returns a BeautifulSoup object for further parsing.

        Parameters
        ----------
        url : str
            The URL of the target webpage.

        Returns
        -------
        BeautifulSoup
            The parsed HTML content of the webpage, ready for data extraction.
        """        
        try:
            response = requests.get(url)
            response.raise_for_status()  # 檢查HTTP請求是否成功
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None

    def get_content(self, soup: BeautifulSoup) -> list[str]:
        """
        Extracts the article content from the provided BeautifulSoup object.

        Parameters
        ----------
        soup : BeautifulSoup
            The parsed HTML content of the article's webpage.

        Returns
        -------
        list[str]
            A list of paragraphs containing the article content.
            Returns None if no content is found.
        """        
        contents = soup.findAll('p', class_=None)
        if contents:
            result = [content.text for content in contents]  # 使用列表推導式簡化代碼
            return result
        else:
            return None

    def get_datetime(self, soup: BeautifulSoup) -> str:
        """
        Extracts the publication date from the provided BeautifulSoup object.

        Parameters
        ----------
        soup : BeautifulSoup
            The parsed HTML content of the article's webpage.

        Returns
        -------
        str
            The publication date of the article in 'YYYY-MM-DD' format.
            Returns None if no date is found.
        """        
        datetime_tag = soup.find(class_='alr4vq1')
        return datetime_tag.text.split(" ")[-2] if datetime_tag else None

    def get_info(self) -> dict:
        """
        Iterates through a range of article IDs, fetching and extracting data from each article.

        Returns
        -------
        dict
            A dictionary containing extracted article information such as title, content, and date.
            The method will stop and return None if the scraping process encounters an error.
        """        
        for i in range(self.start_id - self.page, self.start_id):
            url = self.start_url + str(i)
            soup = self.fetch_data(url)
            if soup:
                content = self.get_content(soup)
                datetime = self.get_datetime(soup)
                self.article_list.append({
                    "url": url,
                    "content": content,
                    "datetime": datetime
                })
                print(f"Scraped data from article ID {i}: {datetime}")
                time.sleep(0.3)  # 控制爬取速度
            else:
                print("Stopping the scrape due to an error.")
                return None
        return self.article_list

# 測試代碼
cnyes = CNYES(100, "https://news.cnyes.com/news/id/", 5723219)
cnyes.get_info()
