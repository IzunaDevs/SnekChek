from setuptools import find_packages, setup
from snekchek import misc

with open("README.md") as readme, open("requirements.txt") as requirements:
    setup(
        name="snekchek",
        author="izunadevs",
        author_email="izunadevs@martmists.com",
        maintainer="martmists",
        maintainer_email="mail@martmists.com",
        version=misc.__version__,
        description=misc.description,
        long_description=readme.read(),
        url="https://github.com/IzunaDevs/SnekChek",
        packages=find_packages(),
        install_requires=requirements.readlines(),
        entry_points={
            "console_scripts": [
                "snekchek = snekchek.__main__:main"
            ]
        }
    )
