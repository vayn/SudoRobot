#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: agent.py
# @Date: 2011年03月30日 星期三 09时59分28秒

from urllib import quote
from simplejson import loads
from google.appengine.api import urlfetch
from google.appengine.api import memcache
from util import replace, rreplace, shortener


class Agent(object):
    error_msg = '抱歉，出现了网络故障'

    def fetch(self, message):
        """Fetch JSON feed from Feed API with urlfetch"""
        try:
            req = urlfetch.fetch(self.api)
            if req.status_code == 200:
                return req
            else:
                return False
        except:
            return False

    def get_data(self, message, key):
        """Get and add data from/to memcache"""
        data = memcache.get(key)
        if data is not None:
            message.reply(data)
        else:
            data = self.fetch(message)
            memcache.add(key, data, 600)
            message.reply(data)

class FsAgent(Agent):
    """FeedzShare Agent"""

    def __init__(self):
        self.api = 'https://ajax.googleapis.com/ajax/services/feed/load?v=1.0&q=' + \
                quote('http://www.feedzshare.com/s/n/rss') + '&num=10'
        self.response = []

    def fetch(self, message):
        """
        Parse Json feed, put all entries in a list, then join
        elements in the list into a string and return it.
        """
        req = Agent.fetch(self, message)
        if req == False:
            message.reply(self.__class__.error_msg)
        else:
            ret = loads(req.content)['responseData']['feed']['entries']
            if len(ret) == 0:
                message.reply(self.__class__.error_msg)
            else:
                for entry in ret:
                    self.response.append(
                        entry['title'] + '\n' +
                        replace(entry['contentSnippet']) + ' ' +
                        shortener(entry['link']) + '\n\n'
                    )
                msg = rreplace(''.join(self.response), '\n')
                return msg

