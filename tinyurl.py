#!/usr/bin/python2
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('tiny')

# hide debug msg from requests
logging.getLogger("requests").setLevel(logging.WARNING)


class TinyURL(object):
    _user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.6 Safari/537.36'
    _tinyurl_url = 'http://tinyurl.com/create.php'
    _max_retry = 5

    def __init__(self, user_agent=_user_agent):
        self._user_agent = user_agent

    def _retry(func):
        # MAX_RETRY = 5
        def wrap_request(self, *args, **kwargs):
            retry_count = self._max_retry
            err_msg = 'connect fail'
            while retry_count:
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    logger.debug(func.__name__)
                    logger.debug(type(e))
                    logger.debug(str(e))
                    err_msg = '[{0}][{1}]: {2}'.format(func.__name__, type(e), str(e))
                """
                except requests.exceptions.HTTPError as e:
                    print('requests.exceptions.HTTPError')
                    #continue
                except socket.timeout:
                    print('socket.timeout')
                    #continue
                except requests.exceptions.Timeout:
                    print('requests.exceptions.Timeout')
                    #continue
                """
                retry_count -= 1
            raise Exception(err_msg)
        return wrap_request

    @_retry
    def get_tinyurl(self, long_url):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, sdch',
                   'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                   'Connection': 'keep-alive',
                   'Host': 'tinyurl.com',
                   'Referer': 'http://tinyurl.com/',
                   'Upgrade-Insecure-Requests': 1,
                   'User-Agent': self._user_agent}

        params = {'source': 'indexpage',
                  'url': long_url,
                  'submit': 'Make TinyURL!',
                  'alias': ''}

        r = requests.get(self._tinyurl_url, params=params, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser", from_encoding="utf-8")
        a_tag = soup.select("#contentcontainer small a")
        if not a_tag:
            print("len 0")
            print(soup)
        short_url = soup.select("#contentcontainer small a")[0]['href']
        return short_url


if __name__ == '__main__':
    url = 'http://tw.yahoo.com'
    tiny = TinyURL()
    short_url = tiny.get_tinyurl(url)
    print(short_url)
