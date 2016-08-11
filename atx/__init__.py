#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is to make mobile test more easily
"""

from __future__ import absolute_import

import os
import sys
import signal

import pkg_resources
try:
    version = pkg_resources.get_distribution("atx").version
except pkg_resources.DistributionNotFound:
    version = 'unknown'

from atx.consts import *
from atx.errors import *
from atx.device import Pattern, Bounds


def _detect_platform(*args):
    if os.getenv('ATX_PLATFORM'):
        return os.getenv('ATX_PLATFORM')

    if len(args) == 0:
        return 'android'
    elif not isinstance(args[0], basestring):
        return 'android'
    elif args[0].startswith('http://'): # WDA use http url as connect str
        return 'ios'
    else:
        # default android
        return 'android'


def connect(*args, **kwargs):
    """Connect to a device, and return its object
    Args:
        platform: string one of <android|ios|windows>
        
    Returns:
        None

    Raises:
        SyntaxError, EnvironmentError
    """
    platform = kwargs.pop('platform', _detect_platform(*args))

    cls = None
    if platform == 'android':
        os.environ['JSONRPC_TIMEOUT'] = "60" # default is 90s which is too long.
        devcls = __import__('atx.device.android')
        cls = devcls.device.android.AndroidDevice
    elif platform == 'windows':
        devcls = __import__('atx.device.windows')
        cls = devcls.device.windows.WindowsDevice
    elif platform == 'ios':
        devcls = __import__('atx.device.ios_webdriveragent')
        cls = devcls.device.ios_webdriveragent.IOSDevice
    elif platform == 'dummy': # for py.test use
        devcls = __import__('atx.device.dummy')
        cls = devcls.device.dummy.DummyDevice
    
    if cls is None:
        raise SyntaxError('Platform: %s not exists' % platform)
    c = cls(*args, **kwargs)
    return c


# def _sig_handler(signum, frame):
#     print >>sys.stderr, 'Signal INT catched !!!'
#     sys.exit(1)
# signal.signal(signal.SIGINT, _sig_handler)
