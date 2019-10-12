"""

PyCozmo setup script.

"""

import os
import sys
import re
import setuptools
from distutils.version import LooseVersion


def get_package_variable(key):
    fspec = os.path.join("pycozmo", "__init__.py")
    with open(fspec) as f:
        for line in f:
            m = re.match(r"(\S+)\s*=\s*[\"']?(.+?)[\"']?\s*$", line)
            if m and key == m.group(1):
                return m.group(2)
    return None


def get_readme():
    with open("README.md") as f:
        readme = f.read()
    return readme


# Check for setuptools version as long_description_content_type is not supported in older versions.
if LooseVersion(setuptools.__version__) < LooseVersion("38.6.0"):
    sys.exit("ERROR: setuptools 38.6.0 or newer required.")

setuptools.setup(
    name="pycozmo",
    packages=setuptools.find_packages(),
    version=get_package_variable("__version__"),
    license="MIT",
    description="A pure-Python Anki Cozmo communication library.",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    author="Kaloyan Tenchov",
    author_email="zayfod@gmail.com",
    url="https://github.com/zayfod/pycozmo/",
    python_requires=">=3.5.4",
    install_requires=["dpkt", "numpy", "Pillow>=6.0.0", "flatbuffers"],
    keywords=["anki", "cozmo", "robot", "robotics"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
    ],
    scripts=[
        "tools/pycozmo_dump.py",
        "tools/pycozmo_replay.py",
    ],
)
