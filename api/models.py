from django.db import models

from db_connection import db

users_collection = db['users']

banks_collection = db['banks']

deposits_collection = db['deposits']

loans_collection = db['loans']

transactions_collection = db['transactions']