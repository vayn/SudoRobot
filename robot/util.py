#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: util.py
# @Date: 2011年03月29日 星期二 08时18分49秒

import re
import urllib2
import simplejson

from datetime import timedelta, tzinfo
from random import choice


__metaclass__ = type

def replace(s):
    """replace html entities"""
    dic = {
        '<b>'    : '',
        '</b>'   : '',
        '&gt;'   : '>',
        '&lt;'   : '<',
        '&amp;'  : '&',
        '&quot;' : '"',
        '&#160;' : ' ',
        '&nbsp;' : ' ',
        '\n'     : '',
    }

    for i, j in dic.iteritems():
        s = s.replace(i, j)
    s = re.sub(r'\s+', ' ', s)
    return s

def rreplace(s, old, new='', count=1):
    """replace character from last"""
    lst = s.rsplit(old, count)
    return new.join(lst)

def shortener(url):
    api = 'https://www.googleapis.com/urlshortener/v1/url'
    headers = {'Content-Type': 'application/json',}
    param = simplejson.dumps({"longUrl": url})
    req = urllib2.Request(api, param, headers)
    resp = urllib2.urlopen(req)
    ret = resp.read()
    shorter = simplejson.loads(ret)['id']
    return shorter

# Time inquiry {{{
TIME_FORMAT = '北京时间 %Y年%m月%d日 %H:%M:%S'

class CST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=8)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'China Standard Time UTC+8'
# }}}

# text_message {{{
class RandomGreeting:
    greetings = (
        "我是快乐的小机器人，咿呀咿呀哟∮",
        "最近天气变化大，请注意身体",
        "/h是帮助",
        "你好！",
        "那尼？",
        "そんなじゅもんで大丈夫か？",
        "无法自我批判与改革、无法自己思考的人、没有生存的必要。",
        "你知道吗，我是一名黑客！",
        "每个安慰你挂科算什么的人最后都默默拿了奖学金",
        "每个夸你肥嘟嘟的脸好可爱的人最后都瘦成了万人迷",
        "“I'm sorry Dave, I'm afraid I can't do that”",
        "永远不要恨你的敌人，因为这会影响你的判断力。",
    )

    @classmethod
    def greeting(cls):
        return choice(cls.greetings)
# }}}

