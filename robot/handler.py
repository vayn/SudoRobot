#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: handler.py
# @Date: 2011年03月29日 星期二 08时05分23秒

from google.appengine.ext.webapp.xmpp_handlers import CommandHandler


__metaclass__ = type

class BaseHandler(CommandHandler):
    error_msg = 'Sudo Robot拒绝接受未授权指令'

    def handle_exception(self, exception, debug_mode):
        if self.xmpp_message:
            self.xmpp_message.reply(self.error_msg+'~')

    def unhandled_command(self, message):
        message.reply(self.error_msg)
