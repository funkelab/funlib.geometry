from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent

long_description = (this_directory / "README.md").read_text()

setup(
    name="funlib.geometry",
    version="0.2",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/funkelab/funlib.geometry",
    author="Jan Funke",
    author_email="funkej@janelia.hhmi.org",
    license="MIT",
    packages=["funlib.geometry"],
)