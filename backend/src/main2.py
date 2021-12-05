# coding=utf-8

from flask import Flask

import constants
from tower import Tower
from weathergenerator import WeatherGenerator


# Create the Flask application.
app = Flask(__name__)

wg = WeatherGenerator()

tower = Tower(constants.NUM_PLANES,
              constants.NUM_GATES,
              wg)


def to_html(departures, arrivals):
    html = '<head>'
    html += '<style>'
    html += 'table {'
    html += 'font-family: arial, sans-serif;'
    html += 'border-collapse: collapse;'
    html += 'width: 100%;'
    html += '}'

    html += 'td, th {'
    html += 'border: 1px solid #dddddd;'
    html += 'text-align: left;'
    html += 'padding: 8px;'
    html += '}'

    html += 'tr:nth-child(even) {'
    html += 'background-color: #dddddd;'
    html += '}'
    html += '</style>'
    html += '</head>'

    html += '<h2>Departure</h2>'
    html += f'<table>'
    html += f'<tr><th>Plane</th><th>Flight</th><th>Gate</th><th>Time</th><th>State</th></tr>'
    for plane in departures:
        gate = plane.gate

        if not gate:
            gate = ''
        html += f'<tr><td>{plane.plane_id}</td><td>{plane.flight_info.flight_number}</td><td>{gate}</td><td>{plane.flight_info.departure_time}</td><td>{plane.state}</td></tr>'
    html += f'</table>'

    html += '<h2>Arrivals</h2>'
    html += f'<table>'
    html += f'<tr><th>Plane</th><th>Flight</th><th>Gate</th><th>Time</th><th>State</th></tr>'
    for plane in arrivals:
        gate = plane.gate
        if not gate:
            gate = ''
        html += f'<tr><td>{plane.plane_id}</td><td>{plane.flight_info.flight_number}</td><td>{gate}</td><td>{plane.flight_info.arrival_time}</td><td>{plane.state}</td></tr>'
    html += f'</table>'
    
    return html
    

@app.route('/atcs')
def get_next():
    tower.step_time()

    return f'<h1>Scarlet Knight Airways: Time={tower.time}</h1>' + \
        to_html(tower.departures, tower.arrivals)


if __name__=='__main__':
    app.run(debug=True)
