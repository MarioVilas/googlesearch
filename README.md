Google Search
============

Google search from Python.

https://python-googlesearch.readthedocs.io/en/latest/

**Note**: this project is not affiliated with Google in any way.

Usage example
-------------

    # Get the first 20 hits for: "Breaking Code" WordPress blog
    from googlesearch import search
    for url in search('"Breaking Code" WordPress blog', stop=20):
        print(url)

Installing
----------

    pip install google
