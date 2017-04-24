from setuptools import setup

with open("README.txt", "r") as txt:
    long_description = txt.read()

setup(

    name="gamelocker",
    version="0.5.2",
    author="ClarkthyLord",
    author_email="clark71@outlook.com",
    url="https://github.com/ClarkThyLord/gamelocker",
    description="A python wrapper for MadlGlory's gamelocker.",
    long_description=long_description,
    keywords="madglory python 3.5 vainglory",
    packages=["gamelocker"],
    install_requires=["requests"]

)
