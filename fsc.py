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

class FSC :
    def __init__(self, page: int, url: str) -> None:
        
        self.page = page #爬的文章數
        self.url = url #開始的URL
        self.article_list = []

    def fetch_data(self, url: str):
        """爬取網頁數據回傳未處理soup"""
        
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None
    
    def get_article_link(self, soup: BeautifulSoup):
        """從抓取的數據中提取各文章連結"""
        
        url_list = []
        contents = soup.find('div', class_ = "newslist").find_all("a")
        for content in contents :
            url_list.append(content["href"])
            
        return url_list
    
    # def get_datetime(self, soup: BeautifulSoup):
    #     datetime_tag = soup.find(class_ = 'alr4vq1')
    #     if datetime_tag :
    #         datetime = datetime_tag.text.split(" ")[-2]  # 取最後一個元素
    #     # print(datetime)
    #         return datetime
    #     else:
    #         return None
        
    # def get_info(self):
        
    #     for i in range(self.start_id - self.page) :
    #         soup = self.fetch_data(self.start_url+str(i))
    #         # print(self.get_content(soup))
    #         print(self.get_datetime(soup))
    #         time.sleep(0.3)

    #     return None

fsc = FSC(1, "https://www.fsc.gov.tw/ch/home.jsp?id=2&parentpath=0")
print(fsc.get_article_link(fsc.fetch_data("https://www.fsc.gov.tw/ch/home.jsp?id=2&parentpath=0")))