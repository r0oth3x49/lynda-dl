#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import lynda
import argparse

from pprint import pprint
from lynda import __version__
from lynda._colorized import *
from lynda._compat import pyver
from lynda._getpass import GetPass
from lynda._progress import ProgressBar
from lynda._colorized.banner import banner
getpass = GetPass()

class Lynda(ProgressBar):

	def __init__(self, url, username='', password='', organization=''):
		self.url = url
		self.username = username
		self.password = password
		self.organization = organization
		super(Lynda, self).__init__()

	def course_list_down(self):
		if not self.organization:
			sys.stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Trying to login as " + fm + sb +"(%s)" % (self.username) +  fg + sb +"...\n")
		if self.organization:
			sys.stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Trying to login as organization " + fm + sb +"(%s)" % (self.organization) +  fg + sb +"...\n")
		course = lynda.course(url=self.url, username=self.username, password=self.password, organization=self.organization)
		course_id = course.id
		course_name = course.title
		chapters = course.get_chapters()
		total_lectures = course.lectures
		total_chapters = course.chapters
		assets = course.assets
		sys.stdout.write (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Course " + fb + sb + "'%s'.\n" % (course_name))
		sys.stdout.write (fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "Chapter(s) (%s).\n" % (total_chapters))
		sys.stdout.write (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture(s) (%s).\n" % (total_lectures))
		for chapter in chapters:
			chapter_id = chapter.id
			chapter_index = chapter.index
			chapter_title = chapter.title
			lectures = chapter.get_lectures()
			lectures_count = chapter.lectures
			sys.stdout.write ('\n' + fc + sd + "[" + fw + sb + "+" + fc + sd + "] : " + fw + sd + "Chapter (%s-%s)\n" % (chapter_title, chapter_id))
			sys.stdout.write (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture(s) (%s).\n" % (lectures_count))
			for lecture in lectures:
				lecture_id = lecture.id
				lecture_index = lecture.index
				lecture_title = lecture.title
				lecture_subtitles = lecture.subtitles
				lecture_best = lecture.getbest()
				lecture_streams = lecture.streams
				if lecture_streams:
					sys.stdout.write(fc + sd + "     - " + fy + sb + "duration   : " + fm + sb + str(lecture.duration)+ fy + sb + ".\n")
					sys.stdout.write(fc + sd + "     - " + fy + sb + "Lecture id : " + fm + sb + str(lecture_id)+ fy + sb + ".\n")
					for stream in lecture_streams:
						content_length = stream.get_filesize()
						if content_length != 0:
							if content_length <= 1048576.00:
								size = round(float(content_length) / 1024.00, 2)
								sz = format(size if size < 1024.00 else size/1024.00, '.2f')
								in_MB = 'KB' if size < 1024.00 else 'MB'
							else:
								size = round(float(content_length) / 1048576, 2)
								sz = format(size if size < 1024.00 else size/1024.00, '.2f')
								in_MB = "MB " if size < 1024.00 else 'GB '
							if lecture_best.dimention[1] == stream.dimention[1]:
								in_MB = in_MB + fc + sb + "(Best)" + fg + sd
							sys.stdout.write('\t- ' + fg + sd + "{:<23} {:<8}{}{}{}{}\n".format(str(stream), str(stream.dimention[1]) + 'p', sz, in_MB, fy, sb))
		if assets and len(assets) > 0:
			for asset in assets:
				content_length = asset.get_filesize()
				if content_length != 0:
					if content_length <= 1048576.00:
						size = round(float(content_length) / 1024.00, 2)
						sz = format(size if size < 1024.00 else size/1024.00, '.2f')
						in_MB = 'KB' if size < 1024.00 else 'MB'
					else:
						size = round(float(content_length) / 1048576, 2)
						sz = format(size if size < 1024.00 else size/1024.00, '.2f')
						in_MB = "MB " if size < 1024.00 else 'GB '
					sys.stdout.write('\t- ' + fg + sd + "{:<23} {:<8}{}{}{}{}\n".format(str(asset), asset.extension, sz, in_MB, fy, sb))

	def download_assets(self, assets='', filepath=''):
		if assets:
			title = assets.filename
			sys.stdout.write(fc + sd + "\n[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading asset(s)\n")
			sys.stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading (%s)\n" % (title))
			try:
				retval = assets.download(filepath=filepath, quiet=True, callback=self.show_progress)
			except KeyboardInterrupt:
				sys.stdout.write (fc + sd + "\n[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "User Interrupted..\n")
				sys.exit(0)
			msg = retval.get('msg')
			if msg == 'already downloaded':
				sys.stdout.write (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Asset : '%s' " % (title) + fy + sb + "(already downloaded).\n")
			elif msg == 'download':
				sys.stdout.write (fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "Downloaded  (%s)\n" % (title))
			else:
				sys.stdout.write (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Asset : '%s' " % (title) + fc + sb + "(download skipped).\n")
				sys.stdout.write (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "{}\n".format(msg))

	def download_subtitles(self, subtitle='', filepath=''):
		if subtitle:
			title = subtitle.title + '-' + subtitle.language
			filename = "%s\\%s" % (filepath, subtitle.filename) if os.name == 'nt' else "%s/%s" % (filepath, subtitle.filename)
			try:
				retval = subtitle.download(filepath=filepath)
			except KeyboardInterrupt:
				sys.stdout.write (fc + sd + "\n[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "User Interrupted..\n")
				sys.exit(0)

	def download_lectures(self, lecture_best='', lecture_title='', inner_index='', lectures_count='', filepath=''):
		if lecture_best:
			sys.stdout.write(fc + sd + "\n[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture(s) : ({index} of {total})\n".format(index=inner_index, total=lectures_count))
			sys.stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Downloading (%s)\n" % (lecture_title))
			try:
				retval = lecture_best.download(filepath=filepath, quiet=True, callback=self.show_progress)
			except KeyboardInterrupt:
				sys.stdout.write (fc + sd + "\n[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "User Interrupted..\n")
				sys.exit(0)
			msg = retval.get('msg')
			if msg == 'already downloaded':
				sys.stdout.write (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture : '%s' " % (lecture_title) + fy + sb + "(already downloaded).\n")
			elif msg == 'download':
				sys.stdout.write (fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "Downloaded  (%s)\n" % (lecture_title))
			else:
				sys.stdout.write (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture : '%s' " % (lecture_title) + fc + sb + "(download skipped).\n")
				sys.stdout.write (fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "{}\n".format(msg))

	def download_captions_only(self, subtitle='', filepath=''):
		if subtitle:
			self.download_subtitles(subtitle=subtitle, filepath=filepath)

	def download_lectures_only(self, lecture_best='', lecture_title='', inner_index='', lectures_count='', filepath=''):
		if lecture_best:
			self.download_lectures(lecture_best=lecture_best, lecture_title=lecture_title, inner_index=inner_index, lectures_count=lectures_count, filepath=filepath)

	def download_lectures_and_captions(self, lecture_best='', lecture_title='', inner_index='', lectures_count='', subtitle='', filepath=''):
		if lecture_best:
			self.download_lectures(lecture_best=lecture_best, lecture_title=lecture_title, inner_index=inner_index, lectures_count=lectures_count, filepath=filepath)
		if subtitle:
			self.download_subtitles(subtitle=subtitle, filepath=filepath)

	def course_download(self, path='', quality='', caption_only=False, skip_captions=False):
		if not self.organization:
			sys.stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Trying to login as " + fm + sb +"(%s)" % (self.username) +  fg + sb +"...\n")
		if self.organization:
			sys.stdout.write(fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Trying to login as organization " + fm + sb +"(%s)" % (self.organization) +  fg + sb +"...\n")
		course = lynda.course(url=self.url, username=self.username, password=self.password, organization=self.organization)
		course_id = course.id
		course_name = course.title
		chapters = course.get_chapters()
		total_lectures = course.lectures
		total_chapters = course.chapters
		assets = course.assets
		sys.stdout.write (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sb + "Course " + fb + sb + "'%s'.\n" % (course_name))
		sys.stdout.write (fc + sd + "[" + fm + sb + "+" + fc + sd + "] : " + fg + sd + "Chapter(s) (%s).\n" % (total_chapters))
		sys.stdout.write (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Lecture(s) (%s).\n" % (total_lectures))
		if path:
			if '~' in path:
				path = os.path.expanduser(path)
			course_path = "%s\\%s" % (path, course_name) if os.name == 'nt' else "%s/%s" % (path, course_name)
		else:
			path = os.getcwd()
			course_path = "%s\\%s" % (path, course_name) if os.name == 'nt' else "%s/%s" % (path, course_name)
		course.course_description(filepath=course_path)
		for chapter in chapters:
			chapter_id = chapter.id
			chapter_index = chapter.index
			chapter_title = chapter.title
			lectures = chapter.get_lectures()
			lectures_count = chapter.lectures
			filepath = "%s\\%s" % (course_path, chapter_title) if os.name == 'nt' else "%s/%s" % (course_path, chapter_title)
			status = course.create_chapter(filepath=filepath)
			sys.stdout.write (fc + sd + "\n[" + fm + sb + "*" + fc + sd + "] : " + fm + sb + "Downloading chapter : ({index} of {total})\n".format(index=chapter_index, total=total_chapters))
			sys.stdout.write (fc + sd + "[" + fw + sb + "+" + fc + sd + "] : " + fw + sd + "Chapter (%s)\n" % (chapter_title))
			sys.stdout.write (fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Found (%s) lectures ...\n" % (lectures_count))
			for lecture in lectures:
				lecture_id = lecture.id
				lecture_index = lecture.index
				lecture_title = lecture.title
				lecture_subtitles = lecture.subtitles
				lecture_best = lecture.getbest()
				lecture_streams = lecture.streams
				if caption_only and not skip_captions:
					self.download_captions_only(subtitle=lecture_subtitles, filepath=filepath)
				elif skip_captions and not caption_only:
					lecture_best = lecture.get_quality(best_quality=lecture_best, streams=lecture_streams, requested=quality)
					self.download_lectures_only(lecture_best=lecture_best, lecture_title=lecture_title, inner_index=lecture_index, lectures_count=lectures_count, filepath=filepath)
				else:
					lecture_best = lecture.get_quality(best_quality=lecture_best, streams=lecture_streams, requested=quality)
					self.download_lectures_and_captions(lecture_best=lecture_best, lecture_title=lecture_title, inner_index=lecture_index, lectures_count=lectures_count, subtitle=lecture_subtitles, filepath=filepath)
		if assets and len(assets) > 0:
			for asset in assets:
				self.download_assets(assets=asset, filepath=course_path)

def main():
	sys.stdout.write(banner())
	version     = "%(prog)s {version}".format(version=__version__)
	description = 'A cross-platform python based utility to download courses from lynda for personal offline use.'
	parser = argparse.ArgumentParser(description=description, conflict_handler="resolve")
	parser.add_argument('course', help="Lynda course or file containing list of courses.", type=str)
	general = parser.add_argument_group("General")
	general.add_argument(
		'-h', '--help',\
		action='help',\
		help="Shows the help.")
	general.add_argument(
		'-v', '--version',\
		action='version',\
		version=version,\
		help="Shows the version.")

	authentication = parser.add_argument_group("Authentication")
	authentication.add_argument(
		'-u', '--username',\
		dest='username',\
		type=str,\
		help="Username or Library Card Number.",metavar='')
	authentication.add_argument(
		'-p', '--password',\
		dest='password',\
		type=str,\
		help="Password or Library Card Pin.",metavar='')
	authentication.add_argument(
		'-o', '--organization',\
		dest='org',\
		type=str,\
		help="Organization, registered at Lynda.",metavar='')

	advance = parser.add_argument_group("Advance")
	advance.add_argument(
		'-d', '--directory',\
		dest='output',\
		type=str,\
		help="Download to specific directory.",metavar='')
	advance.add_argument(
		'-q', '--quality',\
		dest='quality',\
		type=int,\
		help="Download specific video quality.",metavar='')

	other = parser.add_argument_group("Others")
	other.add_argument(
		'--info',\
		dest='info',\
		action='store_true',\
		help="List all lectures with available resolution.")
	other.add_argument(
		'--sub-only',\
		dest='caption_only',\
		action='store_true',\
		help="Download captions/subtitle only.")
	other.add_argument(
		'--skip-sub',\
		dest='skip_captions',\
		action='store_true',\
		help="Download course but skip captions/subtitle.")

	options = parser.parse_args()

	if os.path.isfile(options.course):
		f_in = open(options.course)
		courses = [line for line in (l.strip() for l in f_in) if line]
		f_in.close()
		sys.stdout.write (fc + sd + "[" + fw + sb + "+" + fc + sd + "] : " + fw + sd + "Found (%s) courses ..\n" % (len(courses)))
		for course in courses:

			if not options.username and not options.password:
				username = fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Username : " + fg + sb
				password = fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Password : " + fc + sb
				email = getpass.getuser(prompt=username)
				passwd = getpass.getpass(prompt=password)
				if email and passwd:
					lynda = Lynda(url=course, username=email, password=passwd, organization=options.org)
				else:
					sys.stdout.write('\n' + fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Username and password is required.\n")
					sys.exit(0)

				if options.info:
					lynda.course_list_down()

				if not options.info:
					if options.caption_only and not options.skip_captions:
						lynda.course_download(caption_only=options.caption_only, path=options.output)
					elif not options.caption_only and options.skip_captions:
						lynda.course_download(skip_captions=options.skip_captions, path=options.output, quality=options.quality)
					else:
						lynda.course_download(path=options.output, quality=options.quality)

			elif options.username and options.password:
				lynda = Lynda(url=course, username=options.username, password=options.password, organization=options.org)
				if options.info:
					lynda.course_list_down()

				if not options.info:
					if options.caption_only and not options.skip_captions:
						lynda.course_download(caption_only=options.caption_only, path=options.output)
					elif not options.caption_only and options.skip_captions:
						lynda.course_download(skip_captions=options.skip_captions, path=options.output, quality=options.quality)
					else:
						lynda.course_download(path=options.output, quality=options.quality)

	if not os.path.isfile(options.course):

		if not options.username and not options.password:
			username = fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Username : " + fg + sb
			password = fc + sd + "[" + fm + sb + "*" + fc + sd + "] : " + fg + sd + "Password : " + fc + sb
			email = getpass.getuser(prompt=username)
			passwd = getpass.getpass(prompt=password)
			if email and passwd:
				lynda = Lynda(url=options.course, username=email, password=passwd, organization=options.org)
			else:
				sys.stdout.write('\n' + fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sb + "Username and password is required.\n")
				sys.exit(0)

			if options.info:
				lynda.course_list_down()

			if not options.info:
				if options.caption_only and not options.skip_captions:
					lynda.course_download(caption_only=options.caption_only, path=options.output)
				elif not options.caption_only and options.skip_captions:
					lynda.course_download(skip_captions=options.skip_captions, path=options.output, quality=options.quality)
				else:
					lynda.course_download(path=options.output, quality=options.quality)

		elif options.username and options.password:
			lynda = Lynda(url=options.course, username=options.username, password=options.password, organization=options.org)
			if options.info:
				lynda.course_list_down()

			if not options.info:
				if options.caption_only and not options.skip_captions:
					lynda.course_download(caption_only=options.caption_only, path=options.output)
				elif not options.caption_only and options.skip_captions:
					lynda.course_download(skip_captions=options.skip_captions, path=options.output, quality=options.quality)
				else:
					lynda.course_download(path=options.output, quality=options.quality)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.stdout.write ('\n' + fc + sd + "[" + fr + sb + "-" + fc + sd + "] : " + fr + sd + "User Interrupted..\n")
		sys.exit(0)