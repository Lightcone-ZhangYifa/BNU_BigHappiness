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

url = {
    '教务管理': 'https://onevpn.bnu.edu.cn/http/77726476706e69737468656265737421f3f652d2253e7d1e7b0c9ce29b5b/cas/login?service=http%3A%2F%2Fzyfw.bnu.edu.cn%2F',
    '数字京师': 'https://onevpn.bnu.edu.cn/http/77726476706e69737468656265737421f3f652d2253e7d1e7b0c9ce29b5b/cas/login?service=https%3A%2F%2Fonevpn.bnu.edu.cn%2Flogin%3Fcas_login%3Dtrue',
    '京师大福': 'https://onevpn.bnu.edu.cn/https/77726476706e69737468656265737421fff94494263c641e7c069ce29d51367b9b9e/tp_fp/view?m=fp#act=fp/library/show'
}

username = ''
password = ''


def WebDriver_Init(url: str, silent: bool = False, timeout: int = 3) -> WebDriver:
    chrome_options = Options()
    if silent:
        chrome_options.add_argument('--headless')

    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # 禁止打印日志到控制台
    chrome_options.add_argument("--silent")
    # 禁止打印Chrome驱动的信息日志
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument('--disable-gpu')  # 上面代码就是为了将Chrome不弹出界面
    chrome_options.add_argument('--start-maximized')  # 最大化
    chrome_options.add_argument('--incognito')  # 无痕隐身模式
    chrome_options.add_argument("disable-cache")  # 禁用缓存
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('log-level=3')


    driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(timeout)
    driver.get(url=url)
    # driver.set_window_size()
    # time.sleep(timeout)
    return driver


def write_info(username: str, password: str) -> None:
    with open('../tmp/info.dat', 'wt', encoding='utf-8') as f:
        f.write(username + ' ' + password)


def read_info() -> None:
    global username, password
    if os.path.exists('../tmp/info.dat'):
        with open('../tmp/info.dat', 'rt', encoding='utf-8') as f:
            username, password = f.read().split()
        theme.Config('load login info successfully.')
    else:
        theme.Notice('no login info found.')
        with open('../tmp/info.dat', 'wt', encoding='utf-8') as f:
            f.write('0 0')


def login(driver: WebDriver, username: str or int, password: str, autorefresh: bool = False) -> list[dict]:
    input_username = driver.find_element(By.CSS_SELECTOR, "input[id='un']")
    input_password = driver.find_element(By.CSS_SELECTOR, "input[id='pd']")
    input_username.send_keys(str(username))
    input_password.send_keys(str(password))

    button_login = driver.find_element(By.ID, 'index_login_btn')
    button_login.click()

    # 密码错误的情况：
    try:
        if username != '' and password != '':
            error = driver.find_element(By.ID, 'errormsg')
            theme.Error(error.text)
        else:
            theme.Error('用户名和密码不能为空。')
        input_username = driver.find_element(By.CSS_SELECTOR, "input[id='un']")
        input_password = driver.find_element(By.CSS_SELECTOR, "input[id='pd']")
        input_username.clear()
        input_password.clear()
        username = input('Enter username:')
        password = input('Enter password:')
        login(driver, username, password, autorefresh)
    except NoSuchElementException:
        theme.Successfully('Login successfully')
        write_info(username, password)
        cookies = driver.get_cookies()
        if autorefresh:
            time.sleep(5)
            driver.refresh()
        return cookies

# driver = WebDriver_Init(url=url['京师大福'])
# print(login(driver, username, password))
# input('continue...')
