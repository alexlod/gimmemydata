import requests
from dotenv import load_dotenv
import os


load_dotenv()

OURA_TOKEN = os.getenv('OURA_ACCESS_TOKEN')

endpoints = ['daily_activity','daily_sleep','sleep','workout','daily_readiness']

url = 'https://api.ouraring.com/v2/usercollection/daily_activity' 
url = 'https://api.ouraring.com/v2/usercollection/daily_sleep' 
url = 'https://api.ouraring.com/v2/usercollection/sleep' 
url = 'https://api.ouraring.com/v2/usercollection/workout' 
url = 'https://api.ouraring.com/v2/usercollection/daily_readiness' 




params={ 
    'start_date': '2021-11-01', 
    'end_date': '2021-12-01' 
}
headers = { 
  'Authorization': f'Bearer {OURA_TOKEN}' 
}
response = requests.request('GET', url, headers=headers, params=params) 
print(response.text)


# # HEART RATE:
# url = 'https://api.ouraring.com/v2/usercollection/heartrate' 
# params={ 
#     'start_datetime': '2021-11-01T00:00:00-08:00', 
#     'end_datetime': '2021-12-01T00:00:00-08:00' 
# }