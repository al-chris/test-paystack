from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, redirect
import requests

# PAYSTACK_SECRET_KEY = '' # Save this in a environmental variable
PAYSTACK_API_BASE_URL = 'https://api.paystack.co'

app = Flask(__name__)
load_dotenv()
app.config.from_pyfile('settings.py')

@app.get('/home')
def home():
  return render_template("index.html")


@app.route('/api/payment', methods=['POST'])
def initialize_payment():
    try:
        # Get data from the request
        data = {'email': request.form.get('email-address'), 'amount': request.form.get("amount")}

        # Ensure required data is present in the request
        if 'amount' not in data or 'email' not in data:
            return jsonify({'error': 'Amount and email are required'}), 400

        # Prepare payload for Paystack API
        payload = {
            'email': data['email'],
            'amount': int(data['amount']) * 100,  # Paystack uses amount in kobo (multiply by 100)
            'currency': 'NGN',  # Adjust as needed
        }

        # Make request to Paystack API to initialize payment
        response = requests.post(
            f'{PAYSTACK_API_BASE_URL}/transaction/initialize',
            headers={'Authorization': f'Bearer {app.config.get("PAYSTACK_SECRET_KEY")}'},
            json=payload
        )

        print(payload)

        # Check for success and return the payment URL to the client
        if response.status_code == 200:
            data = response.json()
            print(data['data']['authorization_url'])
            return jsonify({'payment_url': data['data']['authorization_url']})
            # return redirect(data['data']['authorization_url'])

        # Return error if the request to Paystack fails
        return jsonify({'error': 'Unable to initialize payment'}), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    