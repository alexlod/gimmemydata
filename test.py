
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


start_date = '2022-10-01'
end_date = '2022-12-05'


client = OuraClientV2(personal_access_token=OURA_PERSONAL_ACCESS_TOKEN)

heartrate = client.heartrate(start_date=start_date, end_date=end_date)
print(heartrate)
of = Config().get_param('LOCAL_DATA_DIR') + '/oura/oura_heartrate.txt'

with open(of, "w", newline='', encoding="utf-8") as t:
        for datapoint in heartrate:
            t.write(str(datapoint) + "\n")


