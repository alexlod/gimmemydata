
import requests
import datetime
from datasources.spotify.auth import SpotifyAuth
import time

class SpotifyClient:
    def __init__(self):
        self.spotify_auth = SpotifyAuth()
        self.access_token = self.spotify_auth.get_valid_access_token()
        self.api_url = 'https://api.spotify.com/v1/me/'
        self.headers = {
            'Authorization': f'token {self.access_token}',
        }
    
    def get_recently_played(self, start_date=None):

        # Create SpotifyAuth instance
        spotify_auth = SpotifyAuth()
        access_token = spotify_auth.get_valid_access_token()

        # Build Spotify API request URL
        url = self.api_url + 'player/recently-played'

        # Make Spotify API request with access token
        retries = 3
        for i in range(retries):
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                response_json = response.json()
                filtered_history = [track for track in response_json['items'] if datetime.datetime.strptime(track['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ') > start_date]
                return filtered_history

            elif response.status_code == 500:
                print(f'Server error, retrying in {i+1} seconds...')
                time.sleep(i+1)
            else:
                raise Exception(f'Request failed with status code {response.status_code}: {response.text}')
        raise Exception('Maximum retries exceeded, request failed.')