from flask import Flask, jsonify
import requests
import logging
import time 

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Internal Functions (Clean) ---

def validate_request():
    """Simulates validating incoming parameters."""
    logger.info("Validating internal request state...")
    time.sleep(0.1) 
    return True

def prepare_payload():
    """Simulates heavy data processing before making the external call."""
    logger.info("Preparing data payload for Service B...")
    time.sleep(0.2) 
    return {"lab_environment": "platypus-lab01", "action": "fetch_data"}

def format_response(raw_data):
    """Simulates formatting the response before sending it back to the user."""
    logger.info("Formatting final response object...")
    time.sleep(0.05) 
    return {
        "status": "success",
        "raw_service_b_data": raw_data,
        "processed": True
    }

# --- Main Web Route ---

@app.route('/hello')
def hello():
    logger.info("Service A received a request at /hello")
    
    if validate_request():
        payload_context = prepare_payload()
        
        logger.info(f"Calling Service B... (Context: {payload_context['lab_environment']})")
        response = requests.get('http://python-b.pamungkas.cloud/data') 
        
        final_output = format_response(response.json())
        logger.info("Service A successfully completed all tasks!")
        
        return jsonify({
            "message": "Hello from Service A!",
            "data": final_output
        })
    else:
        return jsonify({"error": "Validation failed"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
