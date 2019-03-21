import json

import requests
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from cookiespool.config import *
from cookiespool.db import CookiesRedisClient, AccountRedisClient
from cookiespool.verify import Yundama


class CookiesGenerator(object):
    def __init__(self, name='default', browser_type=DEFAULT_BROWSER):
        """
        父类, 初始化一些对象
        :param name: 名称
        :param browser: 浏览器, 若不使用浏览器则可设置为 None
        """
        self.name = name
        self.cookies_db = CookiesRedisClient(name=self.name)
        self.account_db = AccountRedisClient(name=self.name)
        self.browser_type = browser_type

    def _init_browser(self, browser_type):
        """
        通过browser参数初始化全局浏览器供模拟登录使用
        :param browser: 浏览器 PhantomJS/ Chrome
        :return:
        """
        if browser_type == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps[
                "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)
        elif browser_type == 'Chrome':
            # chrome_options = Options()
            # chrome_options.add_argument('--headless')
            # self.browser = webdriver.Chrome(chrome_options=chrome_options)
            self.browser = webdriver.Chrome()

    def new_cookies(self, username, password):
        raise NotImplementedError

    def set_cookies(self, account):
        """
        根据账户设置新的Cookies
        :param account:
        :return:
        """
        results = self.new_cookies(account.get('username'), account.get('password'))
        if results:
            username, cookies = results
            print('Saving Cookies to Redis', username, cookies)
            self.cookies_db.set(username, cookies)


    def run(self):
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        accounts = self.account_db.all()
        cookies = self.cookies_db.all()
        # print(cookies)
        # Account 中对应的用户
        accounts = list(accounts)
        # Cookies中对应的用户
        valid_users = [cookie.get('username') for cookie in cookies]
        # print('Getting', len(accounts), 'accounts from Redis')
        if len(accounts):
            self._init_browser(browser_type=self.browser_type)
        for account in accounts:
            print(account, valid_users)
            if not account.get('username') in valid_users:
                print('Getting Cookies of ', self.name, account.get('username'), account.get('password'))
                self.set_cookies(account)
        print('Generator Run Finished')

    def close(self):
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')


class xiaoshuoCookiesGenerator(CookiesGenerator):
    def __init__(self, name='xiaoshuo', browser_type=DEFAULT_BROWSER):
        """
        :param name: 名称:小说
        :param browser: 使用的浏览器
        """
        CookiesGenerator.__init__(self, name, browser_type)
        self.name = name
        # self.ydm = yan zheng ma

    def _success(self, username):
        wait = WebDriverWait(self.browser, 5)
        self.browser.get('http://www.quanshuwang.com/')
        cookies = {}
        for cookie in self.browser.get_cookies():
            cookies[cookie["name"]] = cookie["value"]
        print(cookies)
        print('成功获取到Cookies')
        return (username, json.dumps(cookies))

    def new_cookies(self, username, password):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        print('Generating Cookies of', username)
        self.browser.delete_all_cookies()
        print('====go===')
        self.browser.get('http://www.quanshuwang.com/')
        wait = WebDriverWait(self.browser, 20)

        try:
            user = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#htmlUserName')))
            user.send_keys(username)
            psd = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#htmlPassword')))
            psd.send_keys(password)
            submit = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="submit"].btn1')))
            submit.click()
            # time.sleep(3)
            result = self._success(username)
            if result:
                return result
        except :
            print('error')


class MxiaoshuoCookiesGenerator(CookiesGenerator):
    def __init__(self, name='xiaoshuo', browser_type=DEFAULT_BROWSER):
        """
        :param name: 名称:小说
        :param browser: 使用的浏览器
        """
        CookiesGenerator.__init__(self, name, browser_type)
        self.name = name

    def _success(self, username):
        wait = WebDriverWait(self.browser,5)
        self.browser.get('http://www.quanshuwang.com/')
        print('------open')
        # success = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'me_portrait_w')))
        cookies = {}
        for cookie in self.browser.get_cookies():
            cookies[cookie["name"]] = cookie["value"]
            cookies = {}
            for cookie in self.browser.get_cookies():
                cookies[cookie["name"]] = cookie["value"]
            print(cookies)
            print('成功获取到Cookies')
            return (username, json.dumps(cookies))

    def new_cookies(self, username, password):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        print('Generating Cookies of', username)
        self.browser.delete_all_cookies()
        self.browser.get('http://www.quanshuwang.com/')
        wait = WebDriverWait(self.browser, 20)

        try:
            user = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#htmlUserName')))
            user.send_keys(username)
            psd = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#htmlPassword')))
            psd.send_keys(password)
            submit = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="submit"].btn1')))
            submit.click()
            # time.sleep(3)
            result = self._success(username)
            if result:
                return result
        except:
            print('error2')



if __name__ == '__main__':
    pass
    # generator = WeiboCookiesGenerator()
    # generator._init_browser('Chrome')
    # generator.new_cookies('wuasdf1', '123')
