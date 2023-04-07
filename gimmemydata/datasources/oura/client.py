import json
import datetime
from . import exceptions
from .auth import OAuthRequestHandler, PersonalRequestHandler

class OuraClientV2:

    API_ENDPOINT = "https://api.ouraring.com/v2/usercollection"

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        access_token=None,
        refresh_token=None,
        refresh_callback=None,
        personal_access_token=None,
    ):
        """
        :param client_id: The client id - identifies your application.
        :type client_id: str

        :param client_secret: The client secret. Required for auto refresh.
        :type client_secret: str

        :param access_token: Access token.
        :type access_token: str

        :param refresh_token: Use this to renew tokens when they expire
        :type refresh_token: str

        :param refresh_callback: Callback to handle token response
        :type refresh_callback: callable

        :param personal_access_token: Token used for accessing personal data
        :type personal_access_token: str
        """

        if client_id is not None:
            self._auth_handler = OAuthRequestHandler(
                client_id, client_secret, access_token, refresh_token, refresh_callback
            )

        if personal_access_token is not None:
            self._auth_handler = PersonalRequestHandler(personal_access_token)

    def daily_activity(self, start_date=None, end_date=None, next_token=None):
        # end_date default to current UTC date
        # start_date default to end_date - 1 day
        return self._get_summary(start_date, end_date, next_token, "daily_activity")

    def heartrate(self, start_date=None, end_date=None, next_token=None):
        print(f"Making API request for heart rate data from range: {start_date} to {end_date}")

        # Convert the start and end dates to datetime objects
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        # Calculate the number of days between the start and end dates
        num_days = (end_date - start_date).days + 1

        # If the range is less than or equal to 30 days, make a single API call
        if num_days <= 30:
            # Make the API call with the original start and end dates
            start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
            end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S')
            return self._get_summary(start_str, end_str, next_token, "heartrate")
            
        # If the range is greater than 30 days, break it down into 30-day chunks
        data = []
        curr_start_date = start_date
        curr_end_date = start_date + datetime.timedelta(days=29)
        while curr_end_date <= end_date:
            # Make the API call with the current start and end dates
            response = self._get_summary(curr_start_date.strftime('%Y-%m-%dT%H:%M:%S'), curr_end_date.strftime('%Y-%m-%dT%H:%M:%S'), next_token, "heartrate")
            for item in response['data']:
                data.append(item)
            # data.append(response['data'])

            # Move the start and end dates to the next 30-day chunk
            curr_start_date = curr_end_date + datetime.timedelta(days=1)
            curr_end_date = curr_start_date + datetime.timedelta(days=29)

        # If there's a remainder chunk, make an API call with the remaining dates
        if curr_start_date <= end_date:
            response = self._get_summary(curr_start_date.strftime('%Y-%m-%dT%H:%M:%S'), curr_end_date.strftime('%Y-%m-%dT%H:%M:%S'), next_token, "heartrate")
            for item in response['data']:
                data.append(item)
            # data.append(response['data'])

        # Concatenate the data from all the API calls and return it
        return data


    def daily_readiness(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "daily_readiness")
    
    def daily_sleep(self, start_date=None, end_date=None, next_token=None):
        # Convert the start and end dates to datetime objects
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        return self._get_summary(start_str, end_str, next_token, "daily_sleep")

    def personal_info(self):
        url = f"{self.API_ENDPOINT}/personal_info"
        return self._make_request(url)

    def session(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "session")

    def tags(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "tag")

    def workouts(self, start_date=None, end_date=None, next_token=None):
        return self._get_summary(start_date, end_date, next_token, "workout")

    def _get_summary(self, start_date, end_date, next_token, summary_type):
        url = self._build_summary_url(start_date, end_date, next_token, summary_type)
        return self._make_request(url)

    def _make_request(self, url):
        response = self._auth_handler.make_request_v2(url)
        print(response)
        exceptions.detect_and_raise_error(response)
        payload = json.loads(response.content.decode("utf8"))
        return payload

    def _build_summary_url(self, start_date, end_date, next_token, summary_type):
        url = f"{self.API_ENDPOINT}/{summary_type}"
        params = {}
        if start_date is not None:
            if not isinstance(start_date, str):
                raise TypeError("start date must be of type str")
            params["start_datetime"] = start_date

        if end_date is not None:
            if not isinstance(end_date, str):
                raise TypeError("end date must be of type str")
            params["end_datetime"] = end_date

        if next_token is not None:
            params["next_token"] = next_token

        qs = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{url}?{qs}" if qs != "" else url
        return url
