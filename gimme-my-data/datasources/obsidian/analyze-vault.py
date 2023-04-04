#!/usr/bin/env python3

import os
import re
import datetime
from collections import defaultdict
import psycopg2
from gimmemydata import config

# Set the path to your Obsidian vault
vault_path = "/Users/sam/notes/sam-notes-master"

# Set up a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="yourhost.render.com",
    database="yourdatabase",
    user="yourusername",
    password="yourpassword"
)

# Define a regular expression pattern for matching YAML frontmatter
yaml_pattern = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)

# Define a dictionary to store the file counts and word counts
file_counts = defaultdict(int)
word_counts = defaultdict(int)

# Define a function to parse the YAML frontmatter and return the date, if present
def get_date_from_yaml(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()
    match = re.search(yaml_pattern, contents)
    if match:
        yaml_frontmatter = match.group(1)
        yaml_lines = yaml_frontmatter.split('\n')
        for line in yaml_lines:
            if line.startswith('date:'):
                date_string = line.split(':')[1].strip()
                return datetime.datetime.fromisoformat(date_string)
    return None

# Define a function to calculate the word count of a file
def get_word_count(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()
    words = contents.split()
    return len(words)

# Define a function to insert the data into the database
def insert_data(date, top_level_dir, second_level_dir, file_count, edit_count, word_count):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO obsidian_notes
            (date, top_level_dir, second_level_dir, file_count, edit_count, word_count)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (date, top_level_dir, second_level_dir, file_count, edit_count, word_count))
    conn.commit()

# Iterate over the files in the Obsidian vault and populate the file_counts and word_counts dictionaries
for root, dirs, files in os.walk(vault_path):
    for file in files:
        file_path = os.path.join(root, file)
        if file.endswith('.md'):
            # Get the file creation time
            ctime = os.path.getctime(file_path)
            date = datetime.datetime.fromtimestamp(ctime).date()
            # Check if there is YAML frontmatter with a date field
            yaml_date = get_date_from_yaml(file_path)
            if yaml_date is not None:
                date = yaml_date.date()
            # Update the file and word counts for the date
            file_counts[date] += 1
            word_counts[date] += get_word_count(file_path)

# Iterate over the dates and insert the data into the database
start_date = min(file_counts.keys())
end_date = datetime.date.today()
current_date = start_date
while current_date <= end_date:
    top_level_dir = None
    second_level_dir = None
    file_count = file_counts[current_date]
    edit_count = 0
    word_count = word_counts[current_date]
    # Insert the data into the database
    insert_data(current_date, top_level_dir, second_level_dir, file_count, edit_count, word_count)
    current_date += datetime.timedelta(days=1)

# Close the database connection
conn.close()
