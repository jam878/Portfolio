from mp3_tagger import MP3File, VERSION_2
from titlecase import titlecase
import os
import time


untagged = []
successRate = {
    'Pass' : 0,
    'Fail' : 0
}


# Purpose: Get yes/no answers from user
# Input: N/A
# Output: True if 'Yes', False if 'No'
def binaryQuestion(question):
    answer = False
    while True:
        try:
            if question != '':
                print(question)
            userInput = str(input("\nIs this okay? (y/n) "))
        except ValueError as e:
            print("\nPlease enter either 'y' or 'n'")
            continue
        userInput.lower()
        if userInput == 'n':
            break
        elif userInput == 'y':
            answer = True
            break
        else:
            print("\nPlease enter either 'y' or 'n'")
            continue
    return answer


# Purpose: Print directories to tag
# Input: N/A
# Output: List of directories
def listDirectories():
    print("\nHere are the directories that will be altered:")
    dirList = []
    for dir in os.listdir('.'):
        if os.path.isdir(dir) and dir != 'venv' and dir != '.idea':
            dirList.append(dir)
            print(dir)
    answer = binaryQuestion('')
    if not answer:
        print("Exiting...")
        exit()
    return dirList


# Purpose:
    # Get list of files in the current folder
    # Delete non-audio files
    # Compile list of folders containing FLAC audio
# Input:
    # Folder to analyze
    # Root script path
    # Master list of folders containing FLAC audio
# Output:
    # List of files in folder
    # List of folders containing FLAC audio
def getFiles(folder, rootPath, flacList):
    newDir = os.path.join(rootPath, folder)
    os.chdir(newDir)
    trackList = []
    for file in os.listdir('.'):
        if os.path.isfile(file) and file.endswith('.mp3'):
            trackList.append(file)
        elif os.path.isfile(file) and file.endswith('.flac'):
            trackList.append(file)
            if folder not in flacList:
                flacList.append(folder)
        else:
            os.remove(file)
    return trackList, flacList


# Purpose: Allow user to fix genre tags for each album
# Input: Album name, album genre tag
# Output: Proper album genre tag
def getGenre(folder, tags):
    answer = binaryQuestion('\nThe genre for ' + folder + ' is: ' + tags['genre'])
    if answer:
        genre = tags['genre']
    else:
        genre = input("What would you like to tag " + folder + " as: ")
    return genre


# Purpose: Allow user to fix year tags for each album
# Input: Album name, album year tag
# Output: Proper album year tag
def getYear(folder, tags):
    answer = binaryQuestion('\nThe year tag for ' + folder + ' is: ' + tags['year'])
    if answer:
        year = tags['year']
    else:
        while True:
            try:
                year = int(input("What year was " + folder + " released in? "))
            except ValueError as e:
                print("Please enter an integer for the year tag\n")
                continue
            break
        year = str(year)
    return year


def getArtist(artist):
    tokens = artist.split()
    allCaps = []
    for word in tokens:
        if word == word.upper():
            allCaps.append(word)
    artist = titlecase(artist)
    return artist


# Purpose:
    # WIP
def trackTagger(tags, genre, year, folder, mp3):
    tags['track'] = tags['track'][0:tags['track'].find('/')]
    try:
        trackNumber = int(tags['track'])
    except ValueError as e:
        if folder not in untagged:
            untagged.append(folder)
        return True
    if trackNumber < 10:
        trackNumber = str('0' + str(trackNumber))
    else:
        trackNumber = str(trackNumber)
    mp3.genre = genre
    mp3.year = year
    artistName = getArtist(tags['artist'])
    mp3.artist = artistName
    mp3.save()
    return False


def main():
    print("Welcome to MusicTagger")
    # time.sleep(1)
    # Todo
    print("\nBefore using, please:")
    print("1. Read the User Guide")
    print("2. Back up your music folder\n")
    # time.sleep(2)
    # Todo
    print("PLEASE NOTE: ANY NON-AUDIO FILES WILL BE DELETED\n")
    # time.sleep(2)
    # Todo
    print("MP3 and FLAC files will be automatically tagged")
    print("Directories that cannot be tagged will be listed in 'Untagged.txt'")
    rootPath = os.path.dirname(os.path.realpath(__file__))
    flacList = []
    dirList = listDirectories()
    for folder in dirList:
        trackList, flacList = getFiles(folder, rootPath, flacList)
        if folder in flacList:
            continue
        trackList.sort()
        mp3 = MP3File(os.path.join(rootPath, folder, trackList[0]))
        mp3.set_version(VERSION_2)
        tags = mp3.get_tags()
        genre = getGenre(folder, tags)
        year = getYear(folder, tags)
        for track in trackList:
            mp3 = MP3File(os.path.join(rootPath, folder, track))
            mp3.set_version(VERSION_2)
            tags = mp3.get_tags()
            skipFolder = trackTagger(tags, genre, year, folder, mp3)
            if skipFolder:
                successRate['Fail'] += 1
                break
        mp3 = MP3File(os.path.join(rootPath, folder, trackList[0]))
        tags = mp3.get_tags()
        # os.rename(folder, tags)
        os.chdir("..")
        successRate['Pass'] += 1


main()

print("\nTagging finished")
print(successRate['Pass'], "folder(s) tagged")
if successRate['Fail'] != 0:
    print(successRate['Fail'], "folder(s) untagged, check 'Untagged.txt' for details")
