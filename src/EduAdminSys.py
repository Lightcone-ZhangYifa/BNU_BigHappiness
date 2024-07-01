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


def guide(driver: WebDriver, target: str) -> None:
    global menu_titles
    left_menu = driver.find_element(By.CSS_SELECTOR, 'ul[class="left-menu"]')
    menu_items = left_menu.find_elements(By.CSS_SELECTOR, 'li[class="menu-item"]')
    menu_titles = [i.text for i in menu_items]
    if target not in menu_titles:
        raise ValueError(f"{target}不在菜单中，请在下列中选择存在的菜单项:\n{menu_titles}")
    # for i in menu_items:
    #     print(i.text)
    target_items = [i for i in menu_items if i.text==target][0]
    target_items.click()


driver = WebDriver_Init(url=url['教务管理'])
login(driver)
guide(driver, target='网上选课')
