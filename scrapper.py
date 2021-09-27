import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import requests
from flask import Flask, request, render_template, redirect


app = Flask(__name__)


# Stack overflow url to all questions.
URL = 'https://stackoverflow.com/questions'
WEBDRIVER = '/Users/treyschneider/Desktop/chromedriver'
OPTIONS = Options()
OPTIONS.add_argument('--headless')
DRIVER = Chrome(WEBDRIVER, options=OPTIONS)



#CSV writer
csv_file = open('unanswered_list.csv', 'w')
fieldnames = ['question', 'link']
dictwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
dictwriter.writeheader()


#Selenium scrapper
def get_q(pages, tag):
    URL = 'https://stackoverflow.com/questions'
    display_dict = {}
    while_counter = 1
    while while_counter < int(pages):
        DRIVER.get(URL)
        questions = DRIVER.find_elements_by_class_name("question-summary")
        for question in questions:
            try:
                status = question.find_element_by_class_name("unanswered")
            except:
                status = None
            try:
                tags = question.find_element_by_link_text(f'{tag}')
            except:
                tags = None
            if status and tags:
                q_text = question.find_element_by_class_name('question-hyperlink').text
                link = question.find_element_by_class_name('question-hyperlink').get_attribute('href')
                dictwriter.writerow({'question': q_text, 'link': link})
                display_dict[q_text] = link
        while_counter += 1
        URL = DRIVER.find_element_by_link_text('Next').get_attribute('href')
    return display_dict


def find_questions(pages, tag):
    html = requests.get(URL)
    bs = BeautifulSoup(html.text, 'html.parser')
    display_dict = {}
    while_counter = 1
    while while_counter < int(pages):
        question_summary = bs.find_all('div', {'class': 'question-summary'})
        for questions in question_summary:
            status = questions.find('div', {'class': 'status unanswered'})
            tags = questions.find('a', {'class': 'post-tag'},text = tag)
            if status and tags:
                question = questions.find('a', {'class': 'question-hyperlink'}).text
                link = URL + questions.find('a', {'class': 'question-hyperlink'})['href'][10:]
                dictwriter.writerow({'question': question, 'link': link})
                display_dict[question] = link
        while_counter += 1
        next_link = f'?tab=newest&page={while_counter}'
        html = requests.get(URL + next_link)
        bs = BeautifulSoup(html.text, 'html.parser')
    return display_dict


@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/q-list', methods = ['GET', 'POST'])
def q_list():
    pages = request.form['pages']
    tag = request.form['tag']
    question_dict = get_q(pages, tag)
    return render_template('q_list.html', question_dict = question_dict)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
