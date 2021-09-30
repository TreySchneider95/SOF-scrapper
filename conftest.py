import pytest
from scrapper import *

@pytest.fixture
def selenium_driver():
    s_driver = Chrome(WEBDRIVER, options=OPTIONS)
    s_driver.get(URL)
    return s_driver



