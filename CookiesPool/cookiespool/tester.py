import json
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
from cookiespool.db import *
from cookiespool.generator import xiaoshuoCookiesGenerator


class ValidTester(object):
    def __init__(self, name='default'):
        self.name = name
        self.cookies_db = CookiesRedisClient(name=self.name)
        self.account_db = AccountRedisClient(name=self.name)

    def test(self, account, cookies):
        raise NotImplementedError

    def run(self):
        global cc
        cc = 1
        print('开始测试赛！！！')
        accounts = self.cookies_db.all()
        for account in accounts:
            cc +=1
            if cc>13:
                break
            print('成功获取账户！！！！')
            username = account.get('username')
            cookies = self.cookies_db.get(username)
            self.test(account, cookies)


class xiaoshuoValidTester(ValidTester):
    def __init__(self, name='xiaoshuo'):
        ValidTester.__init__(self, name)

    def test(self, account, cookies):

        """直接删除"""
        print('Testing Account', account.get('username'))
        self.cookies_db.delete(account.get('username'))
        print('Deleted User', account.get('username'))
        return None

        """请求百度测试"""
        # try:
        #     cookies = json.loads(cookies)
        # except TypeError:
        #     # Cookie 格式不正确
        #     print('Invalid Cookies Value', account.get('username'))
        #     self.cookies_db.delete(account.get('username'))
        #     print('Deleted User', account.get('username'))
        #     return None
        # try:
        #     response = requests.get('http://www.quanshuwang.com/book/172/172154/50408503.html', cookies=cookies)
        #     if response.status_code == 200:
        #         print('ok!')
        #
        #     else:
        #         # Cookie已失效
        #         print('Invalid Cookies', account.get('username'))
        #         self.cookies_db.delete(account.get('username'))
        #         print('Deleted User', account.get('username'))
        # except ConnectionError as e:
        #     print('Error', e.args)
        #     print('Invalid Cookies', account.get('username'))


class MxiaoshuoValidTester(ValidTester):
    def __init__(self, name='weibo'):
        ValidTester.__init__(self, name)

    def test(self, account, cookies):
        print('Testing Account', account.get('username'))
        try:
            cookies = json.loads(cookies)
        except TypeError:
            # Cookie 格式不正确
            print('Invalid Cookies Value', account.get('username'))
            self.cookies_db.delete(account.get('username'))
            print('Deleted User', account.get('username'))
            return None
        try:
            test_url = 'http://www.quanshuwang.com/book_172154.html'
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print('Valid Cookies', account.get('username'))
            else:
                print(response.status_code, response.headers)
                print('Invalid Cookies', account.get('username'))
                self.cookies_db.delete(account.get('username'))
                print('Deleted User', account.get('username'))
        except ConnectionError as e:
            print('Error', e.args)
            print('Invalid Cookies', account.get('username'))

if __name__ == '__main__':
    tester = xiaoshuoValidTester()
    tester.run()
