from importlib.machinery import SourceFileLoader
from setuptools import setup, find_packages

version_module = SourceFileLoader("version", "pydis/version.py").load_module(
    "version"
)

__version__ = version_module.__version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pydictdis",
    version=__version__,
    author="chalice",
    author_email="lichangyin888@gmail.com",
    description="Management similar to redis interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zombie123456/pydis",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    python_requires=">=3.6",
)
