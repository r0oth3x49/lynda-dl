#!/usr/bin/python

import os
import sys
import json
import time
from pprint import pprint
from .colorized import *
from ._compat import (
    re,
    logout,
    ex_url,
    cc_url,
    get_url,
    requests,
    org_url,
    user_url,
    sigin_url,
    passw_url,
    course_url,
    std_headers,
    compat_urlparse,
    xorg_url,
    )
from ._sanitize import (
            slugify,
            sanitize,
            SLUG_OK
)

early_py_version = sys.version_info[:2] < (2, 7)
session = requests.Session()

class LyndaInfoExtractor:

    _TIMECODE_REGEX = r'\[(?P<timecode>\d+:\d+:\d+[\.,]\d+)\]'

    def match_id(self, url):
        course_name = url.split("/")[-2]
        if course_name:
            return course_name

    def _sanitize(self, unsafetext):
        text = sanitize(slugify(unsafetext, lower=False, spaces=True, ok=SLUG_OK + '()-_-'))
        return text

    def _get_org_csrf_token(self, login_url):
        try:
           response = session.get(login_url)
           match = re.search(r'name="seasurf"\s+value="(.*)"', response.text)
           return match.group(1)
        except AttributeError:
            session.get(logout)
            response = re.search(r'name="seasurf"\s+value="(.*)"', response.text)
            return match.group(1)
        
    def _hidden_inputs(self, form_html):
        try:
           match = re.search(r'name="-_-"\s+value="(.*)"', str(form_html))
           return {"-_-":match.group(1)}
        except AttributeError:
            session.get(logout)
            response = re.search(r'name="-_-"\s+value="(.*)"', str(form_html))
            return {"-_-":match.group(1)}

    def _login_step(self, form_html, fallback_action_url, extra_form_data, referrer_url):
        action_url = fallback_action_url
        form_data = self._hidden_inputs(form_html)
        form_data.update(extra_form_data)

        try:
            response = session.post(action_url, data=form_data,
                              headers={
                                  'Referer': referrer_url,
                                  'X-Requested-With': 'XMLHttpRequest',
                                  }).json()
        except Exception as e:
            print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fr + sb + "Error : {}.".format(e))
            exit(0)

        return response, action_url

    def _extract_organization_url(self, org):
        try:
            resp = session.get(org_url).text
            json_data = json.loads(re.search(r'lynda\s*=\s*(?P<data>{.+?});', resp).group(1))
        except:
            print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fr + sb + "failed to extract csrf token for organization ..")
            exit(0)
        else:
            headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)',
                       '-_-' : json_data.get('-_-'), 'Referer' : org_url, 'X-Requested-With' : 'XMLHttpRequest'}
            data = {'org' : org}
            try:
                resp = session.post(xorg_url, data=data, headers=headers).json()
            except:
                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fr + sb + "failed to extract json url for organization ..")
                exit(0)
            else:
                url, referer = resp.get('RedirectUrl').replace('http', 'https') if not 'https' in resp.get('RedirectUrl') else resp.get('RedirectUrl'), resp.get('RedirectUrl')
                return url, referer
            

    def login(self, user, passw, org=None):
        if org:
            sys.stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Trying to login as organization : " + fm + sb +"(%s)" % (org) +  fg + sb +"...\n")
            organization = org
            lib_card_num = user
            lib_card_pin = passw
            login_url, referer = self._extract_organization_url(organization)
            csrftoken = self._get_org_csrf_token(referer)
            login_data   = dict(
                                    libraryCardNumber=str(lib_card_num),
                                    libraryCardPin=str(lib_card_pin),
                                    libraryCardPasswordVerify="",
                                    org=str(organization),
                                    currentView="login",
                                    seasurf=csrftoken
                                )
            std_headers['Referer'] = referer
            response    = session.post(login_url, data=login_data, headers=std_headers)
            response_text = response.text
            try:
                name = re.search(r'data-qa="eyebrow_account_menu">(.*)</span>', response_text).group(1)#response_text.split('<span class="account-name" data-qa="eyebrow_account_menu">')[1].split('</span>')[0]
            except:
                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fr + sb + "Logged in failed.")
                sys.exit(0)
            else:
                # print(name)
                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Logged in successfully.")
        else:
            username    = user
            sys.stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Trying to login as user : " + fm + sb +"(%s)" % (username) +  fg + sb +"...\n")
            password    = passw
            sigin_page  = session.get(sigin_url)
            sigin_form  = re.search(r'(?s)(<form[^>]+data-form-name=["\']signin["\'][^>]*>.+?</form>)',sigin_page.text)
            form_html   = sigin_form.group()
            sign_page, signin_url = self._login_step(form_html, passw_url, {'email': username}, sigin_url)
            try:
                password_form = sign_page["body"]
            except KeyError:
                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fr + sb + "Lynda Says : Sorry, we do not recognize that email or username.")
                sys.exit(0)
            response, url = self._login_step(password_form, user_url, {'email': username, 'password': password}, signin_url)
            response_text = response.get('UserID') if response.get('UserID') else response.get('password')
            if response_text != "The username or password is invalid.":
                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Logged in successfully.")
            else:
                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fr + sb + "Lynda Says : The password is invalid")
                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fr + sb + "Logged in failed.")
                sys.exit(0)


    def logout(self):
        print (fc + sd + "\n[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloaded course information webpages successfully..")
        print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Trying to logout now...")
        session.get(logout)
        print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Logged out successfully.")


    def _generate_dirname(self, title):
        ok = re.compile(r'[^/]')

        if os.name == "nt":
            ok = re.compile(r'[^\\/:*?"<>|]')

        dirname = "".join(x if ok.match(x) else "_" for x in title)
        return dirname
        

    def course_videos_count(self, json):
        count = 0
        unaccessible_videos = 0
        for chapter in json["Chapters"]:
            for video in chapter.get('Videos', []):
                if video.get('HasAccess') == False:
                    unaccessible_videos += 1
                    continue
                count += 1
                
        return count
    
    def ExtractExerciseFile(self, courseId, courseName):
        fileZip = {}
        lUrl = []
        cUrl = ex_url % (courseId)
        try:
            r           = session.get(cUrl).json()
            ex          = r.get("exercisetab")
            matchUrl    = re.findall('href="(.+)"\srole', ex)
            matchName   = re.findall('span\sclass="exercise-name">(.+)</span', ex)
        except:
            return "nofile"
        else:
            for fzip in matchUrl:
                fUrl    = "https://www.lynda.com%s" % (fzip)
                r       = session.get(fUrl, stream=True)
                zip_url = r.url
                lUrl.append(zip_url)
            fileZip     = dict(zip(matchName, lUrl))
            return fileZip
        
    def Progress(self, iteration, total, prefix = '' , fileSize='' , downloaded = '' , barLength = 100):
        filledLength    = int(round(barLength * iteration / float(total)))
        percents        = format(100.00 * (iteration / float(total)), '.2f')
        bar             = '=' * filledLength + '-' * (barLength - filledLength)
        sys.stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + 'Extracting ' + fg + sb + '(' + str(fileSize) + '/' + str(downloaded) + ') |' + bar + fg + sb + '| ' + percents + '%                                      \r')
        sys.stdout.flush()

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

    def _get_subtitles(self, video_id):
        url =  cc_url.format(video_id=video_id)
        subs = session.get(url).json()
        if subs:
            return {'en' : {'data': self._fix_subtitles(subs)}}
        else:
            return {}
        

    def real_extract(self, url, course_name):

        rootDir             = course_name

        course_id           = (url.split('/')[-1]).split('-')[0]
        curl                = course_url % (course_id)
        course              = session.get(curl).json()
        unaccessible_videos = 0

        lynda_dict = {}
        num_lect =  self.course_videos_count(course)
        sys.stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Found (%s) lectures\n" % (num_lect))
        counter = 0

        
        for chapter in course["Chapters"]:
            chap_num        = chapter.get('ChapterIndex')
            temp_           = self._sanitize(chapter.get('Title'))
            temp_name       = self._generate_dirname(temp_)
            chap            = (temp_name.split('.', 1)[-1] if '.' else temp_name)
            chap_title      = "{0:02d} {1!s}".format(chap_num, chap)
            if chap_num not in lynda_dict:
                lynda_dict[chap_title] = {}
            for video in chapter.get('Videos', []):
                counter += 1
                if video.get('HasAccess') == False:
                    unaccessible_videos += 1
                    continue
                self.Progress(counter, num_lect, fileSize = str(num_lect), downloaded = str(counter), barLength = 40)
                video_id        = video.get('ID')
                lect_num        = video.get('VideoIndex')
                lecture         = self._sanitize(video.get('Title'))
                lecture_title   = "{0:03d} {1!s}".format(lect_num, lecture)
                captions        = self._get_subtitles(video_id)
                if lect_num not in lynda_dict[chap_title]:
                    lynda_dict[chap_title][lecture_title] = {}
                    lurl            = get_url % (course_id, video_id)
                    lecture_json    = session.get(lurl).json()
                    if isinstance(captions, dict) and len(captions) != 0:
                        caption_title = "{0:03d} {1!s}.srt".format(lect_num, lecture)
                        lynda_dict[chap_title][caption_title] = captions
                    for formats in lecture_json:
                        urls = formats.get('urls')
                        cdn  = formats.get('name')
                        if not isinstance(urls, dict):
                            continue
                        if cdn not in lynda_dict[chap_title][lecture_title]:
                            lynda_dict[chap_title][lecture_title][cdn] = urls
        return lynda_dict
