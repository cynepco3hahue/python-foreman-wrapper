import os
from setuptools import setup


def read(fname):
    return open(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), fname,
            )
        )
    ).read()

setup(
    name="python-foreman-wrapper",
    version="0.1",
    author="Lukianov Artyom",
    author_email="artyom.lukianov@gmail.com",
    description="Foreman API wrapper",
    license="GPL2",
    keywords="foreman",
    url="https://github.com/cynepco3hahue/python-foreman-wrapper",
    platforms=["linux"],
    packages=["foreman_wrapper"],
    long_description=read("README.md"),
    install_requires=["python-foreman", "python-rrmngmnt"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License 2 (GPL2)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
    ],
)
