# --*-- coding: utf-8 --*--

import urllib, urllib2, cookielib
import requests
import re
import httplib
import json
import datetime
import time

from requests import session

class FacebookCookies():

    def __init__(self, *args, **kwargs):

        if len(args) == 0:
            self.email = ''
            self.password = ''
        else:
            self.email = args[0]
            self.password = args[1]

        self.USER_ID = '{user_id}'
        self.PAGE_ID = '{page_id}'

        self.base_headers = {
            'Origin':'https://www.facebook.com',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
            'accept': '*/*',
            'accept-encoding' : 'utf-8',
            'accept-language' : 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4'
        }

        self.base_body = {
            '__user':self.USER_ID,
            '__srp_t':self.get_now_epochtime(),
            '__dyn':'',
            '__a':1,
            'page_id':self.PAGE_ID
        }

    def get_now_epochtime(self):

        dtime = datetime.datetime.now()
        ans_time = time.mktime(dtime.timetuple())
        return ans_time

    #base_header에 로그인을 통해 얻은 cookie를 더한 후 반환한다.
    def get_headers(self):

        cookies = self.set_cookies()

        if cookies == -1:
            return -1

        cookie = ''
        for k in cookies:
            cookie += k+'='+cookies[k]+'; '

            self.base_headers['cookie'] = cookie

        return self.base_headers

    def set_cookies(self):

        ACCESS_TOKEN = '{access_token}'
        next_url = 'https://www.facebook.com/?stype=lo&jlou=Aff-D-kUIYh4TJ2dqh495HNbGErRsMkjPF3OBmzeChgffEo7VbK9pVTGP8-dHG4DSUDN3aFh68QMLW9Mx2VzFFlQeZJpwBRIi1nzXglS_2OL9g&smuh=44783&lh=Ac923nf8jlSN07kz'
        login_data = {'email': self.email, 'pass': self.password, 'next': next_url}

        #fr cookie를 가져올 수 있다.
        session = requests.Session()
        session.cookies.get_dict()
        response = session.get('https://www.facebook.com/login.php?login_attempt=1&lwv=110')
        se = session.cookies.get_dict()

        #try login
        body = urllib.urlencode(login_data)
        headers = self.base_headers.copy()
        headers.update(Cookie = 'locale=ko_KR; datr=ZigEfTZnFJKTlwgcnxpZEACeZ; fr='+se['fr']+'; _js_reg_fb_ref=https%3A%2F%2Fwww.facebook.com%2F%3Fstype%3Dlo%26jlou%3DAff-D-kUIYh4TJ2dqh495HNbGErRsMkjPF3OBmzeChgffEo7VbK9pVTGP8-dHG4DSUDN3aFh68QMLW9Mx2VzFFlQeZJpwBRIi1nzXglS_2OL9g%26smuh%3D44783%26lh%3DAc923nf8jlSN07kz; _js_reg_fb_gate=https%3A%2F%2Fwww.facebook.com%2F%3Fstype%3Dlo%26jlou%3DAff-D-kUIYh4TJ2dqh495HNbGErRsMkjPF3OBmzeChgffEo7VbK9pVTGP8-dHG4DSUDN3aFh68QMLW9Mx2VzFFlQeZJpwBRIi1nzXglS_2OL9g%26smuh%3D44783%26lh%3DAc923nf8jlSN07kz; wd=690x699')

        base_cookies = { header.split('=')[0]: header.split('=')[1] for header in headers['Cookie'].split('; ')}

        conn = httplib.HTTPSConnection('www.facebook.com')
        conn.request('POST', '/login.php?login_attempt=1&lwv=110', body=body, headers=headers)
        res = conn.getresponse()
        headers = res.getheaders()

        results = {header[0]: header[1] for header in headers}

        #유효성 검사
        if re.search('c_user', results['set-cookie']) == None:
            return -1

        #로그인을 통해 얻은 cookie에서 필요없는 cookie삭제
        cookies = re.sub('httponly.?','',re.sub('path=\/;', '',results['set-cookie']))
        cookies = re.sub('Max-Age=.*?;', '', cookies)
        cookies = re.sub('domain=.facebook.com.', '', cookies)
        cookies = re.sub('expires=.*?;', '', cookies)

        cookies = re.findall('(.*?=.*?;)', cookies)

        for cookie in cookies:
            cookie = cookie.strip()
            cookie = re.sub('secure.','',cookie)
            if re.search('(.*?)=deleted;', cookie) != None:
                key = re.findall('(.*?)=deleted', cookie)[0]
                try:
                    del base_cookies[key]
                except:
                    pass
            else:
                cookie = cookie.strip()
                cookie = re.findall('(.*)=(.*);', cookie)[0]
                base_cookies.update({cookie[0]:cookie[1]})

        base_cookies.update(presence = ACCESS_TOKEN)
        base_cookies.update(p='-2')

        return base_cookies

    #fb_dtsg --> 페북 세션(html 코드 안에 input type =hidden name=fb_dtsg 이런 식으로 들어있음)
    #fb_dtsg가 있어야 다른 페이지를 로딩할때 데이터를 가져올 수 있다.
    def get_fb_dtsg(self):

        self.base_headers['upgrade-insecure-requests'] = 1
        conn = httplib.HTTPSConnection('www.facebook.com')
        conn.request('GET', '/dietnote/', headers=self.base_headers)
        res = conn.getresponse()

        contents = res.read()

        fb_dtsg = re.findall('fb_dtsg.+?value="([^"]+)"', contents)[0]

        return fb_dtsg



