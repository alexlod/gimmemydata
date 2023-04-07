
import datetime
import os


import requests
import os
import psycopg2
from gimmemydata.config import Config
from gimmemydata.datasources.oura.client import OuraClientV2
import datetime


endpoints = ['daily_activity','daily_sleep','sleep','workout','daily_readiness']


OURA_PERSONAL_ACCESS_TOKEN = Config().get_param('OURA_PERSONAL_ACCESS_TOKEN')


start_date = '2023-03-05'
end_date = '2023-03-20'


client = OuraClientV2(personal_access_token=OURA_PERSONAL_ACCESS_TOKEN)

sleep = client.daily_sleep(start_date=start_date, end_date=end_date)
print(sleep)
# of = Config().get_param('LOCAL_DATA_DIR') + '/oura/oura_sleep.txt'

# with open(of, "w", newline='', encoding="utf-8") as t:
#         for datapoint in sleep:
#             t.write(str(datapoint) + "\n")


