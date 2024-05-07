import os
import re
import glob
from pydub import AudioSegment
from pydub.playback import play
import time


# Set variables
FILE_PATH = os.path.join('home', 'johan', 'code', 'mazu', 'mazu-webapp', 'vocoder', 'syn_files')
playlist = []
last_played = 0

while True:
    # Read number of last audio file played from text file
    try:
        with open("last.txt", "r") as file:
            # Iterate through the file line by line
            for line in file:
                # Strip any leading or trailing whitespace
                first_line = line.strip()
                break  # Stop after reading the first line
        last_played = int(first_line)
    except:
        print("No file found.")


    # Helper functions 

    # Play a soundfile
    def play_file(number):
        print(f"Playing file {number}...\n")
        song = AudioSegment.from_wav(f"/{FILE_PATH}/{number}_synthesized.wav")
        play(song)

    # Extract number from filename
    def extract_number(file):
        base_filename = os.path.basename(file)
        if "_synthesized" in base_filename:
            number = int(base_filename.split("_")[0])
        else:
            number = int(base_filename.split(".")[0])
        return number

    def sorter(item):
        # Extract the numeric part from the filename
        match = re.match(r'.*?(\d+).*?', os.path.basename(item))
        if match:
            return int(match.group(1))
        return float('inf')  # Return infinity for non-numeric filenames


    # Acquire and play previlously unplayed files

    # Acquire all current filepaths from vocoder output
    files = glob.glob(f"/{FILE_PATH}/*_synthesized.wav")

    # Sort the files based on the extracted numeric value
    files.sort(key=sorter)

    # Step through found files, add new ones to the playlist
    for file in files:
        # Add higher filenumbers to the playlist
        num = extract_number(file)
        playlist.append(num)

    # Play files from playlist if they are not played before
    for number in playlist:
        print(f"\nPlaylist number: {number}")
        print(f"Last played: {last_played}")
        if number > last_played:
            last_played = number
            play_file(number)
            # Save the last number of the file that was played
            with open("last.txt", "w") as file:
                file.write(str(last_played))
        else:
            print(f"File number {number} is already played")

    time.sleep(1)
