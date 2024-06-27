import glob
import os.path

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
import BNU

max_page = -1
earliest = (2024, 5, 1)
temp_folder = '../temp/'

current_page = 1
current_item = 0

page_url = 'https://onevpn.bnu.edu.cn/https/77726476706e69737468656265737421fff94494263c641e7c069ce29d51367b9b9e/tp_fp/view?m=fp#act=fp/library/show&pn='
keys = 'time', 'title', 'visit', 'handler', 'content'


def find_with_ExplicitWait(driver, by: str, value, timeout: int = 10):
    return WebDriverWait(driver, timeout=timeout).until(
        EC.presence_of_element_located((by, value))
    )


def find_all_elements_with_ExplicitWait(driver, by: str, value, timeout: int = 10):
    return WebDriverWait(driver, timeout=timeout).until(
        # EC.presence_of_all_elements_located((by, value))
        lambda x: x.find_elements(by, value)
    )
    # time.sleep(3)
    # return driver.find_elements(by,value)


def get_single_item(driver: WebDriver, item: WebElement, filter=lambda x: None, timeout: int = 10) -> dict:
    brief_title = item.find_element(By.CSS_SELECTOR, "div[class='purchase-info-tit push-down-5']")
    brief_infos = item.find_element(By.CSS_SELECTOR, "div[class='purchase-info-02 push-down-15']").find_elements(
        By.TAG_NAME, 'p')
    brief_title.click()
    try:
        # popup = WebDriverWait(driver, timeout=timeout).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='responsive-padding-box form-horizontal']"))
        # )
        popup = find_with_ExplicitWait(driver, By.CSS_SELECTOR, "div[class='responsive-padding-box form-horizontal']")

        # popup_elements = popup.find_elements(By.TAG_NAME,'div')
        popup_elements = find_all_elements_with_ExplicitWait(popup, By.TAG_NAME, 'div')
        title = popup_elements[0].text
        popup_infos = popup_elements[1].find_elements(By.TAG_NAME, 'p')
        content = popup_elements[2].text
        # popup = driver.find_element(By.CSS_SELECTOR, "div[class='responsive-padding-box form-horizontal']")
        # for i in popup_elements:
        #     print(i,i.text)
        info = {
            'time': brief_infos[2].find_elements(By.TAG_NAME, 'span')[-1].text,
            'title': title,
            'handler': popup_infos[0].text,
            'visit': popup_infos[2].text,
            'content': content
        }
        # time.sleep(3)
        button_close = driver.find_element(By.CSS_SELECTOR, "button[class='close']")
        # print(f'info from popup: {info}')
        # input('close...')
        button_close.click()
        return info
    except:
        print(brief_title.text + '的内容没加载成功！')
        return {}

    # popup = driver.find_element(By.CSS_SELECTOR,"div[class='responsive-padding-box form-horizontal']")
    # popup_elements = popup.find_element(By.CSS_SELECTOR,"div[class='bar fz-14 light-gray push-up-5 push-down-10 border-down-e3e3e3']").find_elements(By.TAG_NAME,'p')
    # # for i in popup_elements:
    # #     print(i,i.text)
    # info = {
    #     'time': brief_infos[2].find_elements(By.TAG_NAME,'span')[-1].text,
    #     'title': popup.find_element(By.CSS_SELECTOR, "div[class='bar fz-16 line-height-24 text-bold text-primary']").text,
    #     'handler': popup_elements[0].text,
    #     'visit': popup_elements[2].text,
    #     'content': popup.find_element(By.CSS_SELECTOR, "div[id='pim_content']").text
    # }
    # print(info)
    # time.sleep(1)
    # button_close = driver.find_element(By.CSS_SELECTOR, "button[class='close']")
    # button_close.click()
    # return info


def get_page_cnt(driver: WebDriver) -> int:
    try:
        return int(driver.find_element(By.XPATH, '//*[@id="layer_page_pager_list"]/div[2]/span[3]').text)
        # return int(driver.find_element(By.CSS_SELECTOR, "a[title='尾页']").text)
    except NoSuchElementException:
        return int(driver.find_element(By.XPATH, '//*[@id="layui-laypage-1"]/a[6]').text)
        # return int(driver.find_element(By.CSS_SELECTOR, "a[title='尾页']").text)


def generateCSV(items: list) -> None:
    labels = keys
    with open('../res/raw_data.csv', mode='wt', encoding='utf-8') as f:
        f.write(','.join(labels))
        for item in items:
            f.write(','.join([item[label] for label in labels]))


def generateCSV_title() -> None:
    labels = keys
    with open('../res/raw_data.csv', mode='wt', encoding='utf-8') as f:
        f.write(','.join(labels) + '\n')


def generateCSV_append_item(item: dict) -> None:
    labels = keys
    for i in item:
        item[i] = item[i].replace('\n', '')
        item[i] = item[i].replace(',', '，')

    item['visit'] = item['visit'][4:]
    item['handler'] = item['handler'][5:]
    with open('../res/raw_data.csv', mode='a', encoding='utf-8') as f:
        f.write(','.join([item[label] for label in labels]) + '\n')


def toPage(driver: WebDriver, page: int) -> None:
    # driver.close()
    print('loading target url :', page_url + str(page))
    driver.get(url=(page_url + str(page)))


def write_config(current_page: int, current_item: int) -> None:
    with open('../tmp/conf.dat', 'wt', encoding='utf-8') as f:
        f.write(str(current_page) + ' ' + str(current_item))


def read_config() -> None:
    global current_page, current_item
    if os.path.exists('../tmp/conf.dat'):
        with open('../tmp/conf.dat', 'rt', encoding='utf-8') as f:
            current_page, current_item = [int(i) for i in f.read().split()]
        print(f'[Config]: start from page{current_page}, item{current_item+1}.')
    else:
        print('[Notice]: cannot find configuration file.')
        with open('../tmp/conf.dat', 'wt', encoding='utf-8') as f:
            f.write('1 0')
        print('[Notice]: create default configuration file successfully.')


def get_all_items(driver: WebDriver) -> None:
    global current_page, current_item
    page_cnt = get_page_cnt(driver)
    print('page_cnt =', page_cnt)
    for i in range(current_page, page_cnt + 1):
        toPage(driver, page=i)

        current_page = i

        print('current page =', i)
        # input('continue...')
        item_list = driver.find_elements(By.CSS_SELECTOR, "div[class='purchase-con push-down-20']")
        if current_item != 0:
            for j in range(current_item, len(item_list)):
                while True:
                    driver.refresh()
                    item_list = driver.find_elements(By.CSS_SELECTOR, "div[class='purchase-con push-down-20']")
                    single_item = get_single_item(driver, item_list[j])
                    if single_item:
                        generateCSV_append_item(single_item)
                        current_item = (j + 1) % len(item_list)
                        write_config(current_page, current_item)
                        print(f'Add page{i} item{j + 1} sussceefully :{single_item}')
                        break
                    else:
                        print('retrying...')
        else:
            for j in range(len(item_list)):
                while True:
                    driver.refresh()
                    item_list = driver.find_elements(By.CSS_SELECTOR, "div[class='purchase-con push-down-20']")
                    single_item = get_single_item(driver, item_list[j])
                    if single_item:
                        generateCSV_append_item(single_item)
                        current_item = (j + 1) % len(item_list)
                        write_config(current_page, current_item)
                        print(f'Add page{i} item{j + 1} sussceefully :{single_item}')
                        break
                    else:
                        print('retrying...')


def get_recent_data():
    pass
