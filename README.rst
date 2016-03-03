===================
django-curtail-uuid
===================

Installation
============

::

    pip install django-detect


Usage
=====

::

    # Weixin／Wechat
    request.weixin
    request.weixin.version
    request.wechat
    request.wechat.version
    # iPhone/iPad/iPod
    request.iPhone
    request.iPad
    request.iPod
    # iOS
    request.iOS = request.iPhone or request.iPad or request.iPod
    # Android
    request.Android
    request.android.version


Settings.py
===========

::

    MIDDLEWARE_CLASSES = (
        ...
        'detect.middleware.UserAgentDetectionMiddleware',
        ...
    )

