

import asyncio
import aiohttp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
from gimmemydata.config import Config
import time
import json
import boto3
import requests
import datetime
import requests
import spotipy.util as util

SPOTIFY_CLIENT_ID = Config().get_param('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = Config().get_param('SPOTIFY_CLIENT_SECRET')
S3_BUCKET_NAME = Config().get_param('S3_BUCKET_NAME')
SPOTIFY_USERNAME = Config().get_param('SPOTIFY_USERNAME')
POLL_INTERVAL = 3600
SPOTIFY_REDIRECT_URI = 'https://irregular-expressions.com'

# # # Set up Spotify API client
spotify_auth_url = 'https://accounts.spotify.com/api/token'
spotify_api_url = 'https://api.spotify.com/v1/me/player/recently-played'

SCOPE = 'user-read-recently-played'
CACHE_PATH = './.cache-samjulius'

sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE_PATH)

def get_spotify_history():
    # Create a new SpotifyOAuth object with client ID, client secret, redirect URI, and scope
    

    # Get access token from cache or prompt user to authorize
    access_token = sp_oauth.get_access_token(as_dict=False, check_cache=True)[0]

    # Build Spotify API request URL
    spotify_api_url = 'https://api.spotify.com/v1/me/player/recently-played'

    # Make Spotify API request with access token
    retries = 3
    for i in range(retries):
        response = requests.get(
            spotify_api_url,
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        if response.status_code == 200:
            response_json = response.json()
            track_ids = [item['track']['id'] for item in response_json['items']]
            return track_ids
        elif response.status_code == 401:
            # If access token is expired, refresh token and get new access token
            sp_oauth.refresh_access_token(sp_oauth.get_cached_token()['refresh_token'])
            access_token = sp_oauth.get_cached_token()['access_token']
            print('Refreshed access token:', access_token)
        elif response.status_code == 500:
            print(f'Server error, retrying in {i+1} seconds...')
            time.sleep(i+1)
        else:
            raise Exception(f'Request failed with status code {response.status_code}: {response.text}')
    raise Exception('Maximum retries exceeded, request failed.')


async def get_audio_features(track_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.spotify.com/v1/audio-features/{track_id}', headers={
            'Authorization': f'Bearer {access_token}'
        }) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json
            elif response.status == 401:
                # If access token is expired, refresh token and get new access token
                sp_oauth.refresh_access_token(sp_oauth.get_cached_token()['refresh_token'])
                access_token = sp_oauth.get_cached_token()['access_token']
                print('Refreshed access token:', access_token)
            else:
                raise Exception(f'Request failed with status code {response.status}: {await response.text()}')

async def get_audio_features_for_all_tracks(track_ids):
    tasks = [get_audio_features(track_id) for track_id in track_ids]
    return await asyncio.gather(*tasks)
