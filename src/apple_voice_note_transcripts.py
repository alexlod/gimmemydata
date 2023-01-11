import os
import shutil
from datetime import datetime
import json
import pwd
# import pyobjc
# from Foundation import NSFileManager, NSFileHFSCreatorCode, NSFileHFSTypeCode
from osxmetadata import *
import xattr
from pathlib import Path
import whisper

# The directory to watch for new files
def get_username():
    return pwd.getpwuid(os.getuid())[0]

u = get_username()
watch_dir = f'/Users/{u}/Library/Application Support/com.apple.voicememos/Recordings'

# The directory to copy new files to
target_dir = '/Users/sam/notes/sam-notes-master/08 - Voice Memo Transcripts'

# The file to store the list of processed files
processed_file_record = os.path.join(os.path.abspath(os.path.dirname(__name__)), "processed_files.json")

# Load the list of processed files from the JSON file
with open(processed_file_record, 'r') as f:
    processed_files = json.load(f)

def getWhisperTxt(wav_file, model="large") -> str:

    print(f'Beginning Whisper transcription from {wav_file}')
    model = whisper.load_model(model)
    w = model.transcribe(wav_file)    
    transcript_txt: str = w["text"]
    
    return transcript_txt

class MdFileUtil:

    def __init__(self, tags: str, title: str, target_path: str):
        self.tags = tags.replace(' ', '-').split(',')
        self.title = title
        self.target_dir = target_path
        self.out_file = self.get_md_file()
        self.add_tags = self.add_tags_and_title()
    
    def get_md_file(self):

        try:
            outfile_path = self.target_path
            md_file = open(outfile_path, 'w+', encoding="utf-8")
            md_file.close()
            print(f'Creating new markdown file at: {outfile_path}')
        
        except Exception as e:

            print(f"Error while creating new file: " + str(e))
        
        return outfile_path

    def add_tags_and_title(self):
        
        tag_list = self.tags
        
        obsidian_yaml_block = """---\ntags:"""

        for tag in tag_list:
            obsidian_yaml_block = obsidian_yaml_block + f"\n- {tag}"

        obsidian_yaml_block = obsidian_yaml_block + "\n---"
        
        with open(self.out_file, 'r+', encoding="utf-8") as md_file:
            existing_data = md_file.read()
            md_file.seek(0,0)
            md_file.write(obsidian_yaml_block)
            md_file.write("\n")
            md_file.write(f'# {self.title}')
            md_file.write("\n" + existing_data)

    def append_line(self, t):

        with open(self.out_file, 'a', encoding="utf-8") as md_file:
            md_file.write(t)
            md_file.write("\n")

def get_created_date(f):
    mac_date_added = xattr.getxattr(f, "com.apple.metadata:kMDItemDateAdded")
    dt = datetime.strptime(mac_date_added, "%Y-%m-%d %H:%M:%S %z")
    date = dt.date().strftime("%Y-%m-%d")
    return date


idx = 0

while idx < 2:

    # Iterate over the files in the watch directory
    for filename in os.listdir(watch_dir):
        filepath = os.path.join(watch_dir, filename)
        print(filepath)

        # Skip files that have already been processed
        if filename in processed_files:
            continue

        try:
            tags = "voicememo,transcription"
            title = Path(filepath).stem

            transcription_txt = getWhisperTxt(filepath)
            target_path = os.path.join(target_dir, title + '.md')
            md_file = MdFileUtil(tags, title, target_dir)
            
            md_file.append_line(transcription_txt)
            print(f'Saved Markdown file at location: {target_path}')
            
            # Add the file to the list of processed files
            processed_files.append(filename)
            idx += 1

        except Exception as e:
            print('Error while sending: ', + str(e))
            raise

# Save the updated list of processed files to the JSON file
with open(processed_file_record, 'w') as f:
    json.dump(processed_files, f)



        # # Get the file URL for the voice memo file
        # file_url = pyobjc.core.nsurl.NSURL.fileURLWithPath_(filepath)

        # # Get the file's metadata dictionary
        # metadata = file_url.resourceValuesForKeys_error_(None, None)[0]

        # # Print the metadata keys
        # print(metadata.keys())

        # # Print the title of the voice memo
        # print(metadata['kMDItemTitle'])


