from datetime import datetime
import datetime
import csv
import sqlite3
from flask import Flask, request, render_template, jsonify
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
HOST = '0.0.0.0'

# Stack overflow url to all questions.
URL = 'https://stackoverflow.com/questions'


#CSV writer
csv_file = open('unanswered_list.csv', 'w')
fieldnames = ['question', 'link']
dictwriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
dictwriter.writeheader()

#sqlite connect
DATABASE_FILE = 'SOF.db'
conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
cur = conn.cursor()


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
                dictwriter.writerow({'question': question, 'link': link})
                display_dict[question] = link
        while_counter += 1
        next_link = f'?tab=newest&page={while_counter}'
        html = requests.get(URL + next_link)
        bs_page = BeautifulSoup(html.text, 'html.parser')
    return display_dict


#User frontend
@app.route('/', methods = ['GET', 'POST'])
def home():
    """
    Initial route that takes you home.
    """
    return render_template('index.html')


#User frontend
@app.route('/q-list', methods = ['GET', 'POST'])
def q_list():
    """
    Route that takes you to a result page if you search for a tag and pages on the
    home page
    """
    pages = request.form['pages']
    tag = request.form['tag']
    question_dict = find_questions(pages, tag)
    return render_template('q_list.html', question_dict = question_dict)


#User frontend with API json return
@app.get('/search')
def search_bar():
    """
    Part of the API functions that allows you to search the database
    """
    if request.args.get('search') == None:
        return render_template('search.html')
    data = cur.execute(f"SELECT QUESTION FROM python WHERE question LIKE '%{request.args.get('search')}%'").fetchall()
    return jsonify(data)

#API
@app.get("/questions/", defaults={'num': None})
@app.get("/questions/<num>")
def get_questions(num):
    """
    Part of the API functions that if just question gives you all from the
    database but if you give it a number it limits it to x number of entries
    from the DB
    """
    if num:
        cur.execute("SELECT question FROM python LIMIT %s;" % (num,))
        data = cur.fetchall()
        return jsonify(data)
    cur.execute("SELECT question FROM python;")
    data = cur.fetchall()
    return jsonify(data)


#API
@app.get('/date/<date>')
def get_questions_date(date):
    """
    Part of the API function that allows you to search DB with by date
    """
    date_object = datetime.strptime(date, '%m-%d-%Y').date()
    data = cur.execute("SELECT QUESTION FROM python WHERE date = date('%s')" % (date_object,)).fetchall()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host=HOST)
