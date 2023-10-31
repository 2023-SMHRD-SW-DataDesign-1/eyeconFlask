from flask import Flask, request
import requests
import json
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, supports_credentials=False)

@app.route('/eye', methods=['POST'])
@cross_origin(origins="http://localhost:3000")
def eye():
    data = request.get_json()
    print(data)
    print(data.beforeimg)

    return
if __name__ == '__main__':
    app.run(debug=True)