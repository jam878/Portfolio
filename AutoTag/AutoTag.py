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
    for dir  in os.listdir('.'):
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


# Purpose: Properly capitalized album and song titles
# Input: String to capitalize
# Output: Properly capitalized string
def fixCaps(string):
    if ' ' in string:
        tokens = string.split()
    else:
        tokens = string.split('_')
    allCaps = []
    for word in tokens:
        if word == word.upper() and len(word) > 1:
            allCaps.append(word)
    string = titlecase(string)
    tokens = string.split()
    for word in tokens:
        for capsString in allCaps:
            if capsString.lower() == word.lower():
                word = capsString
    string = ' '.join(tokens)
    return string


# Purpose: Locate 'Remastered' in a string and properly remove it
# Input: String to test
# Output: String without 'Remastered' sections
def remasteredRemover(string):
    tokens = string.split()
    lowerTokens = []
    for word in tokens:
        lowerTokens.append(word.lower())
    if 'remastered' in lowerTokens:
        if string.endswith(')'):
            string = string[:string.rfind('(')]
            string = string.rstrip()
            return string
        else:
            string = string[:string.rfind('-')]
            string = string.rstrip()
            return string
    else:
        return string


# Purpose: Properly tag and rename each track
# Input: MP3 file tags, user-entered tags, album folder and track name
# Output: True if track is properly tagged, False otherwise
def trackTagger(tags, genre, year, folder, mp3, track):
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
    artistName = fixCaps(tags['artist'])
    mp3.artist = artistName
    songName = fixCaps(tags['song'])
    songName = remasteredRemover(songName)
    mp3.song = songName
    album = fixCaps(tags['album'])
    album = remasteredRemover(album)
    mp3.album = album
    mp3.save()
    try:
        os.rename(track, trackNumber + ' - ' + songName + '.mp3')
    except ValueError as e:
        if folder not in untagged:
            untagged.append(folder)
        return True
    return False


# Purpose: Output untagged folders to a text file
# Input: N/A
# Output: 'Untagged.txt'
def printUntagged():
    if os.path.isfile('Untagged.txt'):
        os.remove('Untagged.txt')
    with open('Untagged.txt', 'a') as file:
        file.write("The following albums could not be tagged, please tag them manually:\n")
        for album in untagged:
            file.write(album + '\n')


def main():
    print("Welcome to AutoTag")
    time.sleep(1)
    print("\nBefore using, please back up your music folder")
    time.sleep(4)
    print("PLEASE NOTE: ANY NON-AUDIO FILES WILL BE DELETED\n")
    time.sleep(2)
    print("MP3 files will be automatically tagged")
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
            skipFolder = trackTagger(tags, genre, year, folder, mp3, track)
            if skipFolder:
                successRate['Fail'] += 1
                break
        trackList, flacList = getFiles(folder, rootPath, flacList)
        mp3 = MP3File(os.path.join(rootPath, folder, trackList[0]))
        mp3.set_version(VERSION_2)
        tags = mp3.get_tags()
        os.chdir("..")
        try:
            os.rename(folder, tags['artist'] + ' - ' + tags['album'])
        except ValueError as e:
            if folder not in untagged:
                untagged.append(folder)
                successRate['Fail'] += 1
                continue
        if folder not in untagged:
            successRate['Pass'] += 1
    printUntagged()


main()

print("\nTagging finished")
print(successRate['Pass'], "folder(s) tagged")
if successRate['Fail'] != 0:
    print(successRate['Fail'], "folder(s) untagged, check 'Untagged.txt' for details")
