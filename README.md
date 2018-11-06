googlesearch
============

Google search from Python.

https://breakingcode.wordpress.com/2010/06/29/google-search-python/

Usage example
-------------

    # Get the first 20 hits for: "Breaking Code" WordPress blog
    from googlesearch import search
    for url in search('"Breaking Code" WordPress blog', stop=20):
        print(url)

Installing
----------

    pip install google

Reference documentation
-----------------------

https://python-googlesearch.readthedocs.io/en/latest/
