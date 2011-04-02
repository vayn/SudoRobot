#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: chat.py
# @Date: 2011年03月29日 星期二 01时58分08秒

from datetime import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from robot.handler import BaseHandler
from robot.util import CST, TIME_FORMAT, RandomGreeting
from robot.agent import FsAgent


senders = {}

class XMPPHandler(BaseHandler):
    def text_message(self, message=None):
        global senders
        sender = message.sender

        if sender not in senders:
            senders[sender] = True
            message.reply('人类，我是终结者3.1415926535，输入/h开始毁灭地球')
        else:
            message.reply(RandomGreeting.greeting())

    def help_command(self, message):
        """/h [命令]：显示帮助"""
        command = message.arg
        if not command:
            message.reply('终结者3.14159256535支持以下命令：\n' +
                          '/h [命令]: 帮助\n' +
                          '/t: 查询时间\n' +
                          '/fs: FeedzShare最新条目\n'
                         )
        else:
            try:
                command_name = '%s_command' % command
                command = getattr(self, command_name, None)
                message.reply(command.__doc__)
            except:
                message.reply(self.__class__.error_msg)
    h_command = help_command

    def time_command(self, message):
        """/t：显示当前时间"""
        cst = CST()
        message.reply(datetime.now(cst).strftime(TIME_FORMAT))
    t_command = time_command

    def fs_command(self, message):
        """/fs: 显示FeedzShare上的最新条目"""
        agent = FsAgent()
        agent.get_data(message, 'fs')

application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/',
                                       XMPPHandler),])

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
