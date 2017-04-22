from setuptools import setup

with open("README.txt", "r") as txt:
    long_description = txt.read()

setup(

    name="madglory-ezl",
    version="0.5.1",
    author="ClarkthyLord",
    author_email="clark71@outlook.com",
    url="https://github.com/ClarkThyLord/madglory-ezl",
    keywords="madglory python 3.5 vainglory",
    description="A python wrapper for MadlGlory's gamelocker.",
    long_description=long_description,
    package=["madglory-ezl"],
    install_requires=[

        "requests"

    ]

)
