import os
from pathlib import Path
from invoke import task


@task
def get_js_libs(c):
    old_dir = os.getcwd()
    lib_path = Path(__file__).parent.joinpath("odbx/js/lib")
    os.makedirs(lib_path, exist_ok=True)
    os.chdir(lib_path)
    c.run("wget https://web.chemdoodle.com/downloads/ChemDoodleWeb-8.0.0.zip")
    c.run("unzip ChemDoodleWeb-8.0.0.zip")
    os.chdir(old_dir)
