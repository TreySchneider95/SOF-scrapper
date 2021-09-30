import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import requests
import sqlite3

#sqlite connect
conn = sqlite3.connect('SOF.db')
cur = conn.cursor()


# Stack overflow url to all questions.
URL = 'https://stackoverflow.com/questions'
WEBDRIVER = 'driver/chromedriver'
OPTIONS = Options()
OPTIONS.add_argument('--headless')
DRIVER = Chrome(WEBDRIVER, options=OPTIONS)



#CSV writer
csv_file = open('unanswered_list.csv', 'w')
fieldnames = ['question', 'link']
dictwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
dictwriter.writeheader()


#Variables to search
PAGES = 10
TAG = 'python'

#Selenium scrapper
def get_q(pages, tag):
    URL = 'https://stackoverflow.com/questions'
    display_dict = {}
    while_counter = 1
    while while_counter < int(pages):
        DRIVER.get(URL)
        questions = DRIVER.find_elements_by_class_name("question-summary")
        for question in questions:
            status = question.find_elements_by_class_name("unanswered")
            tags = question.find_element_by_link_text(f'{tag}')
            if len(status) > 0 and len(tags) > 0:
                q_text = question.find_element_by_class_name('question-hyperlink').text
                link = question.find_element_by_class_name('question-hyperlink').get_attribute('href')
                cur.execute("INSERT INTO python VALUES ('%s','%s')" % (q_text, link))
                conn.commit()
        while_counter += 1
        URL = DRIVER.find_element_by_link_text('Next').get_attribute('href')
    return display_dict
if __name__ == '__main__':
    get_q(PAGES, TAG)
#close connections
DRIVER.close()
conn.close()
