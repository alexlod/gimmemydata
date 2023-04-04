#!/usr/bin/env python3

import os
import re
import datetime
from collections import defaultdict
import psycopg2
from gimmemydata.config import Config


class AnalyzeVault():

    def __init__(self):
        self.vault_path = Config().get_param('OBSIDIAN_VAULT_DIR')
        self.render_host = Config().get_param('RENDER_HOST_NAME')
        self.render_db_name = Config().get_param('RENDER_DB_NAME')
        self.render_db_user = Config().get_param('RENDER_DB_USERNAME')
        self.render_db_password = Config().get_param('RENDER_DB_PASSWORD')
        self.yaml_pattern = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)

    # Define a function to parse the YAML frontmatter and return the date, if present
    def get_date_from_yaml(self, file_path):
        with open(file_path, 'r') as f:
            contents = f.read()
        match = re.search(self.yaml_pattern, contents)
        if match:
            yaml_frontmatter = match.group(1)
            yaml_lines = yaml_frontmatter.split('\n')
            for line in yaml_lines:
                if line.startswith('date:'):
                    date_string = line.split(':')[1].strip()
                    try:
                        return datetime.datetime.fromisoformat(date_string)
                    except ValueError as e:
                        print(f"Error in file {file_path}: {e}")
                        return None
        return None

    # Define a function to calculate the word count of a file
    def get_word_count(self, file_path):
        with open(file_path, 'r') as f:
            contents = f.read()
        words = contents.split()
        return len(words)

    def analyze_to_file(self):

        # Define a dictionary to store the file counts and word counts
        file_counts = defaultdict(int)
        word_counts = defaultdict(int)

        of = Config().get_param('LOCAL_DATA_DIR') + '/obsidian/obsidian_analytics.csv'

        with open(of, "w", encoding="utf-8") as t:

            # Iterate over the files in the Obsidian vault and populate the file_counts and word_counts dictionaries
            for root, dirs, files in os.walk(self.vault_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    print(file_path)
                    if file.endswith('.md'):
                        # Get the file creation time
                        ctime = os.path.getctime(file_path)
                        date = datetime.datetime.fromtimestamp(ctime).date()
                        # Check if there is YAML frontmatter with a date field
                        yaml_date = self.get_date_from_yaml(file_path)
                        if yaml_date is not None:
                            date = yaml_date.date()

                        # Update the file and word counts for the date
                        top_level_dir = None
                        second_level_dir = None
                        rel_path = os.path.relpath(
                            os.path.dirname(file_path), self.vault_path)
                        dirs = rel_path.split(os.sep)

                        if len(dirs) >= 1:
                            top_level_dir = dirs[0]
                            print(top_level_dir)
                        if len(dirs) >= 2:
                            second_level_dir = dirs[1]

                        file_counts[(date, top_level_dir,
                                     second_level_dir)] += 1
                        word_counts[(date, top_level_dir, second_level_dir)
                                    ] += self.get_word_count(file_path)

            print('got thru all files')
            # Iterate over the dates and insert the data into the file
            start_date = min(file_counts.keys())[0]
            end_date = datetime.date.today()
            current_date = start_date
            while current_date <= end_date:
                has_files = False
                for top_level_dir in set([k[1] for k in file_counts.keys()]):
                    for second_level_dir in set([k[2] for k in file_counts.keys() if k[1] == top_level_dir]):
                        file_count = file_counts[(
                            current_date, top_level_dir, second_level_dir)]
                        edit_count = 0
                        word_count = word_counts[(
                            current_date, top_level_dir, second_level_dir)]
                        if file_count > 0:
                            # Set the flag to True if there are any files for this date
                            has_files = True
                            # Insert the data into the file
                            t.write(
                                f'{current_date},{top_level_dir},{second_level_dir},{file_count},{edit_count},{word_count}\n')
                # If there are no files for this date, write a row with null/zero values
                if not has_files:
                    t.write(f'{current_date},,,0,0,0\n')
                current_date += datetime.timedelta(days=1)

        print(f'Saved Obsidian analytics to file at: {of}')

    def analyze_to_db(self):

        # Set up a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=self.render_host,
            port=5432,
            database=self.render_db_name,
            user=self.render_db_user,
            password=self.render_db_password
        )

        # Define a dictionary to store the file counts and word counts
        file_counts = defaultdict(int)
        word_counts = defaultdict(int)

        # Define a function to insert the data into the database
        def insert_data(date, top_level_dir, second_level_dir, file_count, edit_count, word_count):
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO obsidian_analytics
                    (date, top_level_dir, second_level_dir, file_count, edit_count, word_count)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (date, top_level_dir, second_level_dir, file_count, edit_count, word_count))
            conn.commit()

        # Iterate over the files in the Obsidian vault and populate the file_counts and word_counts dictionaries
        for root, dirs, files in os.walk(self.vault_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.md'):
                    # Get the file creation time
                    ctime = os.path.getctime(file_path)
                    date = datetime.datetime.fromtimestamp(ctime).date()
                    # Check if there is YAML frontmatter with a date field
                    yaml_date = self.get_date_from_yaml(file_path)
                    if yaml_date is not None:
                        date = yaml_date.date()

                    # Update the file and word counts for the date
                    top_level_dir = None
                    second_level_dir = None
                    rel_path = os.path.relpath(
                        os.path.dirname(file_path), self.vault_path)
                    dirs = rel_path.split(os.sep)

                    if len(dirs) >= 1:
                        top_level_dir = dirs[0]
                    if len(dirs) >= 2:
                        second_level_dir = dirs[1]

                    file_counts[(date, top_level_dir,
                                    second_level_dir)] += 1
                    word_counts[(date, top_level_dir, second_level_dir)
                                ] += self.get_word_count(file_path)

        # Iterate over the dates and insert the data into the file
        start_date = min(file_counts.keys())[0]
        end_date = datetime.date.today()
        current_date = start_date
        while current_date <= end_date:
            has_files = False
            for top_level_dir in set([k[1] for k in file_counts.keys()]):
                for second_level_dir in set([k[2] for k in file_counts.keys() if k[1] == top_level_dir]):
                    file_count = file_counts[(
                        current_date, top_level_dir, second_level_dir)]
                    edit_count = 0
                    word_count = word_counts[(
                        current_date, top_level_dir, second_level_dir)]
                    if file_count > 0:
                        # Set the flag to True if there are any files for this date
                        has_files = True
                        
                        # Insert the data into the database
                        insert_data(current_date, top_level_dir, second_level_dir, file_count, edit_count, word_count)
            
            # If there are no files for this date, write a row with null/zero values
            if not has_files:
                # Insert the data into the database
                insert_data(current_date, "", "", 0, 0, 0)        

            current_date += datetime.timedelta(days=1)

        # Close the database connection
        conn.close()