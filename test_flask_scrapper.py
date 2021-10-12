import pytest
from pathlib import Path
from flask_scrapper import *


def test_conn_to_db(sql_conn):
    assert sql_conn != None

def test_scrapper_func(bs_driver):
    assert bs_driver != None