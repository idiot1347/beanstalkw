#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

DEFAULT_PRIORITY = 2**32 - 1
DEFAULT_TTR = 120


class BaseJob(object):
    def __init__(
            self, body, tube='default', priority=DEFAULT_PRIORITY,
            delay=0, ttr=DEFAULT_TTR):
        self._body = body
        self.tube = tube
        self.priority = priority
        self.delay = delay
        self.ttr = ttr

    @property
    def body(self):
        return self._body


class FuncJob(BaseJob):
    def __init__(
            self, func, args=None, kwargs=None, tube='default',
            priority=DEFAULT_PRIORITY, delay=0, ttr=DEFAULT_TTR):
        super(FuncJob, self).__init__('', tube, priority, delay, ttr)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    @property
    def body(self):
        return json.dumps(
            dict(func=self.func, args=self.args, kwargs=self.kwargs))
