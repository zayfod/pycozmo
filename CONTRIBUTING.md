
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
