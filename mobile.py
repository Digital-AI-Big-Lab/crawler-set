from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

class Mobile01Crawler:
    """Mobile01 爬蟲"""
    
    def __init__(self, start_page: int, end_page: int, base_url: str) -> None:
        """
        Initializes the Mobile01Crawler class with start and end page numbers and base URL.

        Parameters
        ----------
        start_page : int
            The page number to start scraping from.
        end_page : int
            The last page number to scrape.
        base_url : str
            The base URL for the topic list.
        """
        self.start_page = start_page  # 爬取的起始页
        self.end_page = end_page  # 爬取的结束页
        self.base_url = base_url  # 基础URL
        self.article_list = []  # 用于存储爬取的信息
        
        # 设置 Chrome 选项
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')  # 禁用 GPU 加速
        chrome_options.add_argument('--disable-extensions')  # 禁用扩展
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片

        # 启动 Chrome
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def fetch_data(self, page: int) -> None:
        """
        Requests the target URL and extracts data from the page.

        Parameters
        ----------
        page : int
            The page number to scrape.
        """
        url = f"{self.base_url}&p={page}"
        print(f"Fetching data from: {url}")
        
        self.driver.get(url)
        time.sleep(1)  # 控制加载时间
        
        titles = self.driver.find_elements(By.CLASS_NAME, "c-listTableTd__title")
        
        for title in titles:
            try:
                # 找到 <a> 标签并提取 href 和标题文本
                link = title.find_element(By.TAG_NAME, "a")
                url = link.get_attribute("href")
                text = link.text
                
                # 保存文章数据
                self.article_list.append({
                    "title": text,
                    "link": url
                })
                print(f"Scraped: {text}, URL: {url}")
            except Exception as e:
                print(f"Error fetching data: {e}")
    
    def get_info(self) -> None:
        """
        Iterates through a range of pages, fetching and extracting data from each page.
        """
        for page in range(self.start_page, self.end_page + 1):
            self.fetch_data(page)
    
    def save_to_json(self, filename: str) -> None:
        """
        Saves the scraped data to a JSON file.

        Parameters
        ----------
        filename : str
            The filename to save the JSON data to.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.article_list, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")
    
    def close(self) -> None:
        """关闭 Selenium 浏览器"""
        self.driver.quit()

# 测试代码
if __name__ == "__main__":
    base_url = 'https://www.mobile01.com/topiclist.php?f=804'  # Mobile01 的基础 URL
    crawler = Mobile01Crawler(start_page=1, end_page=2, base_url=base_url)  # 爬取第1到2页
    crawler.get_info()  # 开始爬取
    crawler.close()  # 关闭浏览器
