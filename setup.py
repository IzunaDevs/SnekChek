# External Libraries
from setuptools import setup, find_packages

# Snekchek
from snekchek import misc

with open("README.md") as file:
    README = file.read()

with open("requirements.txt") as file:
    REQUIREMENTS = file.readlines()

with open("LICENSE") as file:
    LICENSE = file.read()

if __name__ == '__main__':
    setup(
        name="snekchek",
        author="izunadevs",
        author_email="izunadevs@martmists.com",
        maintainer="martmists",
        maintainer_email="mail@martmists.com",
        license=LICENSE,
        zip_safe=True,
        version=misc.__version__,
        description=misc.description,
        long_description=README,
        url="https://github.com/IzunaDevs/SnekChek",
        packages=find_packages(),
        install_requires=REQUIREMENTS,
        entry_points={
            "console_scripts": ["snekchek = snekchek.__main__:main"]
        },
        keywords=[
            "lint", "python", "pylint", "flake8", "isort", "snekchek", "snekrc"
        ],
        classifiers=[
            "Development Status :: 4 - Beta", "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Topic :: Software Development :: Quality Assurance",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ],
        python_requires=">=3.6")
