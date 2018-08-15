from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import random
import re
import time


def direct_dl():
    links_list = []
    with open("links.txt") as f:
        links_list = f.readlines()

    options = Options()
    options.add_argument('headless')
    options.add_argument('window-size=1366x768')
    prefs = {'download.default_directory' : os.getcwd(),
             "download.prompt_for_download": False}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\chromedriver\chromedriver.exe')

    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': os.getcwd()}}
    command_result = driver.execute("send_command", params)

    link = re.search("#.*", random.choice(links_list)).group(0)
    print(link)

    driver.get('https://directme.ga/' + link)
    print("Page Title is : %s" %driver.title)

    time.sleep(10)


if __name__ == '__main__':
    direct_dl()