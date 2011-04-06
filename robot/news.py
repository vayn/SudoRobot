#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: news.py
# @Date: 2011年04月03日 星期日 01时46分04秒

from robot.agent import FsAgent


class News(object):
    error_msg = '你请求的新闻站不存在哦~'

    def handle(self, name, *args):
        method = getattr(self, name+'_server', None)
        if callable(method):
             method(*args)
        else:
            self.unknown_server(*args)

    def unknown_server(self, message):
        message.reply(self.error_msg)

    def feedzshare_server(self, message):
        """FeedzShare最新条目"""
        agent = FsAgent('http://feeds.feedburner.com/feedzsharenewest')
        agent.get_data(message, 'fs')
    f_server = feedzshare_server

    def pinboard_server(self, message):
        """Pinboard最近热点"""
        agent = FsAgent('http://feeds.pinboard.in/rss/popular/')
        agent.get_data(message, 'pin')
    p_server = pinboard_server

    def solidot_server(self, message):
        """Solidot最新8卦"""
        agent = FsAgent('http://feeds2.feedburner.com/solidot')
        agent.get_data(message, 'solidot')
    s_server = solidot_server

