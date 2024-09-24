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

class CNYES :
    def __init__(self, page: int, start_url: str, start_id: int) -> None:
        
        self.page = page #爬的文章數
        self.start_url = start_url #開始的URL
        self.start_id = start_id #開始的文章ID
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
    
    def get_content(self, soup: BeautifulSoup):
        """從抓取的數據中提取文章的正文內容"""
        
        contents = soup.findAll('p', class_ = None)
        if contents:
            result = []
            for content in contents :
                result.append(content.text)
                
            return result
        else :
            return None
    
    def get_datetime(self, soup: BeautifulSoup):
        """從抓取的數據中提取文章的發佈日期"""

        datetime_tag = soup.find(class_ = 'alr4vq1')
        return datetime_tag.text.split(" ")[-2] if datetime_tag else None

        
    def get_info(self):
        """循環抓取文章信息並輸出"""
        
        for i in range(self.start_id - self.page, self.start_id) :
            soup = self.fetch_data(self.start_url+str(i))
            if soup :
                # print(self.get_content(soup))
                print(self.get_datetime(soup))
                time.sleep(0.3)
            else :
                print("stop scrawl")
                return 

        return None

cnyes = CNYES(1000000, "https://news.cnyes.com/news/id/", 5723219)
cnyes.get_info()