# lynda-dl
**A cross-platform python based utility to download courses from lynda.com for personal offline use.**

[![lynda-dl.png](https://s2.postimg.org/7nnfdy4l5/lynda-dl.png)](https://postimg.org/image/mwdcrpy9h/)

### Requirements

- Python (2 or 3)
- Python `pip`
- Python module `requests`
- Python module `colorama`

### Install modules

	pip install -r requirements.txt
	
### Tested on

- Windows 7/8
- Kali linux (2017.1)

	 
### Download lynda-dl

You can download the latest version of lynda-dl by cloning the GitHub repository.

	git clone https://github.com/r0oth3x49/lynda-dl.git


### Usage 

***Download course using user credentials***

	python lynda-dl.py https://www.lynda.com/COURSE_NAME/ID.html
	
***OR***

	python lynda-dl.py -u user@domain.com -p p4ssw0rd https://www.lynda.com/COURSE_NAME/ID.html
	
***Download course using organization's library card***

	python lynda-dl.py -o organization https://www.lynda.com/COURSE_NAME/ID.html
	
***OR***

	python lynda-dl.py -u library_card_num -p library_card_pin -o organization https://www.lynda.com/COURSE_NAME/ID.html
	
	
***Download course to a specific location using user credentials***

	python lynda-dl.py https://www.lynda.com/COURSE_NAME/ID.html -d "/path/to/directory/"
	
***OR***

	python lynda-dl.py -u user@domain.com -p p4ssw0rd https://www.lynda.com/COURSE_NAME/ID.html -d "/path/to/directory/"

	
***Download course to a specific location using organization's library card***

	python lynda-dl.py -o organization https://www.lynda.com/COURSE_NAME/ID.html -d "/path/to/directory/"
	
***OR***

	python lynda-dl.py -u library_card_num -p library_card_pin -o organization https://www.lynda.com/COURSE_NAME/ID.html  -d "/path/to/directory/"
	

### Advanced Usage

<pre><code>
Author: Nasir khan (<a href="http://r0oth3x49.herokuapp.com/">r0ot h3x49</a>)

Usage: lynda-dl.py [-u (USERNAME/LIBRARY CARD NUMBER)][-p (PASSWORD/LIBRARY CARD PIN)]
                   [-o ORGANIZATION] COURSE_URL [-d DIRECTORY]

Options:
  General:
    -h, --help          Shows the help for program.
    -v, --version       Shows the version of program.

  Advance:
    -u, --username      Username or Library Card Number.
    -p, --password      Password or Library Card Pin.
    -o, --organization  Organization that is registered at lynda.com.
    -d, --directory     Output directory where the videos will be saved,
                        default is current directory.
  
  Example:
	python lynda-dl.py https://www.lynda.com/course_name/id.html
</code></pre>


### Note 
<pre><code>Do not change the position of any argument as given under the Usage, this may cause an error or failur in downloading of course.</code></pre>
