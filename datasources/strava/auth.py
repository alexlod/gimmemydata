
from manage.config import Config
from utils.render import DBClient
from stravalib.client import Client
import time
import datetime

class StravaAuth:
    def __init__(self):
        self.STRAVA_CLIENT_ID = Config().get_param('STRAVA_CLIENT_ID')
        self.STRAVA_CLIENT_SECRET = Config().get_param('STRAVA_CLIENT_SECRET')
        self.STRAVA_REFRESH_TOKEN = Config().get_param('STRAVA_REFRESH_TOKEN')
        self.STRAVA_REDIRECT_URI = 'http://localhost:8282/authorized'
        self.client = Client()

        # Set up DB Connection for Auth
        self.conn = DBClient().connection
        self.cur = self.conn.cursor()
    
    def authorize_app(self):
        authorize_url = self.client.authorization_url(client_id=self.STRAVA_CLIENT_ID, redirect_uri=self.STRAVA_REDIRECT_URI)
        print('Go to the following URL and authorize the application:')
        print(authorize_url)
        
        # Extract the code from your webapp response
        code = input('Paste the code here and press Enter: ')
        token_response = self.client.exchange_code_for_token(client_id=self.STRAVA_CLIENT_ID, client_secret=self.STRAVA_CLIENT_SECRET, code=code)
        access_token = token_response['access_token']
        refresh_token = token_response['refresh_token']
        expires_at = token_response['expires_at']
        self._update_token_in_db(access_token, refresh_token, expires_at)

    def get_tokens_from_db(self):
        conn = self.db_client.connection
        cur = conn.cursor()
        cur.execute("SELECT access_token, refresh_token, expiration_timestamp FROM gimmemydata_auth WHERE datasource = %s", ('strava',))
        row = cur.fetchone()
        return row

    def _update_token_in_db(self, access_token, refresh_token, expiration_timestamp):
        self.cur.execute(
            """
            INSERT INTO gimmemydata_auth (datasource, access_token, refresh_token, expiration_timestamp) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (datasource) DO UPDATE SET 
            access_token = EXCLUDED.access_token, 
            refresh_token = EXCLUDED.refresh_token, 
            expiration_timestamp = EXCLUDED.expiration_timestamp;
            """,
            ('strava', access_token, refresh_token, expiration_timestamp)
        )
        self.conn.commit()

    def _refresh_token(self):
        token_response = self.client.refresh_access_token(client_id=self.STRAVA_CLIENT_ID, client_secret=self.STRAVA_CLIENT_SECRET, refresh_token=self.STRAVA_REFRESH_TOKEN)
        access_token = token_response['access_token']
        expiration_timestamp = token_response['expires_at']
        self.client.access_token = access_token
        print(f'Got new access token expiring at {datetime.datetime.fromtimestamp(expiration_timestamp)}')
        self._update_token_in_db(access_token, token_response['refresh_token'], expiration_timestamp)
    
    def init_client(self):

        # Initialize Strava API client and authenticate with access token
        print('Initializing Strava API client...')
        self.client.access_token = None
        expiration_timestamp = None
        
        # Check if access_token is still valid
        self.cur.execute("SELECT access_token, expiration_timestamp FROM gimmemydata_auth WHERE datasource = %s", ('strava',))
        row = self.cur.fetchone()
        access_token, expiration_timestamp = row

        if access_token and expiration_timestamp > time.time():
            self.client.access_token = access_token
            print(f'Using existing access token expiring at {expiration_timestamp}')
        else:
            print('No valid access token found, refreshing...')
            self._refresh_token()

        return self.client