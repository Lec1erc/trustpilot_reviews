from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import win32clipboard
import random
import time


def get_review():
    text = open(r'data\reviews.txt').read()
    text = text.split("\n\n")
    review = random.choice(text).split("\n")
    if review[0] == "":
        review.pop(0)
    title = review.pop(0)
    body = "".join(review)
    return [title, body]


def get_proxy():
    lines = open('data\proxy.txt').read().splitlines()
    name = random.choice(lines).split(":")
    option_proxy = {"proxy":{
        "http": 'http://'+name[2]+':'+name[3]+'@'+name[0]+':'+name[1],
        "https": 'https://'+name[2]+':'+name[3]+'@'+name[0]+':'+name[1],
        "no-proxy": "localhost,127.0.0.1"
    }}
    return option_proxy


def get_ua():
    ua = UserAgent()
    user_agent = ua.random
    return user_agent


def get_copy():
    """Copy clipboard to var"""
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return text


def get_name():
    lines = open(r'data\names.txt').read().splitlines()
    name = random.choice(lines)
    return name


class Use:
    def __init__(self):
        self.options = Options()
        # self.options.add_argument(f'--proxy-server={get_proxy()}')  # Uncomment this string, if proxy without log/pass
        self.options.add_argument(f'user-agent={get_ua()}')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                       chrome_options=self.options,
                                       seleniumwire_options=get_proxy())  # This string using log/pass proxy
        time.sleep(2)
        self.driver.get("https://www.trustpilot.com/")
        self.driver.switch_to.new_window('tab')
        self.driver.get("https://www.minuteinbox.com/")  # Free temp mail
        self.wait = WebDriverWait(self.driver, 5000)

    def click(self, path, method=By.XPATH):
        for el in range(3):
            time.sleep(0.1)
            try:
                self.driver.find_element(method, path).click()
            except:
                pass

    def switch(self, tab):
        time.sleep(0.5)
        self.driver.switch_to.window(self.driver.window_handles[tab])

    def send(self, path, text, submit=True):
        """Write text into text fields"""
        time.sleep(0.9)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, path)))
        element = self.driver.find_element(By.XPATH, path)
        element.send_keys(text)
        if submit:
            element.submit()

    def wait_until(self, path, method=True):
        """Wait for the element to be usable"""
        time.sleep(0.9)
        if method:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, path)))
        else:
            self.wait.until(EC.presence_of_element_located((By.XPATH, path))).click()

    def get_value(self, id):
        """Get the verification code from mail"""
        time.sleep(1.5)
        self.wait.until(EC.presence_of_element_located((By.ID, id)))
        content = self.driver.find_elements(By.ID, id)
        time.sleep(1)
        content = content[0].text.split(" ")[2]
        return content
