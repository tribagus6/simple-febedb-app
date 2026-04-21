from flask import Flask, jsonify
import requests
import logging # <-- Standard Python logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/hello')
def hello():
    # Write a log message! OpenTelemetry will magically attach the trace ID to this.
    logger.info("Service A is preparing to call Service B...")
    
    response = requests.get('http://service-b:5002/data')
    
    logger.info("Service A successfully received data from Service B!")
    
    return jsonify({
        "message": "Hello from Service A!",
        "service_b_says": response.json()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
