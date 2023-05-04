
import requests
import datetime
from datasources.github.auth import GithubAuth

class GithubClient:
    def __init__(self):
        self.gh_auth = GithubAuth()
        self.access_token = self.gh_auth.get_valid_access_token()
        self.headers = {
            'Authorization': f'token {self.access_token}',
        }
        self.user_url = self.get_authenticated_user_url()

    def get_authenticated_user_url(self):
        res = requests.get('https://api.github.com/user', headers=self.headers)
        data = res.json()
        return data['url']

    def get_user(self):
        res = requests.get(self.user_url, headers=self.headers)
        return res.json()

    def fetch_events_paginated(self, start_date=None, end_date=None):
        events = []
        url = self.user_url + '/events'
        while url:
            res = requests.get(url, headers=self.headers)
            data = res.json()

            # Iterate through the events and check the event_created_at date
            for event in data:
                event_created_at = datetime.datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                if start_date <= event_created_at <= end_date:
                    events.append(event)
                elif event_created_at < start_date:
                    break

            # Check if there is a 'next' page in the Link header
            link_header = res.headers.get('Link')
            next_link = None
            if link_header:
                links = link_header.split(', ')
                for link in links:
                    if 'rel="next"' in link:
                        next_link = link[link.index('<') + 1:link.index('>')]
                        break
            url = next_link

        return events