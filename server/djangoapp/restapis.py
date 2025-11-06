import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url', default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    """Make a GET request to the backend API."""
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += key + "=" + str(value) + "&"

    request_url = backend_url + endpoint
    if params:
        request_url += "?" + params

    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        return response.json()
    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")


def analyze_review_sentiments(text):
    """Analyze sentiment of a given text."""
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url)
        return response.json()
    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")


def post_review(data_dict):
    """Post review data to backend."""
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")
