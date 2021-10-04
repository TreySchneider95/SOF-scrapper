"""Summary
Automatic Stack overflow scrapper for automation
"""

import csv
import sqlite3
import requests
from bs4 import BeautifulSoup


#sqlite connect
conn = sqlite3.connect('SOF.db')
cur = conn.cursor()


# Stack overflow url to all questions.
URL = 'https://stackoverflow.com/questions'


#CSV writer
csv_file = open('unanswered_list.csv', 'w', encoding='UTF8')
fieldnames = ['question', 'link']
dictwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
dictwriter.writeheader()


#Variables to search
PAGES = 10
TAG = 'python'

def find_questions(pages, tag):
    """
    Function to find the question based on the tags and number of pages
    """
    html = requests.get(URL)
    bs_page = BeautifulSoup(html.text, 'html.parser')
    display_dict = {}
    while_counter = 1
    while while_counter < int(pages):
        question_summary = bs_page.find_all('div', {'class': 'question-summary'})
        for questions in question_summary:
            status = questions.find('div', {'class': 'status unanswered'})
            tags = questions.find('a', {'class': 'post-tag'},text = tag)
            if status and tags:
                question = questions.find('a', {'class': 'question-hyperlink'})
                question = question.text
                question = question.replace("'", '"')
                link = URL + questions.find('a', {'class': 'question-hyperlink'})['href'][10:]
                cur.execute("INSERT INTO python VALUES ('%s','%s')" % (question, link))
                conn.commit()
        while_counter += 1
        next_link = f'?tab=newest&page={while_counter}'
        html = requests.get(URL + next_link)
        bs_page = BeautifulSoup(html.text, 'html.parser')
    return display_dict


if __name__ == '__main__':
    find_questions(PAGES, TAG)

#close connections
conn.close()
csv_file.close()
