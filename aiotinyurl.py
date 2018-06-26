#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import lxml.html
import lxml.html.html5parser
import asyncio
import aiohttp
import functools

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('aiotiny')


class AioTinyURL(object):
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                   'AppleWebKit/537.36 (KHTML, like Gecko)'
                   'Chrome/66.0.3359.181 Safari/537.36')
    tinyurl_url = 'http://tinyurl.com/create.php'

    def __init__(self, user_agent=user_agent, max_retry=5,
                 timeout=10, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self.user_agent = user_agent
        self.max_retry = max_retry
        self.timeout = timeout

    async def get_tinyurl(self, long_url):
        headers = {'Accept': 'text/html,application/xhtml+xml,'
                             'application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                   'Connection': 'keep-alive',
                   'Host': 'tinyurl.com',
                   'Referer': 'http://tinyurl.com/',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': self.user_agent}

        params = {'source': 'indexpage',
                  'url': long_url,
                  'submit': 'Make TinyURL!',
                  'alias': ''}

        async with aiohttp.ClientSession(loop=self._loop) as session:
            for _ in range(self.max_retry):
                try:
                    async with session.get(self.tinyurl_url, params=params,
                                           headers=headers, timeout=self.timeout) as resp:
                        resp.raise_for_status()
                        html = await resp.text()
                    doc = lxml.html.fromstring(html)
                    a_tag = doc.cssselect("#contentcontainer small a")
                    if not a_tag:
                        logger.debug("len 0")
                        logger.debug(doc.text_content())
                    short_url_tag = doc.cssselect("#contentcontainer small a")[0]
                    short_url = short_url_tag.attrib['href']
                    del doc
                except Exception as e:
                    logger.debug('%s, %s', type(e), str(e))
                else:
                    break
        return short_url


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    url = 'http://tw.yahoo.com'
    loop = asyncio.get_event_loop()
    tiny = AioTinyURL()
    short_url = loop.run_until_complete(tiny.get_tinyurl(url))
    loop.close()
    print(short_url)
