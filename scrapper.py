import csv
from bs4 import BeautifulSoup
import requests
from flask import Flask, request, render_template, redirect


app = Flask(__name__)


# Stack overflow url to all questions.
URL = 'https://stackoverflow.com/questions'



#CSV writer
csv_file = open('unanswered_list.csv', 'w')
fieldnames = ['question', 'link']
dictwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
dictwriter.writeheader()

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
    question_dict = find_questions(pages, tag)
    return render_template('q_list.html', question_dict = question_dict)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
