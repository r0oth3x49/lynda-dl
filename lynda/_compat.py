#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if sys.version_info[:2] >= (3, 0):
    import requests,re
    import urllib.request as compat_urllib
    from urllib.request import Request as compat_request
    from urllib.request import urlopen as compat_urlopen
    from urllib.error import HTTPError as compat_httperr
    from urllib.error import URLError as compat_urlerr
    from urllib.parse import urlparse as compat_urlparse
    from urllib.request import build_opener as compat_opener
    uni, pyver = str, 3
    
else:
    import requests,re
    import urllib2 as compat_urllib
    from urllib2 import Request as compat_request
    from urllib2 import urlopen as compat_urlopen
    from urllib2 import URLError as compat_urlerr
    from urllib2 import HTTPError as compat_httperr
    from urllib2 import urlparse as compat_urlparse
    from urllib2 import build_opener as compat_opener
    uni, pyver = unicode, 2


org_url     = "https://www.lynda.com/signin/organization"
xorg_url    = "https://www.lynda.com/ajax/signin/organization"
sigin_url   = 'https://www.lynda.com/signin'
passw_url   = 'https://www.lynda.com/signin/password'
user_url    = 'https://www.lynda.com/signin/user'
logout      = "https://www.lynda.com/signout"
course_url  = "https://www.lynda.com/ajax/player?courseId=%s&type=course"
get_url     = "https://www.lynda.com/ajax/course/%s/%s/play"
ex_url      = "https://www.lynda.com/ajax/course/%s/0/getupselltabs"
cc_url      = "https://www.lynda.com/ajax/player?videoId={video_id}&type=transcript"
user_agent  = "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)"
std_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)',
    'X-Requested-With': 'XMLHttpRequest',
    'Host': 'www.lynda.com'}

__ALL__ =[
    "compat_request",
    "requests",
    "logout",
    "re",
    "compat_urllib",
    "compat_urlparse",
    "compat_urlerr",
    "compat_httperr",
    "sigin_url",
    "passw_url",
    "user_url",
    "org_url",
    "course_url",
    "get_url",
    "ex_url",
    "std_headers",
    "compat_urlopen",
    "compat_opener",
    "user_agent",
    "cc_url",
    "xorg_url",
	"pyver"
    ]
