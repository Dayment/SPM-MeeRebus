# selenium-testing/conftest.py

import pytest
import os

def pytest_addoption(parser):
    parser.addoption("--url", action="store", help="URL of the site to test")

@pytest.fixture
def url(request):
    return request.config.getoption("--url") or os.getenv('APP_URL')