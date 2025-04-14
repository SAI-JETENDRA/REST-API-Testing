from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app, resources={
    r"/test_api": {
        "origins": ["http://localhost:3000"],  # Add your React app's origin
        "methods": ["POST"],  # Allow POST requests to /test_api
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/test_api', methods=['POST'])
def test_api():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    try:
        data = request.get_json()
        api_method = data.get('apiMethod')
        api_url = data.get('apiURL')
        api_body = data.get('apiBody')
        api_headers = data.get('apiHeaders', {})

        # Validate required fields
        if not api_method:
            return jsonify({"error": "API method is required"}), 400
        if not api_url:
            return jsonify({"error": "API URL is required"}), 400

        # Make the actual API request
        response = requests.request(
            method=api_method,
            url=api_url,
            headers=api_headers,
            json=api_body if api_body else None
        )

        # Prepare the response
        response_data = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
        }

        # Handle different response types
        if response.status_code == 204:
            response_data["data"] = None
        else:
            try:
                response_data["data"] = response.json()
            except ValueError:
                response_data["data"] = response.text

        return jsonify(response_data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5500)