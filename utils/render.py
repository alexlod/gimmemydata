#!/usr/bin/env python3

import psycopg2
from manage.config import Config


class DBClient():

    def __init__(self):
        self.render_host = Config().get_param('RENDER_HOST_NAME')
        self.render_db_name = Config().get_param('RENDER_DB_NAME')
        self.render_db_user = Config().get_param('RENDER_DB_USERNAME')
        self.render_db_password = Config().get_param('RENDER_DB_PASSWORD')
        self.connection = self.connect()

    def connect(self):
        # Set up a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=self.render_host,
            port=5432,
            database=self.render_db_name,
            user=self.render_db_user,
            password=self.render_db_password
        )

        return conn

    # Define a function to insert the data into the database
    def insert_data(self, sql, data):
        with self.connection.cursor() as cur:
            cur.execute(sql, data)
        self.connection.commit()

    def insert_task_log(self, task_name, timestamp, status):
        try:
            query = "INSERT INTO gimmemydata_task_logs (task_name, timestamp, status) VALUES (%s, %s, %s)"
            with self.connection.cursor() as cur:
                cur.execute(query, (task_name, timestamp, status))
            self.connection.commit()
            print("Task log inserted successfully.")
        except Exception as e:
            print(f"Error while inserting task log: {e}")