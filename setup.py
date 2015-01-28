#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='beanstalkw',
    version='0.1.0',
    url='https://github.com/BeanYoung/beanstalkw',
    license='MIT',
    author='Bingyu Chen',
    author_email='chenbingyu@buding.cn',
    description='beanstalkd worker',
    packages=['beanstalkw'],
    include_package_data=False,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'beanstalkc==0.4.0',
        'PyYAML==3.11']
)
