# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name="scraper",
    packages=["scraper"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_scripts={
        "console_scripts": ['scraper = scraper.scrape:main']
    },
    scripts=[
        "scrape-runner.py"
    ],
    version="1",
    description="A tool to scrape emails from gmail",
)