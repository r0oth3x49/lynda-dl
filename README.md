[![GitHub release](https://img.shields.io/badge/release-v0.2-brightgreen.svg?style=flat-square)](https://github.com/r0oth3x49/lynda-dl/releases/tag/v0.2)
[![GitHub stars](https://img.shields.io/github/stars/r0oth3x49/lynda-dl.svg?style=flat-square)](https://github.com/r0oth3x49/lynda-dl/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/r0oth3x49/lynda-dl.svg?style=flat-square)](https://github.com/r0oth3x49/lynda-dl/network)
[![GitHub issues](https://img.shields.io/github/issues/r0oth3x49/lynda-dl.svg?style=flat-square)](https://github.com/r0oth3x49/lynda-dl/issues)
[![GitHub license](https://img.shields.io/github/license/r0oth3x49/lynda-dl.svg?style=flat-square)](https://github.com/r0oth3x49/lynda-dl/blob/master/LICENSE)

# lynda-dl
**A cross-platform python based utility to download courses from lynda for personal offline use.**

[![lynda.png](https://s26.postimg.cc/bsm316qax/lynda.png)](https://postimg.cc/image/8lrjhk5ut/)

## ***Features***

- Resume capability for a course video.
- Supports organization and individual lynda users both.
- List down course contents and video resolution, suggest the best resolution (option: `--info`).
- Download/skip all available subtitles for a video (options: `--skip-sub, --skip-sub`).
- Download lecture(s) requested resolution (option: `-q / --quality`).
- Download course to user requested path (option: `-d / --directory`).

## ***Issue Reporting Guideline***

To maintain an effective bugfix workflow and make sure issues will be solved, I ask reporters to follow some simple guidelines.

Before creating an issue, please do the following:

1. **Use the GitHub issue search** &mdash; check if the issue has already been reported.
2. **Check if the issue has been fixed** &mdash; try to reproduce it using the latest `master` in the repository.
3. Make sure, that information you are about to report is related to this repository 
   and not the one available ***Python's repository***, Because this repository cannot be downloaded via pip.

A good bug report shouldn't leave others needing to chase you up for more
information. Please try to be as detailed as possible in your report. What is
your environment? What was the course url? What steps will reproduce the issue? What OS
experience the problem? All these details will help to fix any potential bugs as soon as possible.

### ***Example:***

> Short and descriptive example bug report title
>
> A summary of the issue and the OS environment in which it occurs. If
> suitable, include the steps required to reproduce the bug.
>
> 1. This is the first step
> 2. This is the second step
> 3. Further steps, etc.
>
> `<url>` - a lynda course link to reproduce the error.
>
> Any other information you want to share that is relevant to the issue being reported.

## ***Requirements***

- Python (2 or 3)
- Python `pip`
- Python module `requests`
- Python module `colorama`
- Python module `unidecode`
- Python module `six`
- Python module `requests[security]` or `pyOpenSSL`

## ***Module Installation***

	pip install -r requirements.txt
	
## ***Tested on***

- Windows 7/8/8.1/10
- Kali linux (2017.2)
- Ubuntu-LTS (64-bit) (tested with super user)
- Mac OSX 10.9.5 (tested with super user)
 
## ***Download lynda-dl***

You can download the latest version of lynda-dl by cloning the GitHub repository.

	git clone https://github.com/r0oth3x49/lynda-dl.git


## ***Usage***

***Download course using user credentials***

    python lynda-dl.py COURSE_URL
  
***OR***

    python lynda-dl.py -u user@domain.com -p p4ssw0rd COURSE_URL
  
***Download course using organization's library card***

    python lynda-dl.py -o organization COURSE_URL
  
***OR***

    python lynda-dl.py -u library_card_num -p library_card_pin -o organization COURSE_URL
  
  
***Download course to a specific location using user credentials***

    python lynda-dl.py COURSE_URL -d "/path/to/directory/"
  
***OR***

    python lynda-dl.py -u user@domain.com -p p4ssw0rd COURSE_URL -d "/path/to/directory/"

  
***Download course to a specific location using organization's library card***

    python lynda-dl.py -o organization COURSE_URL -d "/path/to/directory/"
  
***OR***

    python lynda-dl.py -u library_card_num -p library_card_pin -o organization COURSE_URL  -d "/path/to/directory/"

***list down course information***

    python lynda-dl.py COURSE_URL --info
  
***Download with specific resolution/ quality***

    python lynda-dl.py COURSE_URL -q 720

## **Advanced Usage**

<pre><code>
Author: Nasir khan (<a href="http://r0oth3x49.herokuapp.com/">r0ot h3x49</a>)

usage: lynda-dl.py [-h] [-v] [-u] [-p] [-o] [-d] [-q] [--info] [--sub-only]
                   [--skip-sub]
                   course

A cross-platform python based utility to download courses from lynda for
personal offline use.

positional arguments:
  course                Lynda course or file containing list of courses.

General:
  -h, --help            Shows the help.
  -v, --version         Shows the version.

Authentication:
  -u , --username       Username or Library Card Number.
  -p , --password       Password or Library Card Pin.
  -o , --organization   Organization, registered at Lynda.

Advance:
  -d , --directory      Download to specific directory.
  -q , --quality        Download specific video quality.

Others:
  --info                List all lectures with available resolution.
  --sub-only            Download captions/subtitle only.
  --skip-sub            Download course but skip captions/subtitle.

Example:
  python lynda-dl.py  COURSE_URL
  python lynda-dl.py -o organization COURSE_URL

</code></pre>
