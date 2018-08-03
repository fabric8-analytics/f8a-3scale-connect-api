import flask
from flask import Flask
from flask import Flask, render_template, request, json
from flask_api import status
import utils
import jwt

app = Flask(__name__)

@app.route('/api/v1/readiness')
def readiness():
    """Generate response for the GET request to /api/v1/readiness."""
    return flask.jsonify({}), 200


@app.route('/api/v1/liveness')
def liveness():
    """Generate response for the GET request to /api/v1/liveness."""
    return flask.jsonify({}), 200


@app.route('/get-route', methods=['POST'])
def get_route():
    params = request.get_json()
    _auth = params.get('auth_token')
    _servID = params.get('service_id')
    if not _auth:
        return json.dumps({"error": "missing or invalid auth token"}), status.HTTP_404_NOT_FOUND
    else:
        try:
            decoded = jwt.decode(_auth, verify=False)
        except Exception:
            return json.dumps({"error": "unauthorized"}), status.HTTP_401_UNAUTHORIZED
        else:
            response = utils.get_route(_servID)
            return json.dumps(response)

@app.route('/get-endpoints', methods=['GET'])
def get_endpoints():
    _auth = request.headers.get('Authorization')
    if not _auth:
        return json.dumps({"error": "missing or invalid auth token"}), status.HTTP_404_NOT_FOUND
    else:
        try:
            decoded = jwt.decode(_auth, verify=False)
        except Exception:
            return json.dumps({"error": "unauthorized"}), status.HTTP_401_UNAUTHORIZED
        else:
            response = utils.get_endpoints()
            return json.dumps(response)


if __name__ == "__main__":
    app.run()
