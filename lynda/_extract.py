#!/usr/bin/python
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

import re
import os
import sys
import json

from pprint  import  pprint
from ._auth  import  LyndaAuth
from ._compat import (
            re,
            time,
            encoding,
            conn_error,
            LOGOUT_URL,
            COURSE_URL,
            VIDEO_URL,
            CAPTIONS_URL,
            EXERCISE_FILES_URL,
            )
from ._sanitize import (
            slugify,
            sanitize,
            SLUG_OK
            )
from ._colorized import *
from ._progress import ProgressBar


class Lynda(ProgressBar):

    _TIMECODE_REGEX = r'\[(?P<timecode>\d+:\d+:\d+[\.,]\d+)\]'
    _VALID_URL = r'''https?://(?:www|m)\.(?:lynda\.com|educourse\.ga)/(?P<course_path>(?:[^/]+/){2,3}(?P<course_id>\d+))-2\.html'''
    _VALID_COURSE_URL = r'''(?x)(?:(.+)/(?P<path>[a-zA-Z0-9_-]+)|(?P<course_path>[a-zA-Z0-9_-]+))/(?P<course_name>[a-zA-Z0-9_-]+)/(?P<course_id>\d+)'''
    _VIDEO_URL = r'''(?x)https?://(?:www\.)?(?:lynda\.com|educourse\.ga)/(?:(?:[^/]+/){2,3}(?P<course_id>\d+)|player/embed)/(?P<video_id>\d+)'''
    _EXERCISE_FILES_REGEX = r'''(?i)<a[^>]+?/ajax/(?P<download_url>(?:[^/]+/){2,6}(?P<file_id>\d+))[^>]*>(?is)<span[^>]+?class=(["\'])exercise-name\1*[^>]*>(?P<filename>.+?)</span>'''#(?i)<span[^>]+?class=(["\'])file-size\1*[^>]*>\((?P<size>.+?)\)</span>'''

    def __init__(self):
        self._session = ''

    def _extract_course_info(self, url):
        mobj = re.match(self._VALID_URL, url)
        if mobj:
            mobject = re.match(self._VALID_COURSE_URL, mobj.group('course_path'))
            if mobject:
                course_name, course_id = mobject.group('course_name'), mobject.group('course_id')
            if not mobject:
                course_name, course_id = mobj.group('course_path').split('/')[-2], mobj.group('course_id')
        if not mobj:
            mobj = re.match(self._VIDEO_URL, url)
            course_name, course_id = None, mobj.group('course_id')
        if not mobj:
            sys.stdout.write('\033[2K\033[1G' + fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Course URL seems incorrect.\n")
            exit(0)
        return course_name, course_id

    def _clean(self, text):
        ok = re.compile(r'[^\\/:*?"<>|]')
        text = "".join(x if ok.match(x) else "_" for x in text)
        text = (text.lstrip('0123456789.- ')).rstrip('. ')
        return text

    def _sanitize(self, unsafetext):
        text = sanitize(slugify(unsafetext, lower=False, spaces=True, ok=SLUG_OK + '().[]'))
        return text

    def _login(self, username='', password='', organization='', cookies=''):
        if not cookies:
            auth = LyndaAuth(username=username, password=password, organization=organization)
            self._session = auth.authenticate()
        if cookies:
            auth = LyndaAuth()
            self._session = auth.authenticate(cookies=cookies)
        if self._session is not None:
            return {'login' : 'successful'}
        else:
            return {'login' : 'failed'}

    def _logout(self):
        if self._session:
            self._session.get(LOGOUT_URL)
        return

    def _fix_subtitles(self, subs):
        srt = ''
        seq_counter = 0
        for pos in range(0, len(subs) - 1):
            seq_current = subs[pos]
            m_current = re.match(self._TIMECODE_REGEX, seq_current['Timecode'])
            if m_current is None:
                continue
            seq_next = subs[pos + 1]
            m_next = re.match(self._TIMECODE_REGEX, seq_next['Timecode'])
            if m_next is None:
                continue
            appear_time = m_current.group('timecode')
            disappear_time = m_next.group('timecode')
            text = seq_current['Caption'].strip()
            if text:
                seq_counter += 1
                srt += '%s\r\n%s --> %s\r\n%s\r\n\r\n' % (seq_counter, appear_time, disappear_time, text)
        if srt:
            return srt

    def _extract_asset_download_url(self, url):
        try:
            response = self._session.get(url, stream=True)
        except conn_error as e:
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
            sys.exit(0)
        return {'type' : 'file', 'file_size' : int(response.headers.get('Content-Length')), 'download_url' : response.url, 'extension' : response.headers.get('Content-Type').split('/')[-1]}

    def _extract_assets(self, course_id):
        url =  EXERCISE_FILES_URL.format(course_id=course_id)
        _temp = []
        try:
            response = self._session.get(url).json()
        except conn_error as e:
            print("")
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
            sys.exit(0)
        except ValueError as e:
            print("")
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "JSONDecodeError : it seems your cookies got expired, provide again.\n")
            sys.exit(0)
        if response and isinstance(response, dict):
            exercise_tab = (response.get('exercisetab')).replace('\r', '').replace('\n', '').replace('\t', '')
            _temp = [m.groupdict() for m in re.finditer(self._EXERCISE_FILES_REGEX, exercise_tab)]
            for entry in _temp:
                entry.update(self._extract_asset_download_url(url='https://www.lynda.com/ajax/{href}'.format(href=entry.get('download_url'))))

        return _temp

    def _extract_subtitles(self, video_id):
        url =  CAPTIONS_URL.format(video_id=video_id)
        try:
            subs = self._session.get(url).json()
        except conn_error as e:
            print("")
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
            sys.exit(0)
        except ValueError as e:
            print("")
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "JSONDecodeError : it seems your cookies got expired, provide again.\n")
            sys.exit(0)
        if subs:
            return {
                    'type' : 'subtitle',
                    'language' : 'en',
                    'extension' : 'srt',
                    'subtitle_data' : self._fix_subtitles(subs),
                    }
        else:
            return {
                    'type' : 'subtitle',
                    'language' : 'en',
                    'extension' : 'srt',
                    'subtitle_data' : None,
                    }

    def _max(self, data):
        return {'url' : [x['url'] for x in data if x['size'] == max([x['size'] for x in data])][0]}

    def _get_max_stream(self, streams):
        cl = 'content-length'
        try:
            fsize = self._session.get(streams.get('url'), stream=True).headers[cl]
        except conn_error as e:
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
            sys.exit(0)
        return {'url' : streams.get('url'), 'size' : int(fsize)}

    def _extract_sources(self, course_id, lecture_id):
        _temp = []
        url = VIDEO_URL.format(course_id=course_id, video_id=lecture_id)
        try:
            play = self._session.get(url).json()
        except conn_error as e:
            print("")
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
            sys.exit(0)
        except ValueError as e:
            print("")
            sys.stdout.write(fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "JSONDecodeError : it seems your cookies got expired, provide again.\n")
            sys.exit(0)
        if play and isinstance(play, list):
            _best_resolution = [{'url' : s['urls'].get('720')} for s in play if s['urls'].get('720')]
            _max_stream = self._max(list(map(self._get_max_stream, _best_resolution))) if _best_resolution and isinstance(_best_resolution, list) else {}
            if _max_stream and isinstance(_max_stream, dict):
                cdn = 'akamai' if 'akamaihd.net' in _max_stream.get('url') else 'edgecast'
                _data_720 = {'type' : cdn, 'height' : 720, 'width' : 1280, 'extension' : 'mp4', 'download_url' : _max_stream.get('url')}
                _temp.append(_data_720)
            for entry in play:
                urls = entry.get('urls')
                if not isinstance(urls, dict):
                    continue
                cdn = entry.get('name').lower()
                for height, dl_url in urls.items():
                    if height == '64' or height == 64:
                        continue
                    if height == '540' or height == 540:
                        width = '960'
                    if height == '720' or height == 720:
                        continue
                    if height == '360' or height == 360:
                        width = '640'
                    _temp.append({
                            'type' : cdn,
                            'height' : int(height),
                            'width' : int(width),
                            'extension' : 'mp4',
                            'download_url' : dl_url,
                        })
        return _temp

    def _real_extract(self, url=''):

        try:
            response = self._session.get(url)
        except conn_error as e:
            sys.stdout.write('\033[2K\033[1G' + fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
            sys.exit(0)
        if url != response.url:
            url = response.url

        _lynda = {}
        course_name, course_id = self._extract_course_info(url=url)
        course_url = COURSE_URL.format(course_id=course_id)
        try:
            course_json = self._session.get(course_url).json()
        except conn_error as e:
            sys.stdout.write('\033[2K\033[1G' + fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Connection error : make sure your internet connection is working.\n")
            sys.exit(0)

        course = course_json.get('Chapters')

        _lynda['course_id'] = course_json.get('ID') or course_id
        _lynda['course_title'] = self._sanitize(self._clean(course_json.get('Title'))) or course_name
        _lynda['description'] = self._sanitize(course_json.get('Description'))
        _lynda['short_description'] = self._sanitize(course_json.get('ShortDescription'))
        _lynda['assets'] = self._extract_assets(course_id)
        _lynda['assets_count'] = len(_lynda['assets'])
        _lynda['chapters'] = []


        if course:
            _lynda['total_chapters'] = len(course)
            _lynda['total_lectures'] = sum([len(chapter.get('Videos', [])) for chapter in course])

            for entry in course:
                chapter_id = entry.get('ID')
                chapter_index = entry.get('ChapterIndex')
                chapter_title = self._sanitize(self._clean(entry.get('Title'))) or self._sanitize(self._clean(entry.get('Videos', [])[0].get('Title')))
                chapter = "{0:02d} {1!s}".format(chapter_index, chapter_title)
                lectures = entry.get('Videos', [])
                if lectures and len(lectures) > 0:
                    _temp_lectures = []
                    for entry in lectures:
                        text = '\033[2K\033[1G\r' + fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Downloading course information .. "
                        self._spinner(text)
                        lecture_id = entry.get('ID')
                        lecture_index = entry.get('VideoIndex')
                        lecture_title = self._sanitize(self._clean(entry.get('Title')))
                        lecture = "{0:03d} {1!s}".format(lecture_index, lecture_title)
                        duration = entry.get('DurationInSeconds')
                        sources = self._extract_sources(course_id, lecture_id)
                        subtitles = self._extract_subtitles(lecture_id)
                        _temp_lectures.append({
                                'lecture_id' : lecture_id,
                                'lecture_index' : lecture_index,
                                'lecture_title' : lecture,
                                'sources' : sources,
                                'sources_count' : len(sources),
                                'subtitles' : subtitles,
                                'duration' : duration,
                            })
                if chapter not in _lynda['chapters']:
                    _lynda['chapters'].append({
                            'chapter_id' : chapter_id,
                            'chapter_index' : chapter_index,
                            'chapter_title' : chapter,
                            'lectures' : _temp_lectures,
                            'lectures_count' : len(_temp_lectures)
                        })

        return _lynda

