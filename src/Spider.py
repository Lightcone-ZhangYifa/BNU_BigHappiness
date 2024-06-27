import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from bs4 import BeautifulSoup
import BNU

max_page = 3
temp_folder = '../temp/'


page_urls = []
keys = 'title', 'visit', 'handler', 'content'



def get_single_item() -> dict:
    # 1.点开
    # 2.爬取
    # 3.点×
    # 返回
    # item = {,,,}
    pass


def get_page_urls(driver: webdriver) -> list:
    # 在第一页获取所有页面的链接
    pass


def toPage(driver: webdriver, page: int) -> None:
    global page_urls
    driver.close()
    driver.get(page_urls)

def get_all_items() -> list:
    # page_cnt 爬取一共多少页
    dataset = []
    for i in range(page_cnt):
        toPage(i)
        # item_list 得到每一个对象
        for item in item_list:
            dataset.append(get_single_item(item))
    return dataset

def get_recent_data():
    pass


def generateCSV(items: list) -> None:
    labels = keys
    with open('../res/raw_data.csv', mode='wt', encoding='gbk') as f:
        f.write(','.join(labels))
        for item in items:
            f.write(','.join([item[label] for label in labels]))


def main():
    driver = BNU.WebDriver_Init(url=BNU.url
                            # , silent=True
                            )
    input('continue...')
    BNU.login(driver=driver, username=BNU.username, password=BNU.password)
    items_list = get_all_items()
    generateCSV(items_list)

    driver.quit()

main()
