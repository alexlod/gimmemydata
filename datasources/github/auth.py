from manage.config import Config
from utils.render import DBClient
from requests_oauthlib import OAuth2Session
import re

class GithubAuth:
    def __init__(self):
        self.GITHUB_CLIENT_ID = Config().get_param('GITHUB_CLIENT_ID')
        self.GITHUB_CLIENT_SECRET = Config().get_param('GITHUB_CLIENT_SECRET')
        self.AUTH_REDIRECT_URI = 'https://localhost:3000/api/auth/callback/github'
        self.GITHUB_AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
        self.GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
        self.SCOPES = ["repo,user"]
        
        # Set up DB Connection for Saving Auth Credentials
        self.conn = DBClient().connection
        self.cur = self.conn.cursor()

        self.gh_oauth = OAuth2Session(self.GITHUB_CLIENT_ID, scope=self.SCOPES, redirect_uri=self.AUTH_REDIRECT_URI)
        self.access_token = self.get_valid_access_token()

    def get_tokens_from_db(self):
        self.cur.execute("SELECT access_token, refresh_token, expiration_timestamp FROM gimmemydata_auth WHERE datasource = %s", ('github',))
        row = self.cur.fetchone()
        if row:
            return {"access_token": row[0], "refresh_token": row[1], "expiration_timestamp": row[2]}
        return row

    def get_github_authorize_url(self):
        authorization_url, state = self.gh_oauth.authorization_url(self.GITHUB_AUTHORIZATION_BASE_URL)
        return authorization_url

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
            ('github', access_token, refresh_token, expiration_timestamp)
        )
        self.conn.commit()
        print("Token updated in DB:", access_token)

    def get_valid_access_token(self):
        token_info = self.get_tokens_from_db()
        
        if token_info:
            return token_info['access_token']

        auth_url = self.get_github_authorize_url()
        
        print("Please navigate to the following URL to authorize the app:")
        print(auth_url)
        response = input("Enter the URL you were redirected to: ")
        
        # Extract the code from the response URL
        code = re.search('code=([^&]+)', response).group(1)
        print(f'code: {code}')

        token = None 
        try:
            token = self.gh_oauth.fetch_token(self.GITHUB_TOKEN_URL, client_secret=self.GITHUB_CLIENT_SECRET, code=code)
            print("Token fetched from Github: ", token['access_token'])
        
        except Exception as e:
            print(f"Error fetching token from Github: {e}")
            return None
        
        self._update_token_in_db(token["access_token"], None, None)
        self.access_token = token["access_token"]  # Update the access_token attribute
        self.conn.close()  # Close the database connection

        return token["access_token"]

    def close(self):
        self.gh_oauth.close()