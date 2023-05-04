

from manage.config import Config
from utils.render import DBClient
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyAuth:
    def __init__(self):
        self.SPOTIFY_CLIENT_ID = Config().get_param('SPOTIFY_CLIENT_ID')
        self.SPOTIFY_CLIENT_SECRET = Config().get_param('SPOTIFY_CLIENT_SECRET')
        self.SPOTIFY_REDIRECT_URI = 'https://irregular-expressions.com'
        self.SCOPE = 'user-read-recently-played'
        
        self.sp_oauth = SpotifyOAuth(client_id=self.SPOTIFY_CLIENT_ID, client_secret=self.SPOTIFY_CLIENT_SECRET, redirect_uri=self.SPOTIFY_REDIRECT_URI, scope=self.SCOPE)
        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)

        # Set up DB Connection for Auth
        self.conn = DBClient().connection
        self.cur = self.conn.cursor()

    def get_tokens_from_db(self):
        conn = self.db_client.connection
        cur = conn.cursor()
        cur.execute("SELECT access_token, refresh_token, expiration_timestamp FROM gimmemydata_auth WHERE datasource = %s", ('spotify',))
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
            ('spotify', access_token, refresh_token, expiration_timestamp)
        )
        self.conn.commit()

    def _refresh_token(self, token_info):
        refreshed_token = self.sp_oauth.refresh_access_token(token_info['refresh_token'])
        self._update_token_in_db(refreshed_token)
        return refreshed_token['access_token']

    def get_valid_access_token(self):
        token_info = self.sp_oauth.get_cached_token()
        if not token_info:
            auth_url = self.sp_oauth.get_authorize_url()
            print("Please navigate to the following URL to authorize the app:")
            print(auth_url)
            response = input("Enter the URL you were redirected to: ")
            code = self.sp_oauth.parse_response_code(response)
            token_info = self.sp_oauth.get_access_token(code)
        
        if self.sp_oauth.is_token_expired(token_info):
            access_token = self._refresh_token(token_info)
        else:
            access_token = token_info['access_token']

        return access_token

