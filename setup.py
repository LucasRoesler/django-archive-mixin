#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

description = """
Archive/soft delete Django models.
"""

setup(
    name="django-archive-mixin",
    version="0.1.0",
    url="https://github.com/LucasRoesler/django-archive-mixin",
    license="MIT",
    platforms=["OS Independent"],
    description=description.strip(),
    author="Lucas Roesler",
    author_email="roesler.lucas@gmail.com",
    keywords="django, model, mixin, soft delete, delete",
    maintainer="Lucas Roesler",
    maintainer_email="roesler.lucas@gmail.com",
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP",
    ]
)
