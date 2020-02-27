# -*- coding: utf-8 -*-

import re

from django.conf import settings
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
        raw_ua = request.META.get('HTTP_USER_AGENT', '')
        ua = raw_ua.lower()

        request.raw_ua = raw_ua
        request.ua = ua

        # ####### Device、OS #######
        # Windows
        request.Windows = 'windows nt' in ua
        # Linux
        request.Linux = 'linux x86_64' in ua
        # macOS
        request.macOS = request.iMac = 'macintosh' in ua
        # iPhone、iPad、iPod
        request.iPhone, request.iPad, request.iPod = 'iphone' in ua, 'ipad' in ua, 'ipod' in ua
        # PC
        request.PC = request.Windows or request.Linux or request.iMac or request.macOS
        # iOS
        request.iOS = request.iPhone or request.iPad or request.iPod
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
        request.dd = request.ding = request.dingtalk = tfv(ua, pattern=r'dingtalk[\s/]([\d.]+)', s='dingtalk')

        # 腾讯 / Tencent
        # QQ
        # Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 QQ/8.2.0.617 V1_IPH_SQ_8.2.0_1_APP_A Pixel/750 Core/WKWebView Device/Apple(iPhone 6) NetType/WIFI QBWebViewType/1 WKType/1
        # Mozilla/5.0 (Linux; Android 8.0.0; MIX 2 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045008 Mobile Safari/537.36 V1_AND_SQ_8.2.0_1296_YYB_D QQ/8.2.0.4310 NetType/WIFI WebP/0.3.0 Pixel/1080 StatusBarHeight/66 SimpleUISwitch/0
        request.qq = tfv(ua, pattern=r' qq/([\d.]+)', s=' qq/')
        # 微信 / Weixin/Wechat
        request.wx = request.weixin = request.wechat = tfv(ua, pattern=r'micromessenger[\s/]([\d.]+)', s='micromessenger')
        request.pcwx = request.PCWechat = tfv(ua, pattern=r'windowswechat[\s/]([\d.]+)', s='windowswechat')
        request.macwx = request.MacWechat = tfv(ua, pattern=r'macwechat[\s/]([\d.]+)', s='macwechat')
        request.winwx = request.WindowsWechat = request.PCWechat and not request.MacWechat
        # 企业微信 / Weixin/Wechat Work
        request.wxwork = tfv(ua, pattern=r'wxwork[\s/]([\d.]+)', s='wxwork')
        # 微信小程序 / Weixin/Wechat MiniProgram
        # Refer: https://developers.weixin.qq.com/community/develop/doc/000688811bc278ab99f69ff1256000
        # Android.*MicroMessenger.*miniProgram
        # iPhone.*MicroMessenger.*
        # Refer: https://developers.weixin.qq.com/community/develop/doc/00044454a102f8ccf2d70d09b5b000
        # 微信 7.0 起小程序内嵌 web-view 的 UA 带上了 miniProgram 标识
        request.wxMiniProgram = request.wx and 'miniprogram' in ua

        # 字节跳动 / ByteDance
        # 字节跳动 IDE
        request.ttIDE = tfv(ua, pattern=r'bytedanceide[\s/]([\d.]+)', s='bytedanceide')
        # 头条 / Toutiao
        request.tt = request.toutiao = tfv(ua, pattern=r'newsarticle[\s/]([\d.]+)', s='newsarticle')
        # 头条小程序 / Toutiao MiniProgram
        request.ttMiniProgram = request.ttMicroApp = tfv(ua, pattern=r'toutiaomicroapp[\s/]([\d.]+)', s='toutiaomicroapp')

        # ####### Crawler #######
        # curl/7.50.1
        request.curl = 'curl' in ua
        # python - requests / 2.19.1
        request.requests = 'requests' in ua
        # Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)
        request.Baiduspider = 'baiduspider' in ua

        exts = {}
        if hasattr(settings, 'DJANGO_DETECT_EXT_FUNC') and hasattr(settings.DJANGO_DETECT_EXT_FUNC, '__call__'):
            exts = settings.DJANGO_DETECT_EXT_FUNC(request) or {}
        for k, v in exts.items():
            setattr(request, k, v)

        return None
