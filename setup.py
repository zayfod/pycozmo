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
    description="A pure-Python communication library, alternative SDK, and application for the Cozmo robot.",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    author="Kaloyan Tenchov",
    author_email="zayfod@gmail.com",
    url="https://github.com/zayfod/pycozmo/",
    python_requires=">=3.6.0",
    install_requires=["dpkt", "numpy", "Pillow>=6.0.0", "flatbuffers", "opencv-python>=4.0.0"],
    keywords=["ddl", "anki", "cozmo", "robot", "robotics"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
    ],
    scripts=[
        "tools/pycozmo_dump.py",
        "tools/pycozmo_replay.py",
        "tools/pycozmo_update.py",
        "tools/pycozmo_resources.py",
        "tools/pycozmo_app.py",
    ],
)
