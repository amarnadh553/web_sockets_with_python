import sqlite3
import asyncio
import websockets
import matplotlib.pyplot as plt
from flask import Flask, render_template, send_file
from io import BytesIO

DB_NAME = "languages.db"

app = Flask(__name__)

def create_database(db_name):
    connection = sqlite3.connect(db_name)
    connection.close()

def create_table(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS languages (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      language TEXT NOT NULL,
                      score INTEGER NOT NULL)''')
    connection.commit()
    connection.close()

def insert_data(data):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO languages (language, score) VALUES (?, ?)''',
                   (data['language'], data['score']))
    connection.commit()
    connection.close()

def get_data(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = '''SELECT * FROM languages'''
    c.execute(query)
    result = c.fetchall()
    return result

def fetch_data(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM languages")
    data = cursor.fetchall()
    connection.close()
    return data

def plot_data(data):
    languages = [row[1] for row in data]
    scores = [row[2] for row in data]
    plt.bar(languages, scores, color='skyblue')
    plt.xlabel('Languages')
    plt.ylabel('Scores')
    plt.title('Programming Language Scores')
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    plt.close()
    return img_data

@app.route('/')
def index():
    data = fetch_data(DB_NAME)
    img_data = plot_data(data)
    return send_file(img_data, mimetype='image/png')

async def handle_client(websocket, path):
    while True:
        data = fetch_data(DB_NAME)
        img_data = plot_data(data)
        await asyncio.sleep(5)  # Update the graph every 5 seconds

if __name__ == "__main__":
    create_database(DB_NAME)
    create_table(DB_NAME)
    data_to_insert = [{'language': 'C++', 'score': 88},
                  {'language': 'R', 'score': 70},
                  {"language":"Cobra", "score": 90},
                  {"language":"Python", "score": 100},
                  {"language":"Go", "score": 10},
                  {"language":"Java", "score": 25}
]
    for i in data_to_insert:
        insert_data(i)

    print("Inserted all the data into DB")

    start_server = websockets.serve(handle_client, "localhost", 8765)

    asyncio.ensure_future(start_server)
    asyncio.ensure_future(app.run(port=5000))

    asyncio.get_event_loop().run_forever()
