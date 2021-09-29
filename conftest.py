import pytest
from scrapper import *

@pytest.fixture
def selenium_driver():
    DRIVER.get(URL)
    return DRIVER



