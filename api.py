from flask import Flask, jsonify
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)

@app.route('/')  # Route racine
def home():
    return "Welcome to the API!"

@app.route('/read/first-chunk', methods=['GET'])
def get_first_chunk():
    logging.info("Fetching the first chunk of data from the database.")
    try:
        conn = sqlite3.connect("my_database.db")  # Assurez-vous que ce chemin correspond à celui utilisé dans etl.py
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data LIMIT 10")
        results = cursor.fetchall()
        conn.close()
        return jsonify([dict(zip([key[0] for key in cursor.description], row)) for row in results]), 200
    except Exception as e:
        logging.error("Error fetching data: %s", str(e))
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
