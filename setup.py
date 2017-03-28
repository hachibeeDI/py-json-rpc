#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

install_requires = open('requirements.txt').read().split('\n')
readme_content = open('README.md').read()


setup(
    name='py-json-rpc',
    version='0.0.3',
    description='Decorator based toolkit to use JSONRPC easy like Flask',
    long_description=readme_content,
    author='OGURA_Daiki',
    author_email='',
    license='MIT',
    keywords=['json rpc', 'smart home'],
    url='https://github.com/hachibeeDI/py-json-rpc',
    packages=find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
