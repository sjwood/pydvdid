"""Module contains the pydvdid package definition.
"""


from setuptools import setup


setup(
    name="pydvdid",
    version="1.0",
    description="A pure Python implementation of the Windows API IDvdInfo2::GetDiscID method, as used by Windows Media Center to compute a 'practically unique' 64-bit CRC for metadata retrieval.", # pylint: disable=locally-disabled, line-too-long
    author="Steve Wood",
    author_email="octocat@nym.hush.com",
    url="https://github.com/sjwood/pydvdid",
    packages=[
        "pydvdid"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Home Automation",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    license="Apache License 2.0",
)
