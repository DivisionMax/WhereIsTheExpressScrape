from flask import Flask, render_template
import csv
import sys
import logging

filename = 'stops.csv'


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/stops', methods=['GET'])
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
    return render_template('stops.html', options=options)


@app.route('/stops/timetable', methods=['POST'])
def timetable():
    return render_template('timetable.html')
