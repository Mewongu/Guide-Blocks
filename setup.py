from setuptools import setup, find_packages

setup(
    name="guide_blocks",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
    author="Andreas Stenberg",
    author_email="andreas@stenite.com",
    description="A library for creating guided installation and setup procedures",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mewongu/Guide-Blocks",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)