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
'https://onevpn.bnu.edu.cn/http/77726476706e69737468656265737421f3f652d2253e7d1e7b0c9ce29b5b/cas/login?service=http%3A%2F%2Fzyfw.bnu.edu.cn%2F'
'https://onevpn.bnu.edu.cn/https/77726476706e69737468656265737421fff944d2253e7d1e7b0c9ce29b5b/dcp/forward.action?path=/portal/portal&p=home'
'https://onevpn.bnu.edu.cn/http/77726476706e69737468656265737421f3f652d2253e7d1e7b0c9ce29b5b/cas/login?service=https%3A%2F%2Fonevpn.bnu.edu.cn%2Flogin%3Fcas_login%3Dtrue'
url = 'https://onevpn.bnu.edu.cn/https/77726476706e69737468656265737421fff94494263c641e7c069ce29d51367b9b9e/tp_fp/view?m=fp#act=fp/library/show'
username = '13255675714'
password = ''
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
    # verificaion = input('«Î ‰»Î—È÷§¬Î£∫')
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

