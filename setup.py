from pathlib import Path
from setuptools import setup
from odbx import __version__

module_dir = Path(__file__).resolve().parent

with open("requirements.txt", "r") as f:
    reqs = f.readlines()

dependency_links = [req for req in reqs if req.startswith("-e git://")]
for ind, req in enumerate(reqs):
    if req in dependency_links:
        reqs[ind] = req.split("#egg=")[-1]

setup(
    name="odbx",
    version=__version__,
    url="https://github.com/ml-evs/odbx.science",
    license="MIT",
    author="Matthew Evans",
    author_email="web@odbx.science",
    include_package_data=True,
    install_requires=reqs,
    dependency_links=dependency_links,
    packages=["odbx"],
    python_requires=">=3.6",
)
