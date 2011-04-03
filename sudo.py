#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: sudo.py
# @Date: 2011年03月29日 星期二 01时58分08秒

from datetime import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from robot.handler import BaseHandler
from robot.util import CST, TIME_FORMAT, RandomGreeting
from robot.agent import VxAgent
from robot.news import News
from robot.weather import weather_forecast


senders = {}

class XMPPHandler(BaseHandler):
    def text_message(self, message=None):
        global senders
        sender = message.sender

        if sender not in senders:
            senders[sender] = True
            message.reply('我是SR家族最新成员SRII，输入/h看看我能做什么')
        else:
            message.reply(RandomGreeting.greeting())

    def help_command(self, message):
        """/h [命令]：显示帮助"""
        command = message.arg
        if not command:
            message.reply('SRII 支持以下命令:\n' +
                          '/h [命令]: 帮助\n' +
                          '/t: 查询时间\n' +
                          '/w [城市]: 天气预报, 如: /w NY\n' +
                          '/vx: V2EX最新贴子\n' +
                          '/news [站名]: 猎取最新消息, 如 /news f.可猎取目标:\n' +
                          '  FeedzShare: F\n' +
                          '  Pinboard: P\n' +
                          '  Solidot: S'
                         )
        else:
            try:
                command_name = '%s_command' % command
                command = getattr(self, command_name, None)
                message.reply(command.__doc__)
            except:
                message.reply(self.__class__.error_msg)
    h_command = help_command

    def r_command(self, message):
        """Code R"""
        msg = 'Sudo Robot系列是电子节点的实验产品，内部代号R'
        message.reply(msg)

    def vx_command(self, message):
        """/vx: V2EX最新贴子"""
        agent = VxAgent()
        agent.get_data(message, 'vx')

    def news_command(self, message):
        """/news [站点]: 获取最新消息"""
        agent = News()
        server = message.arg.strip().lower()
        if len(server) == 0:
            message.reply(self.__class__.error_msg)
        else:
            agent.handle(server, message)

    def time_command(self, message):
        """/t：显示当前时间"""
        cst = CST()
        message.reply(datetime.now(cst).strftime(TIME_FORMAT))
    t_command = time_command

    def weather_command(self, message):
        """/w: 天气预报"""
        location = message.arg
        if len(location) == 0:
            message.reply(self.__class__.error_msg)
        else:
            weather_forecast(location, message)
    w_command = weather_command


application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/',
                                       XMPPHandler),])

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
