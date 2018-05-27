#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
import time
import lynda
import optparse

from sys import *
from pprint import pprint

from lynda.colorized import *
from lynda._compat import pyver
from lynda.colorized.banner import banner


getpass       = lynda.GetPass()
course_dl     = lynda.Downloader()
extract_info  = lynda.LyndaInfoExtractor()



class LyndaDownload:

    def __init__(self, url, user, passw, org=None):
        self.url    = url
        self.user   = user
        self.passw  = passw
        self.org    = org

    def login(self):
        if self.org is not None:
            extract_info.login(self.user, self.passw, self.org)
        else:
            extract_info.login(self.user, self.passw)

    def logout(self):
        extract_info.logout()

    def generate_filename(self, title):
        ok = re.compile(r'[^/]')

        if os.name == "nt":
            ok = re.compile(r'[^\\/:*?"<>|]')

        filename = "".join(x if ok.match(x) else "_" for x in title)
        return filename

    # Source taken from  http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    def printProgress(self, iteration, total, fileSize='' , downloaded = '' , rate = '' ,suffix = '', barLength = 100):
        filledLength    = int(round(barLength * iteration / float(total)))
        percents        = format(100.00 * (iteration / float(total)), '.2f')
        bar             = fc + sd + ('█' if os.name is 'posix' else '#') * filledLength + fw + sd +'-' * (barLength - filledLength)
        stdout.write('{}{}[{}{}*{}{}] : {}{}{}/{} {}% |{}{}{}| {} {}s ETA                                \r'.format(fc,sd,fm,sb,fc,sd,fg,sb,fileSize,downloaded,percents,bar,fg,sb,rate,suffix))
        stdout.flush()

    def Download(self, total, recvd, ratio, rate, eta):
        if total <= 1048576:
            TotalSize   = round(float(total) / 1024, 2)
            Receiving   = round(float(recvd) / 1024, 2)
            Size        = format(TotalSize if TotalSize < 1024.00 else TotalSize/1024.00, '.2f')
            Received    = format(Receiving if Receiving < 1024.00 else Receiving/1024.00,'.2f')
            SGb_SMb     = 'KB' if TotalSize < 1024.00 else 'MB'
            RGb_RMb     = 'KB ' if Receiving < 1024.00 else 'MB '
        else:
            TotalSize   = round(float(total) / 1048576, 2)
            Receiving   = round(float(recvd) / 1048576, 2)
            Size        = format(TotalSize if TotalSize < 1024.00 else TotalSize/1024.00, '.2f')
            Received    = format(Receiving if Receiving < 1024.00 else Receiving/1024.00,'.2f')
            SGb_SMb     = 'MB' if TotalSize < 1024.00 else 'GB'
            RGb_RMb     = 'MB ' if Receiving < 1024.00 else 'GB '
            
        Dl_Speed        = round(float(rate) , 2)
        dls             = format(Dl_Speed if Dl_Speed < 1024.00 else Dl_Speed/1024.00, '.2f')
        Mb_kB           = 'kB/s ' if Dl_Speed < 1024.00 else 'MB/s '
        (mins, secs)    = divmod(eta, 60)
        (hours, mins)   = divmod(mins, 60)
        if hours > 99:
            eta = "--:--:--"
        if hours == 0:
            eta = "%02d:%02d" % (mins, secs)
        else:
            eta = "%02d:%02d:%02d" % (hours, mins, secs)
        self.printProgress(Receiving, TotalSize, fileSize = str(Size) + str(SGb_SMb) , downloaded = str(Received) + str(RGb_RMb), rate = str(dls) + str(Mb_kB), suffix = str(eta), barLength = 40)

    def Downloader(self, url, title, path):
        out = course_dl.download(url, title, filepath=path, quiet=True, callback=self.Download)
        if isinstance(out, dict) and len(out) > 0:
            msg     = out.get('msg')
            status  = out.get('status')
            if status == 'True':
                return msg
            else:
                if msg == 'Lynda Says (HTTP Error 401 : Unauthorized)':
                    print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Lynda Says (HTTP Error 401 : Unauthorized)")
                    print (fc + sd + "[" + fw + sb + "*" + fc + sd + "] : " + fw + sd + "Try to run the lynda-dl again...")
                    exit(0)
                else:
                    return msg
        
    def InfoExtractor(self, outto=None, sub_only=False):
        current_dir = os.getcwd()
        print(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading webpage..")
        time.sleep(2)
        course_path = extract_info.match_id(self.url)
        course_id = (self.url.split('/')[-1]).split('-')[0]
        print(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Extracting course information..")
        time.sleep(0.6)
        if not outto:
            course_name = current_dir + '\\' + course_path if os.name == 'nt' else current_dir + '/' + course_path
        else:
            course_p = "%s\\%s" % (outto, course_path) if os.name == 'nt' else "%s/%s" % (outto, course_path)
            course_name = course_p
            
        print(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Downloading " + fb + sb + "'%s'" % (course_path.replace('-',' ')))
        self.login()
        print(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading course information webpages ..")
        videos_dict = extract_info.real_extract(self.url, course_path)
        fileZip = extract_info.ExtractExerciseFile(course_id, course_path)
        self.logout()
        print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Counting no of chapters..")
        time.sleep(0.3)
        if isinstance(videos_dict, dict):
            print (fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fw + sd + "Found ('%s') chapter(s).\n" % (len(videos_dict)))
            j = 1
            for chap in sorted(videos_dict):
                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fm + sb + "Downloading chapter : (%s of %s)" % (j, len(videos_dict)))
                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fw + sd + "Chapter (%s)" % (chap))
                chapter_path = course_name + '\\' + chap if os.name == 'nt' else course_name + '/' + chap
                try:
                    os.makedirs(chapter_path)
                except  Exception as e:
                    pass
                if os.path.exists(chapter_path):
                    os.chdir(chapter_path)
                print (fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fc + sd + "Found ('%s') lecture(s)." % (len(videos_dict[chap])))
                i = 1
                for lecture_name, _urls in sorted(videos_dict[chap].items()):
                    try:
                        source  = _urls.get('EDGECAST')
                    except KeyError:
                        try:
                            source  = _urls.get('AKAMAI')
                        except:
                            source = None

                    if sub_only:
                        if not source:
                            _data         = _urls['en'].get('data')
                            lecture_name  = self.generate_filename(lecture_name)
                            filepath      = os.path.join(chapter_path, lecture_name)
                            print (fc + sd + "\n[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading lecture : (%s of %s)" % (i, len(videos_dict[chap])))
                            print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading (%s)" % (lecture_name))
                            if os.path.isfile(filepath):
                                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture : '%s' " % (lecture_name) + fy + sb + "(already downloaded).")
                            else:
                                if pyver == 3:
                                    with open(lecture_name, "w", encoding="utf-8") as f:
                                        f.write(_data)
                                    f.close()
                                else:
                                    with open(lecture_name, "w") as f:
                                        f.write(_data)
                                    f.close()
                                print (fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "Downloaded  (%s)" % (lecture_name))
                        else:
                            pass
                    else:
                        if not source:
                            _data         = _urls['en'].get('data')
                            lecture_name  = self.generate_filename(lecture_name)
                            filepath      = os.path.join(chapter_path, lecture_name)
                            print (fc + sd + "\n[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading lecture : (%s of %s)" % (i, len(videos_dict[chap])))
                            print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading (%s)" % (lecture_name))
                            if os.path.isfile(filepath):
                                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture : '%s' " % (lecture_name) + fy + sb + "(already downloaded).")
                            else:
                                if pyver == 3:
                                    with open(lecture_name, "w", encoding="utf-8") as f:
                                        f.write(_data)
                                    f.close()
                                else:
                                    with open(lecture_name, "w") as f:
                                        f.write(_data)
                                    f.close()
                                print (fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "Downloaded  (%s)" % (lecture_name))
                        else:
                            try:
                                _url    = source.get('720')
                            except KeyError:
                                _url    = source.get('360')
                                
                            if _url:
                                print (fc + sd + "\n[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading lecture : (%s of %s)" % (i, len(videos_dict[chap])))
                                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading (%s)" % (lecture_name))
                                msg = self.Downloader(_url, lecture_name, chapter_path)
                                if msg == 'already downloaded':
                                    print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture : '%s' " % (lecture_name) + fy + sb + "(already downloaded).")
                                elif msg == 'download':
                                    print (fc + sd + "\n[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "Downloaded  (%s)" % (lecture_name))
                                else:
                                    print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture : '%s' " % (lecture_name) + fc + sb + "(download skipped).")
                                    print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "{}".format(msg))
                    i += 1
                j += 1
                print ('')
                os.chdir(current_dir)
        if isinstance(fileZip, dict):
            print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Counting no of files attached with this course..")
            time.sleep(0.3)
            print (fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fc + sd + "Found ('%s') lecture(s)." % (len(fileZip)))
            j = 1
            for file_name, url in sorted(fileZip.items()):
                print (fc + sd + "\n[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading file : (%s of %s)" % (j, len(fileZip)))
                print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading (%s)" % (file_name))
                msg = self.Downloader(url, file_name, course_name)
                if msg == 'already downloaded':
                    print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture : '%s' " % (lecture_name) + fy + sb + "(already downloaded).")
                elif msg == 'download':
                    print (fc + sd + "\n[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "Downloaded  (%s)" % (lecture_name))
                else:
                    print (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture : '%s' " % (lecture_name) + fc + sb + "(download skipped).")
                    print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "{}".format(msg))
                j += 1

                print ('')
        print (fc + sd + "\n[" + fm + sb + "*" + fc + sd + "] : " + fb + sb + "(%s)" % (course_path.replace('-',' ')) + fg + sb + " Downloaded successfully.")
        



def main():
    ban = banner()
    print (ban)
    us = '''%prog [-u (USERNAME/LIBRARY CARD NUMBER)][-p (PASSWORD/LIBRARY CARD PIN)]
                   [-o ORGANIZATION] COURSE_URL [-s/--sub-only] [-d DIRECTORY]'''
    version = "%prog version 1.0"
    parser = optparse.OptionParser(usage=us,version=version,conflict_handler="resolve")

    general = optparse.OptionGroup(parser, 'General')
    general.add_option(
        '-h', '--help',
        action='help',
        help='Shows the help for program.')
    general.add_option(
        '-v', '--version',
        action='version',
    help='Shows the version of program.')

    downloader = optparse.OptionGroup(parser, "Advance")
    downloader.add_option(
        "-u", "--username", 
        action='store_true',
        dest='username',\
        help="Username or Library Card Number.")
    downloader.add_option(
        "-p", "--password", 
        action='store_true',
        dest='password',\
        help="Password or Library Card Pin.")
    downloader.add_option(
        "-o", "--organization", 
        action='store_true',
        dest='org',\
        help="Organization, registered at Lynda.")
    downloader.add_option(
        "-s","--sub-only", 
        action='store_true',
        dest='sub_only',\
        default=False,\
        help="Download the captions/subtitle only")
    downloader.add_option(
        "-d","--directory", 
        action='store_true',
        dest='output',\
        help="Output directory where the videos will be saved, default is current directory.")
    
    
    parser.add_option_group(general)
    parser.add_option_group(downloader)

    (options, args) = parser.parse_args()

    if not options.username and not options.password:
        username = fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Username : " + fg + sb
        password = fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Password : " + fc + sb
        email    = getpass.getuser(prompt=username)
        passwd   = getpass.getpass(prompt=password)
        print ("")
        if options.org:
            if options.output and not options.sub_only:
                org         = args[0]
                try:
                    url         = args[1]
                except IndexError:
                    parser.print_usage()
                else:
                    save_to     = args[2]
                    if email and passwd:
                        lynda =  LyndaDownload(url, email, passwd, org=org)
                        lynda.InfoExtractor(outto=save_to)
                    else:
                        print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Username and password is required..")
                        exit(0)
            elif options.output and options.sub_only:
                org         = args[0]
                try:
                    url         = args[1]
                except IndexError:
                    parser.print_usage()
                else:
                    save_to     = args[2]
                    if email and passwd:
                        lynda =  LyndaDownload(url, email, passwd, org=org)
                        lynda.InfoExtractor(outto=save_to, sub_only=True)
                    else:
                        print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Username and password is required..")
                        exit(0)
                    
            elif not options.output and not options.sub_only:
                org         = args[0]
                try:
                    url         = args[1]
                except IndexError:
                    parser.print_usage()
                else:
                    if email and passwd:
                        lynda =  LyndaDownload(url, email, passwd, org=org)
                        lynda.InfoExtractor()
                    else:
                        print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Username and password is required..")
                        exit(0)
            elif not options.output and options.sub_only:
                org         = args[0]
                try:
                    url         = args[1]
                except IndexError:
                    parser.print_usage()
                else:
                    if email and passwd:
                        lynda =  LyndaDownload(url, email, passwd, org=org)
                        lynda.InfoExtractor(sub_only=True)
                    else:
                        print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Username and password is required..")
                        exit(0)
                    
        else:            
            if options.output and not options.sub_only:
                try:
                    url         = args[0]
                except IndexError:
                    parser.print_usage()
                else:
                    save_to     = args[1]
                    if email and passwd:
                        lynda       = LyndaDownload(url, email, passwd)
                        lynda.InfoExtractor(outto=save_to)
                    else:
                        print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Username and password is required..")
                        exit(0)
                        
            elif options.output and options.sub_only:
                try:
                    url         = args[0]
                except IndexError:
                    parser.print_usage()
                else:
                    save_to     = args[1]
                    if email and passwd:
                        lynda       = LyndaDownload(url, email, passwd)
                        lynda.InfoExtractor(outto=save_to, sub_only=True)
                    else:
                        print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Username and password is required..")
                        exit(0)
                    
            elif not options.output and not options.sub_only:
                try:
                    url         = args[0]
                except IndexError:
                    parser.print_usage()
                else:
                    if email and passwd:
                        lynda =  LyndaDownload(url, email, passwd)
                        lynda.InfoExtractor()
                    else:
                        print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Username and password is required..")
                        exit(0)
                        
            elif not options.output and options.sub_only:
                try:
                    url         = args[0]
                except IndexError:
                    parser.print_usage()
                else:
                    if email and passwd:
                        lynda =  LyndaDownload(url, email, passwd)
                        lynda.InfoExtractor(sub_only=True)
                    else:
                        print (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Username and password is required..")
                        exit(0)

    elif options.username and options.password:
        if options.org:
            if options.output:
                username    = args[0]
                password    = args[1]
                org         = args[2]
                try:
                    url         = args[3]
                except IndexError:
                    parser.print_usage()
                else:
                    save_to     = args[4]
                    lynda =  LyndaDownload(url, username, password, org=org)
                    lynda.InfoExtractor(outto=save_to)
            else:
                username    = args[0]
                password    = args[1]
                org         = args[2]
                try:
                    url         = args[3]
                except IndexError:
                    parser.print_usage()
                else:
                    lynda =  LyndaDownload(url, username, password, org=org)
                    lynda.InfoExtractor()
        else:            
            if options.output:
                username    = args[0]
                password    = args[1]
                try:
                    url         = args[2]
                except IndexError:
                    parser.print_usage()
                else:
                    save_to     = args[3]
                    lynda       = LyndaDownload(url, username, password)
                    lynda.InfoExtractor(outto=save_to)
            else:
                username    = args[0]
                password    = args[1]
                try:
                    url         = args[2]
                except IndexError:
                    parser.print_usage()
                else:
                    lynda =  LyndaDownload(url, username, password)
                    lynda.InfoExtractor()
    else:
        parser.print_usage()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print (fc + sd + "\n[" + fm + sb + "*" + fc + sd + "] : " + fr + sd + "User Interrupted..")
        time.sleep(0.8)
        
        
