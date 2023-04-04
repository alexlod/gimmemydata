
import os
import pkg_resources
from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="gimmemydata",
    version="0.0.1",
    author="Sam Hecht",
    author_email="samjulius@gmail.com",
    url="https://github.com/samjhecht/gimmemydata",
    packages=find_packages(),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    entry_points = {
        'console_scripts': ['gimmemydata=gimmemydata.cli:main'],
    },
    description="Get personal data and manage personal data DB.",
    long_description=long_description,
)