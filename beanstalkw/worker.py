#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time

import beanstalkc


class BaseWorker(object):
    def __init__(self, host, port, tubes):
        self.host = host
        self.port = port
        self.tubes = tubes
        self.beanstalk = None

    def work(self):
        while True:
            try:
                if self.beanstalk:
                    self.beanstalk.reconnect()
                else:
                    self.beanstalk = \
                        beanstalkc.Connection(self.host, self.port)
                for tube in self.tubes:
                    self.beanstalk.watch(tube)
                for tube in self.beanstalk.watching():
                    if tube not in self.tubes:
                        self.beanstalk.ignore(tube)

                while True:
                    job = self.reserve(timeout=10)
                    if not job:
                        time.sleep(2)
                        continue
                    try:
                        self.execute_job(job)
                        job.delete()
                    except Exception, e:
                        job.bury()
            except beanstalkc.SocketError, e:
                time.sleep(2)
                if self.beanstalk:
                    self.beanstalk.close()
                self.beanstalk = None
            time.sleep(2)

    def reserve(self, timeout):
        pass

    def execute_job(self, job):
        pass


class Worker(BaseWorker):
    def reserve(self, timeout):
        return self.beanstalk.reserve(timeout)


class FailedWorker(BaseWorker):
    def reserve(self, timeout):
        for i in range(timeout):
            job = self.beanstalk.peek_buried()
            if job:
                return job
            time.sleep(1)
