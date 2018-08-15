from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import random
import xml.etree.ElementTree as ET
import re
import time
import typing

def direct_dl(megalink, savedir, chromedriverpath):
    links_list = []

    if isinstance(megalink, typing.List):
        links_list = megalink
    elif isinstance(megalink, str):
        if ".txt" in megalink:
            with open(megalink) as f:
                links_list = f.readlines()
    else:
        links_list.append(megalink)

    if not os.path.exists(savedir):
        os.makedirs(savedir)

    options = Options()
    options.add_argument('headless')
    options.add_argument('window-size=1366x768')
    options.add_argument('--disable-browser-side-navigation')
    prefs = {'download.default_directory' : savedir,
             "download.prompt_for_download": False}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriverpath)

    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': savedir}}
    command_result = driver.execute("send_command", params)

    for l in links_list:
        print("l = " + l)

    for l in links_list:
        link = re.search("#.*", l).group(0)
        driver.get("https://google.com")
        time.sleep(1)
        print("Downloading: [" + link + "]")
        driver.get('https://directme.ga/' + link)
        time.sleep(1)

    done = False
    while not done:
        arr = os.listdir(savedir)
        d = True
        for a in arr:
            if "crdownload" in a:
                print("Not done")
                time.sleep(5)
                d = False
                break
        if d: done=True

if __name__ == '__main__':
    l = d = chrome = None

    config_path = os.path.join(os.getcwd(), "mega_config.xml")

    if os.path.isfile(config_path):
        with open(config_path) as f:
            e = ET.fromstringlist(["<root>", f.read(), "</root>"])
            l = e.find("download").get("l")
            d = e.find("download").get("d")
            chrome = e.find("download").get("chrome")
    else:
        l = input("Link or Text File: ").strip()
        d = input("Save Directory: ").strip()
        chrome = input("Chromedriver Path: ").strip()

    direct_dl(l, d, chrome)