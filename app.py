from flask import Flask, request, jsonify
import os
import json
import requests

app = Flask(__name__)


PERSISTENT_STORAGE_PATH = "/disha_PV_dir/"
CONTAINER_2_URL = "http://container2:5000/process"

os.makedirs(PERSISTENT_STORAGE_PATH, exist_ok=True)

@app.route('/store-file', methods=['POST'])
def store_file():
    if request.content_type != "application/json":
        return jsonify({"file": None, "error": "Unsupported Media Type"}), 415
    
    try:
        data = request.get_json()
        if not data or "file" not in data or "data" not in data:
            return jsonify({"file": None, "error": "Invalid JSON input."}), 400
        
        file_name = data["file"]
        file_data = data["data"]
        
        if not isinstance(file_name, str) or not isinstance(file_data, str):
            return jsonify({"file": None, "error": "Invalid JSON input."}), 400
        
        file_path = os.path.join(PERSISTENT_STORAGE_PATH, file_name)
        
        with open(file_path, 'w') as f:
            f.write(file_data)
        
        return jsonify({"file": file_name, "message": "Success."}), 200
    except Exception as e:
        return jsonify({"file": None, "error": str(e)}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    if request.content_type != "application/json":
        return jsonify({"file": None, "error": "Unsupported Media Type"}), 415
    
    try:
        data = request.get_json()
        if not data or "file" not in data or "product" not in data:
            return jsonify({"file": None, "error": "Invalid JSON input."}), 400
        
        file_name = data["file"]
        product = data["product"]

        if not isinstance(file_name, str) or not isinstance(product, str):
            return jsonify({"file": None, "error": "Invalid JSON input."}), 400

        file_path = os.path.join(PERSISTENT_STORAGE_PATH, file_name)
        
        if not os.path.isfile(file_path):
            return jsonify({"file": file_name, "error": "File not found."}), 404
        
        response = requests.post(CONTAINER_2_URL, json={"file": file_name, "product": product}, headers={"Content-Type": "application/json"})
        
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"file": None, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
