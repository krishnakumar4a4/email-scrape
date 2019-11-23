# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

from setuptools import setup

setup(
    name="scraper",
    packages=["scraper"],
    entry_scripts={
        "console_scripts": ['scraper = scraper.scrape:main']
    },
    version="1",
    description="A tool to scrape emails from gmail",
)