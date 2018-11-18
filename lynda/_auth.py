#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

Author  : Nasir Khan (r0ot h3x49)
Github  : https://github.com/r0oth3x49
License : MIT


Copyright (c) 2018 Nasir Khan (r0ot h3x49)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

from pprint import pprint
from ._compat import (
        re,
        sys,
        json,
        requests,
        conn_error,
        HEADERS,
        LOGOUT_URL,
        ParseCookie,
        USER_LOGIN_URL,
        AJAX_USERNAME,
        AJAX_PASSWORD,
        ORG_LOGIN_URL,
        AJAX_ORGNIZATION,
        )
from ._colorized import *

class LyndaAuth(object):

    def __init__(self, username='', password='', organization=''):
        self.username = username
        self.password = password
        self.organization = organization
        self._session = requests.Session()

    def _user_login_steps(self, form_html, fallback_action_url, extra_form_data, referrer_url):
        csrftoken = re.search(r'name="-_-"\s+value="(.*)"', form_html)
        if csrftoken:
            data = {'-_-' : csrftoken.group(1)}
            if data and isinstance(data, dict):
                data.update(extra_form_data)
            try:
                webpage = self._session.post(fallback_action_url, data=data, headers={'Referer': referrer_url, 'X-Requested-With': 'XMLHttpRequest'}).json()
            except conn_error as e:
                sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
                sys.exit(0)
            else:
                return webpage, fallback_action_url
        else:
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Failed to extract csrftoken.\n")
            sys.exit(0)

    def _user_session(self):
        try:
            webpage = self._session.get(USER_LOGIN_URL, headers={'User-Agent' : HEADERS.get('User-Agent')}).text
        except conn_error as e:
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
            sys.exit(0)
        else:
            sigin_form  = re.search(r'(?s)(<form[^>]+?data-form-name=["\']signin["\'][^>]*>(?P<form>.+?)</form>)', webpage)
            if sigin_form:
                form_html = sigin_form.group('form')
                sigin_webpage, signin_url = self._user_login_steps(form_html, AJAX_PASSWORD, {'email': self.username}, USER_LOGIN_URL)
                password_form = sigin_webpage.get('body')
                if not password_form:
                    sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Lynda Says : Sorry, we do not recognize that email or username.\n")
                    sys.exit(0)
                response, url = self._user_login_steps(password_form, AJAX_USERNAME, {'email': self.username, 'password': self.password}, signin_url)
                response_text = response.get('UserID') if response.get('UserID') else response.get('password')
                if response_text != "The username or password is invalid.":
                    self._session.headers.update({'User-Agent' : HEADERS.get('User-Agent')})
                    return self._session
                else:
                    return None
            else:
                sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Failed to extract login-form..\n")
                sys.exit(0)

    def _org_login_steps(self, fallback_action_url, extra_form_data, extra_headers, referrer_url):
        
        if fallback_action_url == AJAX_ORGNIZATION:
            HEADERS.update({'-_-' : extra_headers.get('-_-'), 'Referer' : referrer_url})
        else:
            HEADERS.update(extra_headers)
            HEADERS.pop('-_-')

        try:
            response = self._session.post(fallback_action_url, data=extra_form_data, headers=HEADERS)
        except conn_error as e:
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
            sys.exit(0)
        else:
            if fallback_action_url == AJAX_ORGNIZATION:
                response = response.json()
                _org_url, referrer = response.get('RedirectUrl').replace('http', 'https') if not 'https' in response.get('RedirectUrl') else response.get('RedirectUrl'), response.get('RedirectUrl')
                return _org_url, referrer
            else:
                response = response.text
                logged_in_username = re.search(r'data-qa="eyebrow_account_menu">(.*)</span>', response)
                if logged_in_username:
                    return logged_in_username.group(1), None
                else:
                    return None, None

    def _organization_session(self):
        try:
            webpage = self._session.get(ORG_LOGIN_URL, headers={'User-Agent' : HEADERS.get('User-Agent')}).text
        except conn_error as e:
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
            sys.exit(0)
        else:
            data = re.search(r'var\s+lynda\s+=\s+(?P<data>{.+?});', webpage)
            if data:
                json_data = json.loads(data.group(1))
                organization_login_url, referrer_url = self._org_login_steps(AJAX_ORGNIZATION, {'org' : self.organization}, json_data, ORG_LOGIN_URL)
                try:
                    webpage = self._session.get(referrer_url).text
                except conn_error as e:
                    sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
                    sys.exit(0)
                else:
                    csrftoken = re.search(r'name="seasurf"\s+value="(.*)"', webpage)
                    if csrftoken:
                        csrftoken = csrftoken.group(1)
                        login_data   = dict(
                                    libraryCardNumber=self.username,
                                    libraryCardPin=self.password,
                                    libraryCardPasswordVerify="",
                                    org=self.organization,
                                    currentView="login",
                                    seasurf=csrftoken
                                )
                        response, _ = self._org_login_steps(organization_login_url, login_data, {'Referer' : referrer_url}, referrer_url)
                        if response:
                            self._session.headers.update({'User-Agent' : HEADERS.get('User-Agent')})
                            return self._session
                        else:
                            return None
                    else:
                        sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Failed to extract csrftoken.\n")
                        sys.exit(0)
            else:
                sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Failed to extract login-form..\n")
                sys.exit(0)

    def _cookie_session_step(self, raw_cookies):
        cookies = {}
        cookie_parser = ParseCookie()
        try:
            cookie_string = re.search(r'Cookie:\s*(.+)\n', raw_cookies, flags=re.I).group(1)
        except:
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Cookies error, Request Headers is required.\n")
            sys.stdout.write(fc + sd + "[" + fm + sb + "i" + fc + sd + "] : " + fg + sb + "Copy Request Headers for single request to a file, while you are logged in.\n")
            sys.exit(0)
        cookie_parser.load(cookie_string)
        for key, cookie in cookie_parser.items():
            cookies[key] = cookie.value
        return cookies

    def _cookies_session(self, cookies):
        auth_cookies = self._cookie_session_step(raw_cookies=cookies)
        if auth_cookies:
            self._session.cookies.update(auth_cookies)
            return self._session
        else:
            return None

    def authenticate(self, cookies=''):
        if cookies:
            return self._cookies_session(cookies=cookies)
        if self.organization:
            return self._organization_session()
        else:
            return self._user_session()

