from setuptools import setup, find_namespace_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requirements = [
    "rich>=8.0.0",
    "numpy",
    "google",
    "bs4",
    "click",
]

setup(
    name="pyinspect",
    version="0.0.8",  # change __version__ too
    description="Find and inspect python functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require={"dev": ["coverage-badge", "click"]},
    python_requires=">=3.6,",
    packages=find_namespace_packages(),
    include_package_data=True,
    url="https://github.com/FedeClaudi/pyinspect",
    author="Federico Claudi",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "why = pyinspect.answers: cli_get_answers",
            "ask = pyinspect.answers: cli_ask",
        ]
    },
)
