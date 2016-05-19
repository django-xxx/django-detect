=============
django-detect
=============

Installation
============

::

    pip install django-detect


Usage
=====

::

    # ####### Device、OS #######
    # Windows
    request.Windows
    # Linux
    request.Linux
    # iMac/iPhone/iPad/iPod
    request.iMac
    request.iPhone
    request.iPad
    request.iPod
    # PC
    request.PC = request.Windows or request.Linux or request.iMac
    # iOS
    request.iOS = request.iPhone or request.iPad or request.iMac or request.iPod
    # Android and Version
    request.Android
    request.Android.version

    # ####### APP #######
    # Weixin／Wechat and Version
    request.weixin
    request.weixin.version
    request.wechat
    request.wechat.version


Settings.py
===========

::

    MIDDLEWARE_CLASSES = (
        ...
        'detect.middleware.UserAgentDetectionMiddleware',
        ...
    )

