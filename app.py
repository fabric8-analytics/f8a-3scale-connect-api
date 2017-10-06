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


if __name__ == "__main__":
    app.run()
