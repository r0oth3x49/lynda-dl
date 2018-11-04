#!/usr/bin/python

'''

Author 	: Nasir Khan (r0ot h3x49)
Github 	: https://github.com/r0oth3x49
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

from .colors import *
from .. import __version__

def banner():
    banner = """%s%s

 oooo                                .o8                      .o8  oooo    
 `888                               "888                     "888  `888    
  888  oooo    ooo ooo. .oo.    .oooo888   .oooo.        .oooo888   888    
%s%s  888   `88.  .8'  `888P"Y88b  d88' `888  `P  )88b      d88' `888   888%s%s    
%s%s  888    `88..8'    888   888  888   888   .oP"888 8888 888   888   888%s%s    
  888     `888'     888   888  888   888  d8(  888      888   888   888    
 o888o     .8'     o888o o888o `Y8bod88P" `Y888""8o     `Y8bod88P" o888o   
       .o..P'                                                                  
       `Y8P'\t\t\t\t%s%sVersion : %s%s%s\n\t\t\t\t\t%s%sAuthor  : %s%sNasir Khan (r0ot h3x49)\n\t\t\t\t\t%s%sGithub  : %s%shttps://github.com/r0oth3x49


""" % (fc, sb, fm, sb, fc, sb, fm, sb, fc, sb, fy,sb, fg, sd, __version__, fy,sb, fg, sd, fy,sb, fg, sd)
    return banner
