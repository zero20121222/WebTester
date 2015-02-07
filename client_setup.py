from setuptools import setup, find_packages

PACKAGE = ""
NAME = "testerClient"
DESCRIPTION = "WebTester client app use with chrome"
AUTHOR = "MichaelZhao"
AUTHOR_EMAIL = "michaelzhaozero@gmail.com"
URL = ""
VERSION = "1.0"

EXCLUDES_MODULE = ["app", "app.*", "test", "summary", "summary.*"]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(exclude=EXCLUDES_MODULE),
    package_data={},
    classifiers=[
        "Development Status :: terminus",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Mac OS",
        "Programming Language :: Python",
    ],
    entry_points={
        'console_scripts': [
            'testerClient = client:init_deal',
        ],
    },
    zip_safe=False,
)