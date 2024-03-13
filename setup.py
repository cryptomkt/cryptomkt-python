import os
import setuptools
import sys

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    print("publish")
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as requeriments:
    REQUIREMENTS = requeriments.readlines()

setuptools.setup(
    name="cryptomarket",
    version="3.1.0",
    packages=['cryptomarket', 'cryptomarket.websockets'],
    include_package_data=True,
    description="Cryptomarket API client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['api', 'cryptomkt', 'cryptomarket', 'bitcoin', 'client'],
    url="https://github.com/cryptomkt/cryptomkt-python",
    install_requires=REQUIREMENTS,
    author="CryptoMarket",
    python_requires='>=3.8',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)