#!/usr/bin/env python

# Copyright (c) 2009-2015, Mario Vilas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import with_statement

from distutils.core import setup
from os import chdir
from os.path import abspath, join, split
from warnings import catch_warnings, simplefilter

here = split(abspath(__file__))[0]
chdir(here)

with catch_warnings():
    simplefilter('ignore')
    setup(name='google',
          provides=['google'],
          requires=['beautifulsoup4'],
          packages=['google'],
          scripts=[join('scripts', 'google')],
          version="1.07",
          description="Python bindings to the Google search engine.",
          long_description=open(join(here, 'README.md'), 'rU').read(),
          author="Mario Vilas",
          author_email="mvilas@gmail.com",
          url="http://breakingcode.wordpress.com/",
          classifiers=["Development Status :: 5 - Production/Stable",
                       "Intended Audience :: Developers",
                       "License :: OSI Approved :: BSD License",
                       "Environment :: Console",
                       "Programming Language :: Python",
                       "Topic :: Software Development :: Libraries :: Python Modules",
                       ],
          )
