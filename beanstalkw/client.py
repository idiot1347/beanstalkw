#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import thread
 
import beanstalkc

import job


class Client(object):
    def __init__(self, host, port):
        self.connection = beanstalkc.Connection(host, port)
        self.current_tube = 'default'
        self.write_lock = thread.allocate_lock()

    def _put(self, job):
        if self.current_tube != job.tube:
            self.connection.use(job.tube)
            self.tube = job.tube
        return self.connection.put(
            json.dumps(job.body),
            job.priority,
            job.delay,
            job.ttr)

    def put(self, job):
        with self.write_lock:
            try:
                return self._put(job)
            except beanstalkc.SocketError, e:
                self.connection.reconnect()
                self.current_tube = 'default'
                return self._put(job)

    def enqueue(self, func, args, kwargs, tube, priority, delay, ttr):
        return self.put(job.Job(func, args, kwargs, priority, delay, ttr))
