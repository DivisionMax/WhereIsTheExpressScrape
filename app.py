from flask import Flask, render_template, request
import requests
import csv
import sys
import logging
import time
import datetime
from bs4 import BeautifulSoup

filename = 'stops.csv'

url_timetable = 'https://myciti.org.za/en/timetables/route-stop-timetables/'

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


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
    soup = BeautifulSoup(html, 'html.parser')
    # if stop does not exist, no rows in table body OR
    # if stop does not exist, <h3>Selected Stop: </h3> in timetable-info is empty
    table = soup.find('table', attrs={'id': 'bodytable'})
    trs = table.find_all('tr')
    rows = []
    # Each row is '<time>	<bus>	<direction>'
    i = 1
    for row in trs:
        print('{} {}'.format(i, row))
        data = []
        for td in row.find_all('td'):
            data.append(td.text)
        rows.append(data)
        i = i + 1
    json = {
        'rows': rows,
        'day': weekday,
        'stop': stop_name,
        'date': datetime.date.today().strftime("%d %B %Y")
    }
    return render_template('timetable.html', data=json)
