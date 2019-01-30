import os
from stravalib import Client, exc, model
from requests.exceptions import ConnectionError, HTTPError
import requests
import csv
import time
from datetime import datetime

def get_name(access_token):
    client = Client()
    client.access_token = access_token
    athlete = client.get_athlete()
    return athlete.firstname + " " + athlete.lastname

