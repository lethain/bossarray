
### Overview

boss_array.py is a wrapper around the [Yahoo BOSS][yahoo_boss] search service. It caches retrieved results and reuses them as much as possible. For example, you might retrieve results ``x[0:10]``, and later retrieve ``x[5:15]``. It would reuse the previously cached results 5 through 9, and only retrieve 10 through 14. In that same vein, if you fetched ``x[10-20]``, and then tried to retieve 15, it would use a cached copy.

boss_array.py also abstracts away the 50 result per query limit. Thus you can retrieve the first two hundred results ``x[:200]`` and it is smart enough to break that into four queries and combine the results. Note, however, that it still requires four queries, so it will be slower. However, if you first retrieved ``x[0:50]`` and then ``x[0:100]``, it would use the cached copy of 0-49, and only require one http request to fetch 50-99.

[yahoo_boss]: http://developer.yahoo.com/search/boss/

### Imagined Usage

The purpose of boss_array.py is to simplify dealing with Yahoo BOSS search results. In particular it simplifies working with results by hand in the interpreter, but its simplicity and caching may be helpful in a variety of applications.

### Setup

1. [Install the Yahoo BOSS Mashup framework.][install]
2. Create a ``config.json`` file in the directory you're running Python in (as detailed in the installation instructions for the Yahoo BOSS Mashup framework).

[install]: http://developer.yahoo.com/search/boss/mashup.html

### Usage

    from boss_array import BossArray
    x = BossArray("Python") # Here "Python" is your search term.
    len(x) # to find the length
    y = x[0:10] # fetches results 0-9
    z = x[0:100] # has 0-9 cached, so fetches 10-99
    a = x[50] # has 50 cached, so returns cached copy
    for result in x[0:100]: # already has them cached, so no http request
        print result['url']
    # open a url in a browser
    import webbrowser
    webbrowser.open(x[15]['url']) 

