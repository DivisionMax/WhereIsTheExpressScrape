import requests
from bs4 import BeautifulSoup
from flask import Flask
import csv



route_timetable_url = 'https://myciti.org.za/en/timetables/route-stop-timetables/'

# Response.content

response = requests.get(route_timetable_url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')
stops = soup.find('select', attrs={'id': 'stations', 'name': 'timetable[station]'})

headers = ['id', 'name']

with open('stops.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(headers)
    for stop in stops.find_all('option'):
        id = stop.get('value')
        name = stop.text
        writer.writerow([id, name])

