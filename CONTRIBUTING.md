
Contributing to PyCozmo
=======================

Any contribution to PyCozmo is welcome and appreciated.


Bug Reports and Feature Requests
--------------------------------

- Bug reports and feature requests should be made using [GitHub issues](https://github.com/zayfod/pycozmo/issues).


Pull Requests
-------------

- Pull requests should be made against the [master branch](https://github.com/zayfod/pycozmo/tree/master).
- All [checks](https://github.com/zayfod/pycozmo/actions) - linters, tests, package and documentation builds -
    run automatically on pull requests and should be passing before a PR can be merged.
- To run the linters and tests locally, install the development dependencies (requires pip 25.1 or newer) and run:
    ```
    pip install -e . --group dev
    flake8
    mypy
    pytest
    ```
- Code should adhere to the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/).
- Using docstrings is encouraged.
- Adding tests is encouraged.


Releases
--------

Unreleased changes are the latest commits on the master branch. Releases are tags on the master branch and are
listed in [CHANGES.md](CHANGES.md).

To make a release:

1. Update `__version__` in `pycozmo/__init__.py` and move the "Unreleased" entries in `CHANGES.md` under a new
    version heading. Merge these changes to master through a pull request.
2. Tag the release commit on master with the version number and push the tag:
    ```
    git tag -a 0.9.0 -m "PyCozmo 0.9.0"
    git push origin 0.9.0
    ```
3. The [Release workflow](.github/workflows/release.yml) builds the package, publishes it to
    [PyPI](https://pypi.org/project/pycozmo/), and creates a GitHub release.
    [Read the Docs](https://pycozmo.readthedocs.io/) builds the documentation for the new tag.
