# Change Log


## 0.2 (2018-06-04)

Features:
  - Download specific quality for course videos (option: `-q / --quality`).
  - Get user input if no credentials provided using command line argument.
  - List down all available resolution for a video in a course (option: `--info`).
  - Download multiple courses by providing text file containing list of courses.

Bugfixes:
  - ZeroDivision error fixed.


## 0.1 (2017-08-29)

Features:
  - Resume capability for a course video.
  - Downloads all available subtitles if any attached with video.
  - Saves course to user provided path (directory), default is current directory (option: `-d / --directory`).
  - Skip captions/subtitle and download course only (option: `--skip-sub`).
  - Download captions/subtitle only thanks to @leo459028 (option: `--sub-only`).