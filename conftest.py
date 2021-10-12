import pytest
from scrapper import *

@pytest.fixture
def bs_driver():
    html = requests.get(URL)
    bs = BeautifulSoup(html.text, 'html.parser')
    return bs

@pytest.fixture
def sql_conn():
    DATABASE_FILE = 'SOF.db'
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    return conn


