import pytest
from pathlib import Path

import selenium
from scrapper import *

def test_driver_not_none(selenium_driver):
    assert selenium_driver != None

def test_class_status_exists(selenium_driver):
    questions = selenium_driver.find_elements_by_class_name("question-summary")
    assert len(questions)>0

def test_class_tags_exists(selenium_driver):
    status = selenium_driver.find_elements_by_class_name("unanswered")
    assert len(status)>0

def test_class_question_exists(selenium_driver):
    tags = selenium_driver.find_elements_by_class_name('post-tag')
    assert len(tags)>0

def test_csv_file_path_exists():
    path_to_file = "unanswered_list.csv"
    path = Path(path_to_file)
    assert path.is_file()

def test_next_page_works(selenium_driver):
    next = selenium_driver.find_elements_by_link_text('Next')
    assert len(next)>0
