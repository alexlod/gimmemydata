
import os
from manage.config import Config
from datasources.oura.client import OuraClientV2
import datetime
import json
import requests 


endpoints = ['daily_activity','daily_sleep','sleep','workout','daily_readiness']
OURA_PERSONAL_ACCESS_TOKEN = Config().get_param('OURA_PERSONAL_ACCESS_TOKEN')

start_date = '2022-03-01'
end_date = '2022-03-20'


client = OuraClientV2(personal_access_token=OURA_PERSONAL_ACCESS_TOKEN)

sleep = client.get_data_for_range(start_date=start_date, end_date=end_date, endpoint='sleep')
# print(json.loads(sleep).encode('utf-8'))
for i in sleep['data']:
    print(i['day'])
# sleep = client.heartrate(start_date=start_date, end_date=end_date)
# print(sleep)



# url = 'https://api.ouraring.com/v2/usercollection/heartrate' 
# params={ 
#     'start_datetime': start_date, 
#     'end_datetime': end_date 
# }
# headers = { 
#   'Authorization': f'Bearer {OURA_PERSONAL_ACCESS_TOKEN}', 
# }
# response = requests.request('GET', url, headers=headers, params=params) 
# print(response.text)