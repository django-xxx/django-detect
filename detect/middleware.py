# -*- coding: utf-8 -*-

import re

from django_six import MiddlewareMixin


class ConstExtendIntField(int):
    def __new__(cls, flag, version=''):
        obj = int.__new__(cls, flag)
        obj.version = version
        return obj


def tfv(ua, pattern='', s=''):
    """ True/False and Version """
    matched = re.findall(pattern, ua)
    return ConstExtendIntField(True, matched[0]) if matched else ConstExtendIntField(s in ua, '')


class UserAgentDetectionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        ua = request.META.get('HTTP_USER_AGENT', '').lower()

        # ####### Device、OS #######
        # Windows
        request.Windows = 'windows nt' in ua
        # Linux
        request.Linux = 'linux x86_64' in ua
        # iMac、iPhone、iPad、iPod
        request.iMac, request.iPhone, request.iPad, request.iPod = 'macintosh' in ua, 'iphone' in ua, 'ipad' in ua, 'ipod' in ua
        # PC
        request.PC = request.Windows or request.Linux or request.iMac
        # iOS
        request.iOS = request.iPhone or request.iPad or request.iMac or request.iPod
        # Android
        request.Android = tfv(ua, pattern=r'android ([\d.]+)', s='android')

        # ####### APP #######
        # 百度 / Baidu
        # 百度APP / BaiduBoxApp
        request.bd = request.baidu = tfv(ua, pattern=r'baiduboxapp[\s/]([\d.]+)', s='baiduboxapp')
        # 百度智能小程序 / Swan
        request.bdMiniProgram = request.bdSmartProgram = tfv(ua, pattern=r'swan[\s/]([\d.]+)', s='swan')

        # 阿里 / Ali
        # 钉钉 / DingDing
        request.dd = request.ding = tfv(ua, pattern=r'dingtalk[\s/]([\d.]+)', s='dingtalk')

        # 腾讯 / Tencent
        # 微信 / Weixin/Wechat
        request.wx = request.weixin = request.wechat = tfv(ua, pattern=r'micromessenger[\s/]([\d.]+)', s='micromessenger')
        # 企业微信 / Weixin/Wechat Work
        request.wxwork = tfv(ua, pattern=r'wxwork[\s/]([\d.]+)', s='wxwork')
        # 微信小程序 / Weixin/Wechat MiniProgram
        # Refer: https://developers.weixin.qq.com/community/develop/doc/000688811bc278ab99f69ff1256000
        # Android.*MicroMessenger.*miniProgram
        # iPhone.*MicroMessenger.*
        # Refer: https://developers.weixin.qq.com/community/develop/doc/00044454a102f8ccf2d70d09b5b000
        # 微信 7.0 起小程序内嵌 web-view 的 UA 带上了 miniProgram 标识
        request.wxMiniProgram = request.wx and 'miniprogram' in ua

        # 头条 / Toutiao
        # 头条 IDE
        request.ttIDE = tfv(ua, pattern=r'bytedanceide[\s/]([\d.]+)', s='bytedanceide')
        # 头条小程序 / Toutiao MiniProgram
        request.ttMiniProgram = request.ttMicroApp = tfv(ua, pattern=r'toutiaomicroapp[\s/]([\d.]+)', s='toutiaomicroapp')

        # ####### Crawler #######
        # curl/7.50.1
        request.curl = 'curl' in ua
        # python - requests / 2.19.1
        request.requests = 'requests' in ua
        # Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)
        request.Baiduspider = 'baiduspider' in ua

        return None
