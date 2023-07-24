# Python standard libraries

# Third-party libraries
from flask import Flask, request, jsonify

from api.assistant import skill_q_and_a
from api.v1.connector_routes import connector_routes

# Flask app setup
app = Flask(__name__)


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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
