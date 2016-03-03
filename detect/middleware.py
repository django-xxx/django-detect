# -*- coding: utf-8 -*-

import re


class ConstExtendIntField(int):
    def __new__(cls, flag, version=''):
        obj = int.__new__(cls, flag)
        obj.version = version
        return obj


class UserAgentDetectionMiddleware(object):

    def process_request(self, request):
        ua = request.META.get('HTTP_USER_AGENT', '').lower()
        # Weixin and Version
        wx = re.findall(r'micromessenger[\s/]([\d.]+)', ua)
        request.weixin = request.wechat = ConstExtendIntField(True, wx[0]) if wx else ConstExtendIntField(False, '')
        # iPhone、iPad、iPod
        request.iPhone, request.iPad, request.iPod = 'iphone' in ua, 'ipad' in ua, 'ipod' in ua
        # iOS
        request.iOS = request.iPhone or request.iPad or request.iPod
        # Android
        adr = re.findall(r'android ([\d.]+)', ua)
        request.Android = ConstExtendIntField(True, adr[0]) if adr else ConstExtendIntField('android' in ua, '')
        return None
