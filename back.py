import csv
import os
import lyricsgenius             #Library for fetching songs from Genius

#read and print song list from initial csv database
def initial_read():

    list = []               #storing csv rows as dictionaries

    with open("test.csv", mode="r") as database:

        catalog=csv.DictReader(database)                #using dictreader to print the dictionaries

        for item in catalog:
            print(item)
            list.append(item)

    return list

list = initial_read()               #Load initial data from csv 

#function to save modified list variable to new csv file.
def rewrite_csv(list):
    with open("test.csv", mode="w", newline="") as database:
        fieldnames = ["name", "description", "id", "albumtitle", "genre", "releasedate"]  # Added new fields
        writer = csv.DictWriter(database, fieldnames=fieldnames)
        writer.writeheader()
        for item in list:
            writer.writerow(item)

rewrite_csv(list)               #Update the csv file with the current list of songs


#Fetchs song details from Genius library. Extracts artist name and description
def get_song(item):
        genius = lyricsgenius.Genius('26r3qCegkDDdjAs4Fv1aZNXyo1ildgMvLDfNkCsd83AkIdMgDF-ep6BE66lVHdge')

        artist = item['description']; 
        artist = artist[3:]
        genius_artist = genius.search_artist(artist, max_songs=0, sort="title")
        song = genius_artist.song(item['name'])

        return song


#Fetches and stores songs lyrics into a .txt file if the don't already exist
def get_lyrics(item):
    lyrics_list = []

    lyrics_dir = os.path.join(os.getcwd(),"song_lyrics")                #Create a directory to save a song's lyrics if the directory doesn't already exist.
    if not os.path.exists(lyrics_dir):
        os.makedirs(lyrics_dir)

    test_path = os.path.join(lyrics_dir,item['name'] + ".txt")

    if not os.path.exists(test_path):
        song = get_song(item)               #Use Genius's API to fetch song lyrics
        file = (item['name'] + ".txt")
        file_path = os.path.join(lyrics_dir,file)
        
        #Save the song lyrics into a .tx file
        with open(file_path,"w",errors='replace') as lyrics:
            lyrics.write(song.lyrics)
        
        read_lyrics(lyrics_list, file_path)
    
    elif os.path.exists(test_path):
        read_lyrics(lyrics_list,test_path)
    
    return lyrics_list

#Read lyrics from a given .txt file. 
def read_lyrics(lyrics_list, file_path):
    read = False

    with open(file_path, "r") as lyrics:
        for line in lyrics:
            if "[Intro]" in line:               #Strips the Intro line to save only songs.
                read = True
                lyrics_list.append("[Intro]")
                continue
            if read:
                lyrics_list.append(line.strip())

