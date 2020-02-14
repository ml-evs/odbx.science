from pathlib import Path
from setuptools import setup, find_packages

module_dir = Path(__file__).resolve().parent

setup(
    name="odbx",
    version="0.4.0",
    url="https://github.com/ml-evs/odbx.science",
    license="MIT",
    author="Matthew Evans",
    author_email="web@odbx.science",
    include_package_data=True,
    packages=['odbx'],
    python_requires=">=3.6",
)
