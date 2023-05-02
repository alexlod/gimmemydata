#!/usr/bin/env python3

import requests

class OAuth2:
    def __init__(self, client_id, client_secret, token_url, redirect_uri=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.redirect_uri = redirect_uri

    def get_access_token(self, code=None, refresh_token=None):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        if code:
            payload.update({
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': self.redirect_uri,
            })
        elif refresh_token:
            payload.update({
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            })

        response = requests.post(self.token_url, data=payload)
        response.raise_for_status()

        return response.json()
