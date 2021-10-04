import pytest
from scrapper import *

@pytest.fixture
def bs_driver():
    html = requests.get(URL)
    bs = BeautifulSoup(html.text, 'html.parser')
    return bs



