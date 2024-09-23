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

class UDN :
    def __init__(self, page: int, start_url: str, start_id: int) -> None:
        
        self.page = page #這邊的page指文章數
        self.start_url = start_url #開始的URL
        self.start_id = start_id #開始的文章ID

    def fetch_data(self, url: str):
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup
    
    def get_content(self, soup: BeautifulSoup):
        result = []
        contents = soup.findAll('p', class_ = None)
        
        for content in contents :
            result.append(content.text)
            
        return result
    
    def get_datetime(self, soup: BeautifulSoup):
        datetime_tag = soup.find(class_ = 'article-content__time')
        if datetime_tag :
            datetime = datetime_tag.text.split(" ")[0]
        # print(datetime)
            return datetime
        else:
            return None
        
    def get_info(self):
        
        for i in range(self.start_id - self.page, self.start_id) :
            soup = self.fetch_data(self.start_url+str(i))
            # print(self.get_content(soup))
            print(self.get_datetime(soup))
            time.sleep(0.3)

        return None



udn = UDN(1000000, "https://udn.com/news/story/124222/", 8243941)
udn.get_info()