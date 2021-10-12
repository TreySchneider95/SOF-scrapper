import pytest
from pathlib import Path

import selenium
from scrapper import *
from flask_scrapper import *

PATH_TO_FILE = "unanswered_list.csv"

def test_driver_not_none(bs_driver):
    assert bs_driver != None

def test_class_status_exists(bs_driver):
    questions = bs_driver.find_all('div', {'class': 'question-summary'})
    assert len(questions)>0

def test_class_tags_exists(bs_driver):
    status = bs_driver.find_all('div', {'class': 'status unanswered'})
    assert len(status)>0

def test_class_question_exists(bs_driver):
    tags = bs_driver.find_all('a', {'class': 'post-tag'})
    assert len(tags)>0

def test_csv_file_path_exists():
    path = Path(PATH_TO_FILE)
    assert path.is_file()

def test_next_page_works(bs_driver):
    next_link = '?tab=newest&page=2'
    html = requests.get(URL + next_link)
    assert html.status_code == 200
