import pytest
import pytest_factoryboy

from .factories import ItemFactory, ListFactory, UserFactory

pytest_factoryboy.register(ListFactory)
pytest_factoryboy.register(ItemFactory)
pytest_factoryboy.register(UserFactory)


def pytest_addoption(parser):
    parser.addoption("--functional", action="store_true", help="run functional tests as well")
    parser.addoption("--functional-only", action="store_true", help="run only the functional tests")


def pytest_collection_modifyitems(config, items):
    """
    Run the functional tests with the --functional or --functional-only options.
    """
    functional = config.getoption("--functional")
    functional_only = config.getoption("--functional-only")

    skip_functional_tests = not functional and not functional_only
    skip_unit_tests = functional_only

    functional_skip_marker = pytest.mark.skip(reason="need --functional or --functional-only option to run")
    unit_skip_marker = pytest.mark.skip(reason="--functional-only option set")

    for item in items:
        filename, *_ = item.nodeid.split("::")
        if "functional" in filename and skip_functional_tests:
            item.add_marker(functional_skip_marker)
        elif "functional" not in filename and skip_unit_tests:
            item.add_marker(unit_skip_marker)
