import requests
import os
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv('OMDB_API_KEY')

def omdb_movie_data(title):
    api_key = OMDB_API_KEY 
    url = f'http://www.omdbapi.com/?t={title}&apikey={api_key}'
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None