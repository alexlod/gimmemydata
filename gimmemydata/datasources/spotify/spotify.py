
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


def write_to_s3(file_content, s3_key):
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=s3_key,
        Body=file_content
    )

def get_spotify_history():
    # Create a new SpotifyOAuth object with client ID, client secret, redirect URI, and scope
    sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE_PATH)

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
            return response_json['items']
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


while True:

    # Get the most recent timestamp from S3
    s3 = boto3.client('s3')
    try:
        s3_objects = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix='spotify/recently-played/', MaxKeys=1)['Contents']
        latest_object = s3_objects[0]
        latest_timestamp = latest_object['Key'].split('/')[-1].split('.')[0]
    except KeyError:
        # If there are no objects in the S3 bucket, set latest_timestamp to a very old timestamp to retrieve all records
        latest_timestamp = '20000101000000'

    # Remove microseconds from the latest timestamp to avoid precision errors
    latest_timestamp = latest_timestamp[:-6]

    # Retrieve listening history from Spotify API
    history = get_spotify_history()

    # Filter out tracks that have already been saved to S3
    filtered_history = [track for track in history if track['played_at'] > latest_timestamp]

    # Get current timestamp and directory path
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    directory_path = datetime.datetime.now().strftime('spotify/recently-played/%Y/%m/%d/%H/')

    # Write data to S3
    if len(filtered_history) > 0:
        s3_key = directory_path + timestamp + '.json'
        file_content = json.dumps(filtered_history).encode('utf-8')
        write_to_s3(file_content, s3_key)

    # Wait for some time before retrieving the next batch of data
    time.sleep(int(POLL_INTERVAL))

























# def get_spotify_access_token():
#     # Retrieve access token from Spotify API
#     response = requests.post(
#         spotify_auth_url,
#         headers={
#             'Content-Type': 'application/x-www-form-urlencoded'
#         },
#         data={
#             'grant_type': 'client_credentials',
#             'client_id': SPOTIFY_CLIENT_ID,
#             'client_secret': SPOTIFY_CLIENT_SECRET,
#             'scope': 'user-read-recently-played'
#         }
#     )
#     response_json = response.json()
#     return response_json['access_token']


# token = util.prompt_for_user_token(username=SPOTIFY_USERNAME, 
#                                    scope=scope, 
#                                    client_id=SPOTIFY_CLIENT_ID,   
#                                    client_secret=SPOTIFY_CLIENT_SECRET,     
#                                    redirect_uri=SPOTIFY_REDIRECT_URI)



# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
# auth_manager = auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
# sp = spotipy.Spotify(auth_manager=auth_manager)

# results = sp.current_user_recently_played(limit=50,after=None,before=None)
# for idx, track in enumerate(results['tracks']['items']):
    # print(idx, track['name'])