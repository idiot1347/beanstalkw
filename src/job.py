#!/usr/bin/python
# -*- coding: utf-8 -*-

DEFAULT_PRIORITY = 2**32
DEFAULT_TTR = 120


class Job(object):
    def __init__(
            self, func, args=None, kwargs=None, tube='default',
            priority=DEFAULT_PRIORITY, delay=0, ttr=DEFAULT_TTR):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.tube = tube
        self.priority = priority
        self.delay = delay
        self.ttr = ttr

    @property
    def body(self):
        return dict(func=self.func, args=self.args, kwargs=self.kwargs)
