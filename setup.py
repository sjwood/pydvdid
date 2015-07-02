"""Module contains the pydvdid package definition.
"""


from setuptools import setup


setup(
    name=b"pydvdid",
    packages=[b"pydvdid"],
    version=b"0.1",
    description=b"A pure python implementation of the Windows API IDvdInfo2::GetDiscID method.",
    url=b"https://github.com/sjwood/pydvdid",
    author=b"Steve Wood",
    author_email=b"octocat@nym.hush.com",
    license=b"Apache License 2.0"
)

