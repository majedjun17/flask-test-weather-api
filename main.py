from flask import Flask, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

@app.route('/list', methods=['POST'])
def events():
    conn = sqlite3.connect('general.db')
    c = conn.cursor()
    country = request.form.get('country', type=str)
    if country is not '' and country is not None:
        pass
    else:
        return jsonify({'error': 'Provide a country'}), 400
    r = c.execute('SELECT * FROM event WHERE country = ? AND created_at >= datetime("now", "-6 hours")', (country,))
    for i in r:
        return jsonify(i)
    response = requests.get(
        url="https://api.predicthq.com/v1/events/",
        headers={
        "Authorization": "Bearer EqpJf87ypBIW6cbbhkXRj_HOyxkNezMRw66NdI86",
        "Accept": "application/json"
        },
        params={
            "country": country
        }
    )
    if response.status_code != 200:
        return jsonify(response.json())
    res = response.json()['results']
    sorted_data = sorted(res, key=lambda x: x['rank'])
    sorted_data = sorted_data[0:10]
    lst = []
    for i in sorted_data:
        lst.append([i['id'], i['rank'], i['geo']['geometry']['coordinates']])
    

    for i in lst:
        c.execute("INSERT INTO event (id, rank, long, lat, country) VALUES (?, ?, ?, ?, ?)", 
            (i[0], int(i[1]), i[2][0], i[2][1], country))
        conn.commit()
    conn.close()
    return jsonify(lst)
#========================================================================================================

@app.route('/weather', methods=['POST'])
def weather():
    EventId = request.form.get('EventId', type=str)
    if EventId is not '' and EventId is not None:
        pass
    else:
        return jsonify({'error': 'Provide a EventId'}), 400
    conn = sqlite3.connect('general.db')
    c = conn.cursor()
    r = c.execute('SELECT * FROM weather WHERE id = ? AND created_at >= datetime("now", "-6 hours")', (EventId,))
    for i in r:
        return jsonify({'temp': i[1], 'humidity':i[2]})
    row = c.execute('SELECT long, lat FROM event where id = (?)', (EventId,))
    lat = 10000
    lon = 10000
    for i in row:
        lon = i[0]
        lat = i[1]
    API_KEY = "f22892654725839a44ff6db985f0b151"
    if lat == 10000:
        return jsonify({'error': 'Provide a valid EventID'}), 400

    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}")
    if response.status_code != 200:
        return jsonify(response.json())
    c.execute("INSERT INTO weather (id, temp, humidity) VALUES (?, ?, ?)", 
           (EventId, response.json()['main']['temp'], response.json()['main']['humidity']))
    conn.commit()
    conn.close()
    return jsonify({'temp': response.json()['main']['temp'], 'humidity':response.json()['main']['humidity']})
    



if __name__ == '__main__':
    app.run(debug=True, port=80)
