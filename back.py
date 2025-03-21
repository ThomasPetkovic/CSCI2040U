    # Working copy of back-end logic

import csv
import os
import lyricsgenius

#read from initial database
def initial_read():

    list = []

    with open("test.csv", mode="r") as database:

        catalog=csv.DictReader(database)

        for item in catalog:
            print(item)
            list.append(item)

    return list

list = initial_read()

#function to save modified list variable to new csv file. can be replaced with append functionality later on if optimization required.
def rewrite_csv(list):
    with open("test.csv", mode="w", newline="") as database:
        fieldnames = ["name", "description", "id", "albumtitle", "genre", "releasedate"]  # Added new fields
        writer = csv.DictWriter(database, fieldnames=fieldnames)
        writer.writeheader()
        for item in list:
            writer.writerow(item)

rewrite_csv(list)

def find_lyrics(item):
    
    lyrics_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"song_lyrics")
    test_path = os.path.join(lyrics_dir,item['name'] + ".txt")

    if not os.path.exists(test_path):
        file = item['name'] + ".txt"
        file_path = os.path.join(lyrics_dir,file)
        print(file_path)
        genius = lyricsgenius.Genius('ogwCLyB6vLx_aWgYvR1ZOgVyGOMAd_KUPrGmUmc8K1PpgcsC17h3TQH7OZer4bzW')

        artist = item['description']; 
        artist = artist[3:]
        genius_artist = genius.search_artist(artist, max_songs=0, sort="title")
        song = genius_artist.song(item['name'])
            
        with open(file_path,"w") as lyrics:
            lyrics.write(song.lyrics)
        
        read_lyrics(file_path)
    
    elif os.path.exists(test_path):
        read_lyrics(test_path)

def read_lyrics(file_path):
    lyrics_list = []
    with open(file_path, "r") as lyrics:
        for line in lyrics:
            lyrics_list.append(line.strip())
    return lyrics_list
