#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time

import beanstalkc


class Worker(object):
    def __init__(self, host, port, tubes):
        self.host = host
        self.port = port
        self.tubes = tubes

    def work(self):
        while True:
            beanstalk = None
            try:
                if beanstalk:
                    beanstalk.reconnect()
                else:
                    beanstalk = \
                        beanstalkc.Connection(self.host, self.port)
                for tube in self.tubes:
                    beanstalk.watch(tube)
                for tube in beanstalk.watching():
                    if tube not in self.tubes:
                        beanstalk.ignore(tube)

                while True:
                    job = beanstalk.reserve(timeout=10)
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
                if beanstalk:
                    beanstalk.close()
                beanstalk = None
            time.sleep(2)

    def execute_job(self, job):
        pass
