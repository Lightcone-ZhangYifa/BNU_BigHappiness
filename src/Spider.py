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

url = 'https://onevpn.bnu.edu.cn/https/77726476706e69737468656265737421fff94494263c641e7c069ce29d51367b9b9e/tp_fp/view?m=fp#act=fp/library/show'
username = '13255675714'
password = ''
max_page = 3
temp_folder = '../temp/'


page_urls = []
keys = 'title', 'visit', 'handler', 'content'


def WebDriver_Init(url: str, silent: bool = False, timeout: int = 10) -> webdriver:
    chrome_options = Options()
    if silent:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver.implicitly_wait(timeout)
    driver.get(url=url)
    # time.sleep(timeout)
    return driver


def login(driver: webdriver, username: str or int, password: str or int) -> None:
    pass
    # input_username = driver.find_element(By.ID, 'register-sms-1_input_1_phone')
    # input_username.send_keys(str(username))
    #
    # button_send = driver.find_element(By.CLASS_NAME, 'zppp-sms__send')
    # button_send.click()
    #
    # verificaion = input('请输入验证码：')
    #
    # input_verification = driver.find_element(By.ID, 'register-sms-1_input_2_validate_code')
    # input_verification.send_keys(verificaion)
    #
    # checkbox_login = driver.find_element(By.ID, 'accept')
    # checkbox_login.click()
    #
    # button_submit = driver.find_element(By.CLASS_NAME, 'zppp-submit')
    # button_submit.click()
    #
    # time.sleep(5)
    #
    # driver.back()
    # driver.refresh()



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


def generateCSV(items: list) -> None:
    labels = keys
    with open('../res/dataset.csv', mode='wt', encoding='gbk') as f:
        f.write(','.join(labels))
        for item in items:
            f.write(','.join([item[label] for label in labels]))


def main():
    driver = WebDriver_Init(url=url
                            # , silent=True
                            )
    input('continue...')
    login(driver=driver, username=username, password=password)
    items_list = get_all_items()
    generateCSV(items_list)


main()
