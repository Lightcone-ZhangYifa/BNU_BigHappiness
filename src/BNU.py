import glob
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

url = {
    '教务管理': 'https://onevpn.bnu.edu.cn/http/77726476706e69737468656265737421f3f652d2253e7d1e7b0c9ce29b5b/cas/login?service=http%3A%2F%2Fzyfw.bnu.edu.cn%2F',
    '数字京师': 'https://onevpn.bnu.edu.cn/http/77726476706e69737468656265737421f3f652d2253e7d1e7b0c9ce29b5b/cas/login?service=https%3A%2F%2Fonevpn.bnu.edu.cn%2Flogin%3Fcas_login%3Dtrue',
    '京师大福': 'https://onevpn.bnu.edu.cn/https/77726476706e69737468656265737421fff94494263c641e7c069ce29d51367b9b9e/tp_fp/view?m=fp#act=fp/library/show'
}

username = '202311998186'
password = '@Yif123456'

def WebDriver_Init(url: str, silent: bool = False, timeout: int = 3) -> WebDriver:
    chrome_options = Options()
    if silent:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver.implicitly_wait(timeout)
    driver.get(url=url)
    # driver.set_window_size()
    # time.sleep(timeout)
    return driver

def login(driver: WebDriver, username: str or int, password: str, autorefresh: bool = False) -> list[dict]:
    input_username = driver.find_element(By.CSS_SELECTOR, "input[id='un']")
    input_password = driver.find_element(By.CSS_SELECTOR, "input[id='pd']")
    input_username.send_keys(str(username))
    input_password.send_keys(str(password))

    button_login = driver.find_element(By.ID, 'index_login_btn')
    button_login.click()

    # 密码错误的情况：
    try:
        error = driver.find_element(By.ID, 'errormsg')
        print(error.text)
        input_username = driver.find_element(By.CSS_SELECTOR, "input[id='un']")
        input_password = driver.find_element(By.CSS_SELECTOR, "input[id='pd']")
        input_username.clear()
        input_password.clear()
        username = input('Enter username:')
        password = input('Enter password:')
        login(driver, username, password, autorefresh)
    except NoSuchElementException:
        print('Login successfully')
        cookies = driver.get_cookies()
        if autorefresh:
            time.sleep(5)
            driver.refresh()
        return cookies

# driver = WebDriver_Init(url=url['京师大福'])
# print(login(driver, username, password))
# input('continue...')
