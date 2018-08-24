# coding: utf-8

import os
import setuptools
import sys

here = os.path.abspath(os.path.dirname(__file__))

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    print("publish")
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

with open(os.path.join(here, 'README.md'), 'r') as f:
    README = f.read()

with open(os.path.join(here, 'requirements.txt'), 'r') as f:
    REQUIREMENTS = [line.strip() for line in f.readlines()]

setuptools.setup(
    name="cryptomarket",
    version="0.0.4",
    author="CryptoMarket",
    author_email="pablo@cryptomkt.com",
    description="CryptoMarket API client library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cryptomkt/cryptomkt-python",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=REQUIREMENTS,
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)    