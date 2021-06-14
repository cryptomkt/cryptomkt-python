import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as requeriments:
    REQUIREMENTS = requeriments.readlines()

setuptools.setup(
    name="cryptomarket",
    version="0.0.0",
    packages=['cryptomarket', 'cryptomarket.websockets'],
    # include_package_data=True,
    description="Cryptomarket API client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['api', 'cryptomkt', 'cryptomarket', 'bitcoin', 'client'],
    url="https://github.com/cryptomkt/cryptomkt-python",
    install_requires=REQUIREMENTS,
    author="CryptoMarket",
    
    python_requires='>=3.6',
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