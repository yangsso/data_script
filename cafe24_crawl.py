# -*- coding: utf-8 -*-

import datetime #날짜
import hashlib #
import httplib #통신
import re #정규식 처리
import sys 
import threading
import urllib
import MySQLdb

class Cafe24Login(object):
    def __init__(self, username, pwd):
        phpsessid = 'mysessionid{}'.format(str(datetime.date.today()))                                           
        phpsessid = hashlib.md5(phpsessid).hexdigest()                                                                           
        self.base_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',                                                 
            'Cookie': 'PHPSESSID={}'.format(phpsessid),                                                                  
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
            'Origin': 'https://eclogin.cafe24.com'                                                                           
        }
        self.username = username
        self.pwd = pwd

    def print_userinfo(self):
        print "%s %s" % (self.username, self.pwd)

    def login(self):
        self.use_auth()
        enc_data = self.get_enc_data()
        login_params = self.user_id_check(enc_data)
        login_url = self.com_login(login_params)
        return self.final_login(login_url)


    def use_auth(self):                                                                                                                          
        body = urllib.urlencode(dict(mall_id=self.username))                                                                  
        headers = self.base_headers.copy()                                                                                                        
        conn = httplib.HTTPSConnection('eclogin.cafe24.com')                                                         
        conn.request('POST', '/Shop/?url=MallUseAuth', body, headers)                                        
        response = conn.getresponse()                                                                                                        
        cookie = response.getheader('set-cookie').split('; ')[0]                                                 
        self.base_headers['Cookie'] += '; {}'.format(cookie)                                                                  
        conn.close() 


    def get_enc_data(self):                                                                                                
        body = urllib.urlencode(dict(userid_hidden=1, login_mode=1, userid=self.username, 
                mall_id=self.username, userpasswd=self.pwd, is_multi='F', url='Run'))
        headers = self.base_headers.copy()                                                                                                        
        headers.update({'Referer': 'https://eclogin.cafe24.com/Shop/'})                                  
        conn = httplib.HTTPSConnection('eclogin.cafe24.com')                                                         
        conn.request('POST', '/Shop/index.php', body=body, headers=headers)                          
        response = conn.getresponse()                                                                                                        
        data = response.read()                                                                                                                   
        conn.close()                                                                                                                                         
        enc_data = data.split("EncData' value='")[1].split("'")[0]                                           
        return enc_data                                                                                                                                  

    def user_id_check(self, enc_data):                                                                                                        
        body = urllib.urlencode(dict(is_auth='T', CAFE24EncData=enc_data))                  
        headers = self.base_headers.copy()                                                                                           
        headers.update({'Referer': 'https://eclogin.cafe24.com/Shop/index.php'})        
        conn = httplib.HTTPSConnection('intoit.cafe24.com')                                                 
        conn.request('POST', '/admin/php/user_id_check.php', body, headers)                 
        response = conn.getresponse()                                                                                           
        data = response.read()                                                                                                          
        conn.close()                                                                                                                                
        params = re.findall(r'input.*?name="(.*?)".*?value="(.*?)"', data)                  
        return dict(params)                                                                                                                 
                                                                                                                                                                
    def com_login(self, params):                                                                                                                  
        body = urllib.urlencode(params)                                                                                         
        headers = self.base_headers.copy()                                                                                           
        headers.update({                                                                                                                        
                'Referer': 'https://intoit.cafe24.com/admin/php/user_id_check.php',         
                'Origin': 'https://intoit.cafe24.com'                                                                   
        })                                                                                                                                                  
        conn = httplib.HTTPSConnection('user.cafe24.com')                                                   
        conn.request('POST', '/comLogin/?action=comLogin', body, headers)                   
        response = conn.getresponse()                                                                                           
        data = response.read()                                                                                                          
        conn.close()                                                                                                                                
        return data.split("'")[1]                                                                                                   
                                                                                                                                                                
                                                                                                                                                                
    def final_login(self, login_url):                                                                                                         
        login_path = login_url.split('cafe24.com')[1]                                                           
        headers = self.base_headers.copy()                                                                                           
        headers.update(dict(referer='https://user.cafe24.com/comLogin/?action=comLogin'))
        conn = httplib.HTTPSConnection('intoit.cafe24.com')                                                 
        conn.request('GET', login_path, headers=headers)                                                        
        response = conn.getresponse()                                                                                           
        cookies = dict(re.findall(r'\s?(.*?)=(.*?); path.*?(?:,|$)', response.getheader('set-cookie')))
        response.read()                                                                                                                         
        conn.close()                                                                                                                                
        return '; '.join(['{}={}'.format(k, v) for k, v in cookies.items()])


