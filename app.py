from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/stops', methods=['GET'])
def stops():
    return render_template('stops.html')


@app.route('/stops/timetable', methods=['POST'])
def timetable():
    return render_template('timetable.html')
