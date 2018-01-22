# External Libraries
from setuptools import setup, find_packages

# Snekchek
from snekchek import misc

if __name__ == '__main__':
    with open("README.md") as readme, open("requirements.txt") as requirements, \
            open("LICENSE") as license:  # pylint: disable=redefined-builtin
        setup(
            name="snekchek",
            author="izunadevs",
            author_email="izunadevs@martmists.com",
            maintainer="martmists",
            maintainer_email="mail@martmists.com",
            license=license.read(),
            zip_safe=False,
            version=misc.__version__,
            description=misc.description,
            long_description=readme.read(),
            url="https://github.com/IzunaDevs/SnekChek",
            packages=find_packages(),
            install_requires=requirements.readlines(),
            entry_points={
                "console_scripts": ["snekchek = snekchek.__main__:main"]
            },
            keywords=[
                "lint", "python", "pylint", "flake8", "isort", "snekchek",
                "snekrc"
            ],
            classifiers=[
                "Development Status :: 3 - Alpha", "Environment :: Console",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Topic :: Software Development :: Quality Assurance",
                "Topic :: Software Development :: Libraries :: Python Modules"
            ],
            python_requires=">=3.6")
