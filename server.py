import sqlite3 as lite
from sqlalchemy import create_engine
from flask_restful import Resource, Api
from flask import Flask, request
import json
import argparse

from flask_cors import CORS, cross_origin

db_connect = create_engine('sqlite:///data.db')
app = Flask(__name__)

api = Api(app)

CORS(app, resources={r"/sentiment_range":\
                     {"origins": "http://frontend.sentiment.01dd0694.svc.dockerapp.io:5000"}})


@app.route('/sentiment/<date>')
def sentiment_for_date(date):
    conn = db_connect.connect() 
    query = conn.execute('select * from reddit_data where dt=:date', {'date': date})
    d = query.cursor.fetchall()
    if(len(d) == 0):
        return json.dumps('found nothing')
    data = {}
    data['date'] = d[0][0]
    data['sentiment'] = d[0][1]
    data['post_count'] = d[0][2]

    return json.dumps(data)

@app.route('/sentiment_range')
def sentiment_for_range():
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    if(not start_date or not end_date):
        return json.dumps('Missing dates')

    conn = db_connect.connect() 
    query = conn.execute('select * from reddit_data where dt between ? and ?',(start_date, end_date))
    d = query.cursor.fetchall()
    if(len(d) == 0):
        return json.dumps('Found nothing')
    data = {}
    for row in d:
        obj = {}
        obj['sentiment'], obj['post_count'] = row[1], row[2]
        data[row[0]] = obj
    print('found ' + str(len(d)) + ' sentiments')
    return json.dumps(data)
def __init__(self):
    print('duuude')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host', type=str,
        default='0.0.0.0',
        help='what url to run the server on, default 0.0.0.0')
    parser.add_argument(
        '--port', type=integer,
        default=3001,
        help='what port to run the server on, default 3001')

    args = parser.parse_args()
    host, port = vars(args)['host'], vars(args)['port']

    app.run(port=port, host=host)
