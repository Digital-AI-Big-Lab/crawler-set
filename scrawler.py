# # scrawler.py
import requests
from bs4 import BeautifulSoup


def fetch_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 在這裡解析你需要的數據
    return soup
def printData(url):
    data = fetch_data(url)
    tags = data.findAll('p', class_ = None)
    for tag in tags :
        print(tag.text)
        
# x = 'https://news.cnyes.com/news/id/'  # 替換為你要爬取的網址
# for i in range(5621198,5721198) :
#     time.sleep(1)
#     printData(x+str(i))
#     # 在這裡處理獲取的數據
printData("https://udn.com/news/story/124222/8243941")
