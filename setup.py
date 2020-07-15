# coding: utf-8

import os
import setuptools
import sys

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    print("publish")
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
REQUIREMENTS = [
    line.strip() for line in open(os.path.join(os.path.dirname(__file__),
                                               'requirements.txt')).readlines()]

setuptools.setup(
    name="cryptomarket",
    version="1.0.4",
    packages=setuptools.find_packages(),
    include_package_data=True,
    description="CryptoMarket API client library",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=['api', 'cryptomkt', 'cryptomarket', 'bitcoin', 'client'],
    url="https://github.com/cryptomkt/cryptomkt-python",
    install_requires=REQUIREMENTS,
    author="CryptoMarket",
    author_email="pablo@cryptomkt.com",
    classifiers=(
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
