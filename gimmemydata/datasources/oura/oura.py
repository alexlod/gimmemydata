import requests
import os
import psycopg2
from gimmemydata.config import Config
from gimmemydata.datasources.oura.client import OuraClientV2
import datetime





endpoints = ['daily_activity','daily_sleep','sleep','workout','daily_readiness']

url = 'https://api.ouraring.com/v2/usercollection/daily_activity' 
url = 'https://api.ouraring.com/v2/usercollection/daily_sleep' 
url = 'https://api.ouraring.com/v2/usercollection/sleep' 
url = 'https://api.ouraring.com/v2/usercollection/workout' 
url = 'https://api.ouraring.com/v2/usercollection/daily_readiness' 

OURA_PERSONAL_ACCESS_TOKEN = Config().get_param('OURA_PERSONAL_ACCESS_TOKEN')
client = OuraClientV2(personal_access_token=OURA_PERSONAL_ACCESS_TOKEN)

heartrate = client.heartrate(start_datetime='2021-11-01T00:00:00-08:00', end_datetime='2021-12-01T00:00:00-08:00')

print(heartrate)

# # HEART RATE:
# url = 'https://api.ouraring.com/v2/usercollection/heartrate' 
# params={ 
#     'start_datetime': '2021-11-01T00:00:00-08:00', 
#     'end_datetime': '2021-12-01T00:00:00-08:00' 
# }