import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--test-sandbox",
        action="store_true",
        default=False,
        help="Run sandbox tests",
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--test-sandbox"):
        skipper = pytest.mark.skip(reason="Only run when --test-sandbox is given")
        for item in items:
            if "test_sandbox" in item.keywords:
                item.add_marker(skipper)
