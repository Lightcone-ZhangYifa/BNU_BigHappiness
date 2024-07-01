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
from typing import Optional
from requests.compat import urljoin
import theme
from BNU import url, login, WebDriver_Init

menu_titles = ['学籍档案',
               '辅修事宜',
               '学籍异动',
               '培养方案',
               '网上选课',
               '教学安排',
               '考试安排',
               '等级考试',
               '学业成绩',
               '网上评教',
               '毕业事宜',
               '电子证明']

OnlineCourseSelection_modules = []


def guide(driver: WebDriver, target: str) -> None:
    global menu_titles
    left_menu = driver.find_element(By.CSS_SELECTOR, 'ul[class="left-menu"]')
    menu_items = left_menu.find_elements(By.CSS_SELECTOR, 'li[class="menu-item"]')
    menu_titles = [i.text for i in menu_items]
    if target not in menu_titles:
        raise ValueError(f"{target}不在菜单中，请在下列中选择存在的菜单项:\n{menu_titles}")
    # for i in menu_items:
    #     print(i.text)
    target_items = [i for i in menu_items if i.text == target][0]
    target_items.click()


def isActiveModule(module: WebElement) -> bool:
    return "baseMode1.png" in module.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')


def OnlineCourseSelection_module_select(driver: WebDriver, target: str) -> None:
    guide(driver, target='网上选课')

    iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[id="frmDesk"]')
    driver.switch_to.frame(iframe)

    all_modules = driver.find_elements(By.CSS_SELECTOR, 'div[class="module"]')
    all_module_titles = [i.text for i in all_modules]
    active_module_titles = [i.text for i in all_modules if isActiveModule(i)]

    if target not in all_module_titles:
        raise ValueError(
            f"{target}当前不可用，\n当前存在的菜单项:\n{all_module_titles}\n当前有效的菜单项:\n{active_module_titles}")
    target_items = [i for i in all_modules if i.text == target][0].find_element(By.CSS_SELECTOR, 'div[class="title"]')
    target_items.click()


def exportCSV(content: list[dict[str:str]], path: Optional[str]=None,encoding:str='gbk') -> None:
    if not path:
        path = '../res/course_data.csv'
    with open(path, mode='wt', encoding=encoding) as f:
        f.write(','.join([i.replace(',','，') for i in content[0].keys()])+'\n')
        for i in content:
            f.write(','.join([j.replace(',','，') for j in i.values()]) + '\n')
    theme.Info(f'Export csv data to: {os.path.abspath(os.path.join(os.getcwd(),path))}')


def toContent(table: list[dict[str, WebElement]]) -> list[dict[str, str]]:
    # table_text = []
    # for i in table:
    #     table_text.append({j: i[j].text for j in i})
    table_text = [{j: i[j].text for j in i} for i in table]
    theme.Info('Get table content successfully')
    return table_text


def getTable(driver: WebDriver) -> list[dict[str, WebElement]]:
    table = driver.find_element(By.CSS_SELECTOR, 'table')
    table_title = [i.text for i in table.find_element(By.CSS_SELECTOR, 'thead').find_elements(By.CSS_SELECTOR, 'td')]
    table_body_items = table.find_element(By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')

    # items = []
    # for i in table_body_items:
    #     items.append({table_title[j]: i.find_elements(By.CSS_SELECTOR, 'td')[j] for j in range(len(table_title))})
    items = [{table_title[j]: i.find_elements(By.CSS_SELECTOR, 'td')[j] for j in range(len(table_title))}
             for i in table_body_items]
    theme.Info('Get table element successfully')
    return items


def professionCS(driver: WebDriver):
    OnlineCourseSelection_module_select(driver, '按开课计划选课')

    iframe = driver.find_element(By.CSS_SELECTOR, 'iframe[id="frmReport"]')
    driver.switch_to.frame(iframe)

    table = getTable(driver)
    print(table)
    table_text = toContent(table)
    print(table_text)
    for i in table_text:
        print(i)
    table_text = toContent(table)
    exportCSV(table_text)

    driver.switch_to.default_content()

def generalCS():
    pass


driver = WebDriver_Init(url=url['教务管理']
                        # , silent=True
                        )
login(driver)
professionCS(driver)
while 1:
    pass
driver.quit()
