# tinyurl
An easy function to get short URL from tinyurl.com

>>> import tinyurl
>>> 
>>> url = 'http://tw.yahoo.com'
>>> 
>>> tiny = tinyurl.TinyURL()
>>> short_url = tiny.get_tinyurl(url)
>>> print(short_url)
