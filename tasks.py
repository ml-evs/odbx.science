import os
from invoke import task


@task
def get_js_libs(c):
    old_dir = os.getcwd()
    os.makedirs("odbx/js/lib", exist_ok=True)
    os.chdir("odbx/js/lib")
    c.run("wget https://web.chemdoodle.com/downloads/ChemDoodleWeb-8.0.0.zip")
    c.run("unzip ChemDoodleWeb-8.0.0.zip")
    os.chdir(old_dir)
