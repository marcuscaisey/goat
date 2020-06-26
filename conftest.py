import pytest


def pytest_addoption(parser):
    parser.addoption("--functional", action="store_true", help="run functional tests")


def pytest_collection_modifyitems(config, items):
    """
    Skip over the functional tests if the --functional option is not given.
    """
    if config.getoption("--functional"):
        return

    for item in items:
        filename, *_ = item.nodeid.split("::")
        if "functional" in filename:
            print(filename)
            skip_functional = pytest.mark.skip(reason="need --functional option to run")
            item.add_marker(skip_functional)
