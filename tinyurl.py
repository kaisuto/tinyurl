#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import lxml.html
import lxml.html.html5parser
import requests

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('tiny')

# hide debug msg from requests
logging.getLogger("requests").setLevel(logging.WARNING)


class TinyURL(object):
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                   'AppleWebKit/537.36 (KHTML, like Gecko)'
                   'Chrome/66.0.3359.181 Safari/537.36')
    tinyurl_url = 'http://tinyurl.com/create.php'

    def __init__(self, user_agent=user_agent, max_retry=5, timeout=10):
        self.user_agent = user_agent
        self.max_retry = max_retry
        self.timeout = timeout

    def get_tinyurl(self, long_url):
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

        for _ in range(self.max_retry):
            try:
                with requests.get(self.tinyurl_url, params=params,
                                  headers=headers, timeout=self.timeout) as resp:
                    resp.raise_for_status()
                    html = resp.text
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
    tiny = TinyURL()
    short_url = tiny.get_tinyurl(url)
    print(short_url)
