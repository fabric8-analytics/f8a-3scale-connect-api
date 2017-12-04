from flask import Flask
from flask import Flask, render_template, request, json
import utils
import jwt

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    params = request.get_json()
    _auth = params['auth_token']
    decoded = jwt.decode(_auth, verify=False)
    company = decoded['company']
    response = utils.register(company)
    print ('Inside register')
    print(response)
    #return _auth
    return json.dumps(response)

@app.route('/get-route', methods=['POST'])
def get_route():
    params = request.get_json()
    _auth = params.get('auth_token')
    _servID = params.get('service_id')
    if not _auth:
        return json.dumps({"error": "Bad request"})
    else:
        try:
            decoded = jwt.decode(_auth, verify=False)
        except Exception:
            return json.dumps({"error": "unauthorized"})
        else:
            company = decoded['company']
            response = utils.get_route(_servID)
            return json.dumps(response)


if __name__ == "__main__":
    app.run()
