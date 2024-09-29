import time
import random
import requests
from bs4 import BeautifulSoup
import html # 引入 html 模組以解碼轉義字符

class CnyesNewsSpider():

    def __init__(self):
        self.base_url = "https://api.cnyes.com/media/api/v1/newslist/category/headline"
        self.headers = {
            'Origin': 'https://news.cnyes.com/',
            'Referer': 'https://news.cnyes.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

    def get_newslist_info(self, page=100, limit=30):
        """ 獲取指定頁數的新聞資料 """
        r = requests.get(f"{self.base_url}?page={page}&limit={limit}", headers=self.headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            return None
        newslist_info = r.json()['items']
        return newslist_info

    def crawl_all_news(self):
        """ 爬取所有新聞資料，直到最後一頁 """
        page = 1
        limit = 30
        all_news = []

        while True:
            newslist_info = self.get_newslist_info(page=page, limit=limit)

            if not newslist_info:
                print("已無更多新聞可抓取。")
                break

            print(f'正在爬取第 {page} 頁，共 {len(newslist_info["data"])} 條新聞。')

            # 保存當前頁的新聞
            for news in newslist_info["data"]:
                # 格式化時間，只顯示年月日
                publish_date = time.strftime("%Y-%m-%d", time.localtime(news["publishAt"]))

                # 解碼 HTML 轉義字符
                if news["content"]:
                    decoded_content = html.unescape(news["content"])  # 轉換 HTML 轉義字符
                    soup = BeautifulSoup(decoded_content, 'html.parser')  # 使用 BeautifulSoup 解析 HTML
                    clean_content = soup.get_text()  # 提取純文字
                else:
                    clean_content = "無內文"
                
                content_preview = clean_content[:30]  # 截取內文前30個字

                news_item = {
                    'URL': f'https://news.cnyes.com/news/id/{news["newsId"]}',
                    '標題': news["title"],
                    '內文預覽': content_preview,
                    '關鍵字': news["keyword"],
                    '發布時間': publish_date,
                    '分類': news["categoryName"],
                }
                all_news.append(news_item)

                # 列印新聞
                print(f'    ------------ {news["newsId"]} ------------')
                # print(f'    新聞 > URL：{news_item["URL"]}')
                # print(f'    新聞 > 標題：{news_item["標題"]}')
                # print(f'    新聞 > 內文預覽：{news_item["內文預覽"]}')
                # print(f'    新聞 > 關鍵字：{news_item["關鍵字"]}')
                # print(f'    新聞 > 發布時間：{news_item["發布時間"]}')
                # print(f'    新聞 > 分類：{news_item["分類"]}')
                # print()

            # 隨機延遲，避免反爬蟲
            time.sleep(random.uniform(2, 5))

            # 檢查是否還有下一頁
            if newslist_info["next_page_url"] is None:
                break

            page += 1

        print(f"共爬取 {len(all_news)} 條新聞。")
        return all_news
if __name__ == "__main__":
    cnyes_news_spider = CnyesNewsSpider()
    all_news = cnyes_news_spider.crawl_all_news()

