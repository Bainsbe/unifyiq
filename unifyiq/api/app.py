# Python standard libraries

import json
from datetime import datetime, timedelta, timezone

# Third-party libraries
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
    JWTManager

from api.assistant import skill_q_and_a
from api.v1.auth_routes import auth_routes
from api.v1.connector_routes import connector_routes
from utils.configs import get_jwt_secret_key

# Flask app setup
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = get_jwt_secret_key()
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=60))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        question = request.form['question']
        print("Question: ", question)
        answer = skill_q_and_a(question)
        response_obj = {'status': 'success', 'answer': answer}
        return jsonify(response_obj)
    except Exception as e:
        print('Exception')
        response_obj = {'status': 'failed', 'reason': str(e)}
        return jsonify(response_obj)


app.register_blueprint(connector_routes, url_prefix='/api/v1/connectors')
app.register_blueprint(auth_routes, url_prefix='/api/v1/auth')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
