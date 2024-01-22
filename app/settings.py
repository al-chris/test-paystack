# This is the settings.py file

from os import environ
SECRET_KEY = environ.get('SECRET_KEY')
PAYSTACK_SECRET_KEY = environ.get('PAYSTACK_SECRET_KEY')