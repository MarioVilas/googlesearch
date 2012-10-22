#!/usr/bin/env python

# Python bindings to the Google search engine
# Copyright (c) 2009-2012, Mario Vilas
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

__version__ = "$Id: google.py 930 2012-02-13 21:21:25Z qvasimodo $"

__all__ = ['search']

import BeautifulSoup
import cookielib
import os
import time
import urllib
import urllib2
import urlparse

# URL templates to make Google searches.
url_home          = "http://www.google.%(tld)s/"
url_search        = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search"
url_next_page     = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d"
url_search_num    = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search"
url_next_page_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d"

# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = cookielib.LWPCookieJar(
                            os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Request the given URL and return the response page, using the cookie jar.
def get_page(url):
    """
    Request the given URL and return the response page, using the cookie jar.

    @type  url: str
    @param url: URL to retrieve.

    @rtype:  str
    @return: Web page retrieved for the given URL.

    @raise IOError: An exception is raised on error.
    @raise urllib2.URLError: An exception is raised on error.
    @raise urllib2.HTTPError: An exception is raised on error.
    """
    request = urllib2.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    cookie_jar.add_cookie_header(request)
    response = urllib2.urlopen(request)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    cookie_jar.save()
    return html

# Filter links found in the Google result pages HTML code.
# Returns None if the link doesn't yield a valid result.
def filter_result(link):
    try:

        # Valid results are absolute URLs not pointing to a Google domain
        # like images.google.com or googleusercontent.com
        o = urlparse.urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link

        # Decode hidden URLs.
        if link.startswith('/url?'):
            link = urlparse.parse_qs(o.query)['q'][0]

            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urlparse.urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link

    # Otherwise, or on error, return None.
    except Exception:
        pass
    return None

# Returns a generator that yields URLs.
def search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0):
    """
    Search the given query string using Google.

    @type  query: str
    @param query: Query string. Must NOT be url-encoded.

    @type  tld: str
    @param tld: Top level domain.

    @type  lang: str
    @param lang: Languaje.

    @type  num: int
    @param num: Number of results per page.

    @type  start: int
    @param start: First result to retrieve.

    @type  stop: int
    @param stop: Last result to retrieve.
        Use C{None} to keep searching forever.

    @type  pause: float
    @param pause: Lapse to wait between HTTP requests.
        A lapse too long will make the search slow, but a lapse too short may
        cause Google to block your IP. Your mileage may vary!

    @rtype:  generator
    @return: Generator (iterator) that yields found URLs. If the C{stop}
        parameter is C{None} the iterator will loop forever.
    """

    # Set of hashes for the results found.
    # This is used to avoid repeated results.
    hashes = set()

    # Prepare the search string.
    query = urllib.quote_plus(query)

    # Grab the cookie from the home page.
    get_page(url_home % vars())

    # Prepare the URL of the first request.
    if num == 10:
        url = url_search % vars()
    else:
        url = url_search_num % vars()

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    while not stop or start < stop:

        # Sleep between requests.
        time.sleep(pause)

        # Request the Google Search results page.
        html = get_page(url)

        # Parse the response and process every anchored URL.
        soup = BeautifulSoup.BeautifulSoup(html)
        anchors = soup.findAll('a')
        for a in anchors:

            # Get the URL from the anchor tag.
            try:
                link = a['href']
            except KeyError:
                continue

            # Filter invalid links and links pointing to Google itself.
            link = filter_result(link)
            if not link:
                continue

            # Discard repeated results.
            h = hash(link)
            if h in hashes:
                continue
            hashes.add(h)

            # Yield the result.
            yield link

        # Prepare the URL for the next request.
        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()

# When run as a script, take all arguments as a search query and run it.
if __name__ == "__main__":
    import sys
    query = ' '.join(sys.argv[1:])
    if query:
        for url in search(query, stop=20):
            print(url)
