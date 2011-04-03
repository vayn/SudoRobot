#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: weather.py
# @Date: 2011年03月31日 星期四 20时50分55秒

import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from urllib import urlencode
from xml.dom import minidom
from google.appengine.api import urlfetch
from google.appengine.api import memcache


class Weather:
    def __init__(self, location, message=None):
        self.location = location
        self.forecast = {}
        self.base_url = 'http://www.google.com/ig/api?hl=zh-cn&'
        self.message = message

    def setBaseUrl(self, baseurl):
        """If Google remove the api, we can set a new one."""
        self.base_url = baseurl

    def parse_data(self, dom):
        root = dom.documentElement
        forecast = {}
        forecast['city'] = root.getElementsByTagName('forecast_information')[0].\
                firstChild.getAttribute('data')

        cur_cond = root.getElementsByTagName('current_conditions')[0].childNodes
        forecast['current'] = {}
        for node in cur_cond:
            if node.nodeName not in ('icon', 'temp_f'):
                if node.nodeName == 'temp_c':
                     forecast['current'].update({
                         '温度': node.getAttribute('data')+'℃',
                     })
                else:
                     forecast['current'].update({
                         node.nodeName: node.getAttribute('data'),
                     })

        days = []
        low = []
        high = []
        conditions = []

        conditions_list = root.getElementsByTagName('forecast_conditions')
        for condlist in conditions_list:
            forecast_days = condlist.getElementsByTagName('day_of_week')
            forecast_low = condlist.getElementsByTagName('low')
            forecast_high = condlist.getElementsByTagName('high')
            forecast_condition = condlist.getElementsByTagName('condition')

            for day_tmp in forecast_days:
                days.append(day_tmp.getAttribute('data'))
            for low_tmp in forecast_low:
                low.append(low_tmp.getAttribute('data'))
            for high_tmp in forecast_high:
                high.append(high_tmp.getAttribute('data'))
            for cond_tmp in forecast_condition:
                conditions.append(cond_tmp.getAttribute('data'))

        forecast['days'] = days
        forecast['low'] = low
        forecast['high'] = high
        forecast['conditions'] = conditions
        return forecast

    def get_forecast(self):
        params = {'weather': self.location}
        url = self.base_url + urlencode(params)
        headers = {'Accept-Charset': 'UTF-8'}
        resp = urlfetch.fetch(url, headers)
        if resp.status_code == 200:
            data = resp.content
            try:
                dom = minidom.parseString(data.decode('gb2312'))
                self.forecast = self.parse_data(dom)
                return self.forecast
            except UnicodeEncodeError:
                logging.error('minidom cannot parse the string cause encoding error.')
        else:
            logging.error('There was an error on urlfetch')
            if self.message is not None:
                self.message.reply('暂时无法获得该地区的天气数据')

def weather_forecast(location, message=None):
    """
    Reply to client with the forecast.
    You could reinplement it in a better way.
    """
    data = memcache.get(location)
    if data is None:
        msg = []
        weather = Weather(location, message)
        forecast = weather.get_forecast()
        msg.append(forecast['city'])

        cur = ''
        for desc, content in forecast['current'].iteritems():
            cur += "%s, " % content
        msg.append(cur[:-2])

        fore = ''
        for i, day in enumerate(forecast['days']):
            fore += "%s: " % day
            fore += "最高%s℃, " % forecast['high'][i]
            fore += "最低%s℃, " % forecast['low'][i]
            fore += "%s\n" % forecast['conditions'][i]
        msg.append(fore[:-1])
        data = '\n'.join(msg)
        memcache.add(location, data, 43200)
        message.reply(data)
    else:
        message.reply(data)

if __name__ == '__main__':
    print weather_forecast('ny')
