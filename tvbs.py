import requests
from bs4 import BeautifulSoup
import time
import json

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

class TVBS :
    
    def __init__(self, page: int, start_url: str, start_id: int) -> None:
        
        self.page = page #爬的文章數
        self.start_url = start_url #開始的URL
        self.start_id = start_id #開始的文章ID
        self.article_list = []

    def fetch_data(self, url: str):
        """爬取網頁數據並提取JSON格式的內容"""

        try:
            response = requests.get(url)
            response.encoding = 'utf-8'  # 設置為 utf-8
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', type="application/ld+json")
            main_data = json.loads(script_tag.string) if script_tag else None
            
            return main_data
        
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None
        
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {url}: {e}")
            return None
        
    def get_content(self, main_data: str):
        """從抓取的數據中提取文章的正文內容"""
        
        return main_data.get("articleBody", "No content available") if main_data else None

    
    def get_datetime(self, main_data: str):
        """從抓取的數據中提取文章的發佈日期"""
        
        return main_data.get("datePublished", "No date available") if main_data else None
        
    def get_info(self):
        """循環抓取文章信息並輸出"""

        for i in range(self.start_id - self.page, self.start_id) :
            soup = self.fetch_data(self.start_url + str(i))
            # print(self.get_content(soup))
            print(self.get_datetime(soup))
            time.sleep(0.3)

        return None



tvbs = TVBS(50, "https://news.tvbs.com.tw/money/", 2628359)
tvbs.get_info()