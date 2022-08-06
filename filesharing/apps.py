import time

import requests
from django.apps import AppConfig
from selenium import webdriver

my_session = None


def session_start():
    global my_session
    driver = webdriver.Chrome()
    url = "https://www.tu-chemnitz.de/informatik/DVS/blocklist/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    driver.get(url)
    driver.get(url)
    time.sleep(35)
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0"
    }
    my_session = requests.session()
    my_session.headers.update(headers)
    for cookie in driver.get_cookies():
        cookie_data = {cookie['name']: cookie['value']}
        my_session.cookies.update(cookie_data)


class FilesharingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filesharing'
    session_start()
