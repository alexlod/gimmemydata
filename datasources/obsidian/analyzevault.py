#!/usr/bin/env python3

import os
import re
import csv
import datetime
from collections import defaultdict
import psycopg2
from manage.config import Config


class AnalyzeVault():

    def __init__(self, vault_dir):
        self.vault_dir = vault_dir
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

    def truncate_path(self, vault_dir, file_path):
        # Remove trailing slashes from the base path and file path
        vault_dir = vault_dir.rstrip('/')
        vault_name = os.path.basename(vault_dir)
        file_path = file_path.rstrip('/')

        # Get the relative path of the file with respect to the base path
        rel_path = os.path.relpath(file_path, vault_dir)
        rel_dir = os.path.dirname(rel_path)

        # If the relative path is '.' or '..', return the full file path
        if rel_path == '.' or rel_path == '..':
            print('ding ding ding')
            return vault_name, file_path

        return vault_name, rel_dir

    # Define a function to calculate the word count of a file
    def get_word_count(self, file_path):
        with open(file_path, 'r') as f:
            contents = f.read()
        words = contents.split()
        return len(words)

    def analyze_vault(self):
        # Define a dictionary to store the file counts and word counts
        file_stats = defaultdict(int)

        # Iterate over the files in the Obsidian vault and populate the file_counts and word_counts dictionaries
        for root, dirs, files in os.walk(self.vault_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.md'):
                    # Get the file creation time
                    ctime = os.stat(file_path).st_birthtime
                    date = datetime.datetime.fromtimestamp(ctime).date()
                    # Check if there is YAML frontmatter with a date field
                    yaml_date = self.get_date_from_yaml(file_path)
                    if yaml_date is not None:
                        date = yaml_date.date()

                    vault_name, truncated_path = self.truncate_path(self.vault_dir, file_path)
                    word_cnt = self.get_word_count(file_path)

                    file_stats[(date, truncated_path, file, vault_name,
                                    word_cnt)] += 1
        
        # Create a list of all dates between the earliest and latest dates in the file_stats dictionary
        date_list = [entry[0] for entry in file_stats.keys()]
        min_date = min(file_stats.keys())[0]
        max_date = datetime.date.today()
        all_dates = [min_date + datetime.timedelta(days=x) for x in range((max_date - min_date).days + 1)]

        # Create a set of dates that have file entries
        file_dates = set(date_list)

        # create new dict with a row for each file and a row for each missing date
        stats_by_date = {}
        for entry in file_stats.keys():
            date, path, filename, vault_name, word_count = entry
            stats_by_date[(date, path, filename, vault_name, word_count)] = file_stats[(date, path, filename, vault_name, word_count)]
            for d in all_dates:
                if d not in file_dates:
                    stats_by_date[(d,'','','',0)] = 0

        return stats_by_date

    def analyze_to_file(self):

        stats = self.analyze_vault()

        of = Config().get_param('LOCAL_DATA_DIR') + '/obsidian/obsidian_analytics.csv'

        with open(of, "w", newline='', encoding="utf-8") as t:

            # Write the stats to a csv file
            writer = csv.writer(t)
            writer.writerow(['date', 'path', 'filename', 'vault_name', 'word_count', 'file_count'])
            for entry in stats.keys():
                date, path, filename, vault_name, word_count = entry
                count = stats[(date, path, filename, vault_name, word_count)]
                writer.writerow([date, path, filename, vault_name, word_count, count])

        print(f'Saved Obsidian analytics to file at: {of}')

    def analyze_to_db(self):
        """
            CREATE TABLE obsidian_analytics (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                directory TEXT,
                file_name TEXT,
                vault_name TEXT,
                word_count INT,
                file_count INT
            );
        """

        # Set up a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=self.render_host,
            port=5432,
            database=self.render_db_name,
            user=self.render_db_user,
            password=self.render_db_password
        )

        stats = self.analyze_vault()

        # Define a function to insert the data into the database
        def insert_data(date, file_path, file_name, vault_name, word_cnt, file_cnt):
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO obsidian_analytics
                    (date, directory, file_name, vault_name, word_count, file_count)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (date, file_path, file_name, vault_name, word_cnt, file_cnt))
            conn.commit()

        # Clear the table before inserting new data
        with conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE obsidian_analytics')
        conn.commit()

        for entry in stats.keys():
            date, file_path, file_name, vault_name, word_cnt = entry
            file_cnt = stats[(date, file_path, file_name, vault_name, word_cnt)]
            insert_data(date, file_path, file_name, vault_name, word_cnt, file_cnt)

        # Close the database connection
        conn.close()
        
        print(f'Finished saving Obsidian analytics to db: {self.render_db_name}')




# def runObsidianAnalyze():
    
#     vault_dir = Config().get_param('OBSIDIAN_VAULT_DIR')

#     av = AnalyzeVault(vault_dir)
#     av.analyze_to_db()


# def cli():

#     parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#     exclusive_group = parser.add_mutually_exclusive_group(required=False)
#     exclusive_group.add_argument('--configure', action='store_true', help="Configure the CLI and create or update config yaml file.")
#     parser.add_argument('--obsidian', action="store_true", help="Analyze Obsidian vault & return data.")
#     parser.add_argument('--debug', action="store_true", help="Enable debug mode.")
#     args = parser.parse_args().__dict__

#     if args.get('debug'):
#         enableDebugMode()

#     if args.get('configure'):
#         Config().configure()
#         sys.exit(1)
#     else:
#         Config().get_config()

#     if args.get('obsidian'):
#         runObsidianAnalyze()
#     else:
#         parser.print_help()