from flask import Flask, jsonify
import psycopg2
import logging # <-- Standard Python logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='10.0.1.50',
        database='mydb',
        user='myuser',
        password='mypassword'
    )
    return conn

@app.route('/data')
def get_data():
    logger.info("Service B received request, connecting to PostgreSQL...") # <-- New Log
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT 42 as answer;')
    result = cur.fetchone()
    
    cur.close()
    conn.close()
    
    logger.info(f"Service B successfully fetched result: {result[0]}") # <-- New Log
    
    return jsonify({"message": "Successfully queried the database!", "db_result": result[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

