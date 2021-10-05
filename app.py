import datetime
import requests
from flask import Flask, request, render_template, redirect, jsonify
import sqlite3
from datetime import date, datetime

app = Flask(__name__)

#sqlite connect
DATABASE_FILE = 'SOF.db'
conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
cur = conn.cursor()


# @app.route('/', methods = ['GET', 'POST'])
# def home():
#     return render_template('index.html')


# def _find_next_id():
#     cur.execute("SELECT question FROM python;")
#     data = cur.fetchall()
#     return max(country["id"] for country in countries) + 1


# @app.route(methods=['GET', 'POST'])
# def get_countries_multi():


@app.get("/questions/", defaults={'num': None})
@app.get("/questions/<num>")
def get_questions(num):
    if num:
        cur.execute("SELECT question FROM python LIMIT %s;" % (num,))
        data = cur.fetchall()
        return jsonify(data)
    else:
        cur.execute("SELECT question FROM python;")
        data = cur.fetchall()
    return jsonify(data)

@app.get('/date/<date>')
def get_questions_date(date):
    date_object = datetime.strptime(date, '%m-%d-%Y').date()
    print(date_object)
    data = cur.execute("SELECT QUESTION FROM python WHERE date = date('%s')" % (date_object,)).fetchall()
    return jsonify(data)

@app.get('/search')
def search_bar():
    print(request.args.get('search'))
    if request.args.get('search') == None:
        return render_template('search.html')
    data = cur.execute(f"SELECT QUESTION FROM python WHERE question LIKE '%{request.args.get('search')}%'").fetchall()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')