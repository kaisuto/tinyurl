# tinyurl
An easy function to get short URL from tinyurl.com


Synchronous Version
------------

```python
from tinyurl import TinyURL

url = 'http://tw.yahoo.com'

tiny = TinyURL()
short_url = tiny.get_tinyurl(url)
print(short_url)
```

Asynchronous Version
------------
```python
import asyncio
from aiotinyurl import AioTinyURL

url = 'http://tw.yahoo.com'

loop = asyncio.get_event_loop()
tiny = AioTinyURL()
short_url = loop.run_until_complete(tiny.get_tinyurl(url))
print(short_url)
loop.close()
```
