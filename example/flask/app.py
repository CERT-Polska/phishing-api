import time
import requests
import re
import binascii

from flask import Flask, jsonify, request, make_response
from itsdangerous import TimedJSONWebSignatureSerializer
from itsdangerous.exc import BadData
from werkzeug.exceptions import Forbidden

import config


app = Flask(__name__)

jwt_secret = binascii.unhexlify(config.JWT_SECRET)
s = TimedJSONWebSignatureSerializer(jwt_secret, expires_in=300)


@app.route('/push', methods=['OPTIONS', 'POST'])
def route_push():
    if request.method == 'OPTIONS':
        res = make_response()
        res.headers['X-PUSHAPI-CERT-PL'] = 'https://www.cert.pl/ostrzezenia_phishing'
        res.headers['X-PUSHAPI-CERT-PL-UID'] = config.AUTH_UID
        return res

    try:
        obj = s.loads(request.form['jwt'])
    except BadData:
        raise Forbidden('Invalid jwt provided.')

    print('Received object:', obj)
    # TODO implement your logic here
    return 'OK'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

