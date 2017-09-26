from flask import Flask, render_template, request
import requests
import csv
import sys
import logging
import time
from bs4 import BeautifulSoup

filename = 'stops.csv'

url_timetable = 'https://myciti.org.za/en/timetables/route-stop-timetables/'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def stops():
    options = []
    with open(filename, 'r') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile)
        try:
            for row in reader:
                options.append(row)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

    logging.debug(options)
    return render_template('index.html', options=options)


@app.route('/timetable')
def timetable():
    stop_id = request.args.get('id')
    stop_name = request.args.get('name')
    weekday = time.strftime("%A")
    params = {
        'timetable[weekday]': weekday,
        'timetable[station]': stop_id,
    }
    response = requests.get(url_timetable, params)
    html = response.content
    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', attrs={'id': 'bodytable'})
    # trs = table.find_all('tr')
    # rows = []
    # Each row is '<time>	<bus>	<direction>'
    # for row in trs:
    #     data = []
    #     for td in row.find_all('td'):
    #         data.append(td.text)
    #     rows.append(data)
    json = {
        'table': table,
        'day': weekday,
        'stop': stop_name,
    }
    return render_template('timetable.html', data=json)
