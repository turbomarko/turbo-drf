#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# We use calendar versioning
version = "2024.05.21"

with open("README.md") as readme_file:
    long_description = readme_file.read()

setup(
    name="turbo-drf",
    version=version,
    description=("A Cookiecutter template for creating production-ready Django Rest Framework projects quickly."),
    long_description=long_description,
    author="Mark Hoffman",
    author_email="7urbo.marko@gmail.com",
    url="https://github.com/turbomarko/turbo-drf",
    packages=[],
    license="BSD",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Django :: 4.2",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
    ],
    keywords=(
        "cookiecutter, Python, projects, project templates, django, "
        "drf, rest, skeleton, scaffolding, project directory, setup.py"
    ),
)
