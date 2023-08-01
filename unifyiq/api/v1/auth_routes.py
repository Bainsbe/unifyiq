import random
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, unset_jwt_cookies

from utils.configs import get_admin_emails, get_otp_email, get_otp_password
from utils.database.otpuser_db import get_user, add_user_otp, update_user_otp

auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.route('verified_email', methods=['POST'])
def verified_email():
    data = request.get_json()
    email = data.get('email')
    white_list = get_admin_emails()
    if email in white_list:
        return {'message': 'Email in whitelist'}, 200
    else:
        return jsonify({'error': 'Email is not in whitelist'}), 400


def generate_otp():
    digits = "0123456789"
    otp = ''.join(random.choice(digits) for i in range(6))
    return otp


def send_otp_emai(email, otp):
    # sender_email = 'ha.testotp@gmail.com'
    sender_email = get_otp_email()
    sender_password = get_otp_password()
    receiver_email = email
    subject = 'Important! OTP for complete the sign up for your UnifyIQ account'
    body = f'Your OTP is: {otp}'
    smtp_server = 'smtp.gmail.com'
    port = 587
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send OTP to {email}: {e}")


def check_valid_otp(email, otp, time):
    user = get_user(email)
    otp_saved = user['otp']
    otp_created_at = user['created_at']
    if time <= (otp_created_at.timestamp() + 15 * 60) and otp == otp_saved:
        return True
    else:
        return False


# def generate_token(user_id):
#     expires_in = datetime.now(pytz.utc) + timedelta(minutes=10)
#     payload = {
#         'user_id': user_id,
#         'exp': expires_in,
#     }
#     token = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm='HS256')
#     print('token', token)
#     return token


@auth_routes.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')
    otp = generate_otp()
    try:
        send_otp_emai(email, otp)
    except Exception as e:
        return jsonify({'error: Failed to sent OTP'}), 500
    user = get_user(email)

    now = datetime.now()

    if user != None and user['email']:
        update_user_otp(email, otp, now)
    else:
        add_user_otp(email, otp, False)
    return jsonify({'message': 'OTP sent successfully'}), 200


@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    time = data.get('time')
    user = get_user(email)
    if (check_valid_otp(email, otp, time)):
        # token = generate_token(user['id'])
        token = create_access_token(identity=email)
        return jsonify({
            'message': 'Login succesfully',
            'userId': user['id'],
            'token': token
        }), 201
    else:
        return jsonify({'error': 'Invalid OTP or OTP is expired'}), 400


@auth_routes.route('/logout', methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
