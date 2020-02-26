import sys
import json
import os

#Aaron Fye
#Feb 26 2020
#A program to take a file system, take the names then open a JSON file in each folder, then convert that json to SQL statements.

def getListOfFiles(dirName):
    # Taken from online somewhere.

    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

def getTitles():
    #Make a new file for use a but later
    sys.stdout = open('Names.txt', 'wt')

    #This is where the folders are.
    dirName = 'C:\\Users\\aaron\\PycharmProjects\\autoDB\\manga\\'

    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(dirName)
    index = 0

    # Print the files to Names.txt
    for elem in listOfFiles:
        # iterate the index
        index = index + 1
        # for some reason, the files are listed twice, so let's only take one of them.
        if index % 2 == 0:
            continue
        else:
            # split up the paths by the \ character
            data = elem.split("\\")

            # write the names of each folder down. (It is the 7th element in the file path.)
            print(data[6])

def makeSQL():

    # Make a file to store the sql statements. Not needed if I could figure out how to use sql in python. lol
    sys.stdout = open('database.sql', 'wt', encoding="utf_8")

    # Open the file with all the names we just wrote down, but in read mode.
    manga = open("Names.txt", "r")

    # Set up name
    name = ""

    # Set up an ID system.
    id = 0

    #Number of lines var
    mL = 0

    #Loops for lines in the file.
    for lines in manga:

        #add one to the amount of lines.
        mL = mL + 1

    #Close it, because that makes it work. lol
    manga.close()

    # Open it back up!
    manga = open("Names.txt", "r")

    #Loop fo the number of files you need.
    for x in range(0, mL):
            #Get the name of the manga.
            name = manga.readline()

            #Add 1 to the ID.
            id = id + 1

            #Truncate the name, other wise it was looking for \n at the end as well.
            name = name[0:-1]

            #Open the file it was looking for.
            fo = open('C:\\Users\\aaron\PycharmProjects\\autoDB\\manga\\' + name + '\\index.json', 'r', encoding="utf_8", errors="ignore")

            #Get the data from it.
            data = fo.read()

            #Read the JSON
            data2 = json.loads(data)

            #Close it
            fo.close()

            #Turn the int to a string, for concat purposes.
            mID = str(id)

            #IDK why I did these. I think testing? lol.
            #Set up and fill each variable from the JSON file.
            title = ""
            title = data2["name"]

            author = ""
            author = data2["author"]

            coll = ""
            coll = data2["collection"]

            date = ""
            date = data2["date"]

            desc = ""
            desc = data2["desc"]

            group = ""
            group = data2["group"]

            #This one is interesting. Since the tags were a list of strings, we take them and moosh them together.
            tags = ""
            tags = ",".join(data2["tags"])


            #Sometimes the group, collection, and/or description were null, so we needed to filter them out.
            #Then, we print a formed SQL statement into the file.
            if type(group) != type(author) and type(coll) != type(author) and type(desc) != type(author):
                print("INSERT INTO manga (mID, mAuthor, mCollection, mDate, mDesc, mGroup, mName, mTags) VALUES (" + mID + ", \"" + author + "\", \"" + "Unknown" + "\", \"" + date + "\", \"" + "Unknown" + "\", \"" + "Unknown" + "\", \"" + title + "\", \"" + tags + "\");")
            if type(group) != type(author) and type(coll) != type(author) and type(desc) == type(author):
                print("INSERT INTO manga (mID, mAuthor, mCollection, mDate, mDesc, mGroup, mName, mTags) VALUES (" + mID + ", \"" + author + "\", \"" + "Unknown" + "\", \"" + date + "\", \"" + desc + "\", \"" + "Unknown" + "\", \"" + title + "\", \"" + tags + "\");")
            if type(group) != type(author) and type(coll) == type(author) and type(desc) != type(author):
                print("INSERT INTO manga (mID, mAuthor, mCollection, mDate, mDesc, mGroup, mName, mTags) VALUES (" + mID + ", \"" + author + "\", \"" + coll + "\", \"" + date + "\", \"" + "Unknown" + "\", \"" + "Unknown" + "\", \"" + title + "\", \"" + tags + "\");")
            if type(group) != type(author) and type(coll) == type(author) and type(desc) == type(author):
                print("INSERT INTO manga (mID, mAuthor, mCollection, mDate, mDesc, mGroup, mName, mTags) VALUES (" + mID + ", \"" + author + "\", \"" + coll + "\", \"" + date + "\", \"" + desc + "\", \"" + "Unknown" + "\", \"" + title + "\", \"" + tags + "\");")
            if type(group) == type(author) and type(coll) != type(author) and type(desc) != type(author):
                print("INSERT INTO manga (mID, mAuthor, mCollection, mDate, mDesc, mGroup, mName, mTags) VALUES (" + mID + ", \"" + author + "\", \"" + "Unknown" + "\", \"" + date + "\", \"" + "Unknown" + "\", \"" + group + "\", \"" + title + "\", \"" + tags + "\");")
            if type(group) == type(author) and type(coll) != type(author) and type(desc) == type(author):
                print("INSERT INTO manga (mID, mAuthor, mCollection, mDate, mDesc, mGroup, mName, mTags) VALUES (" + mID + ", \"" + author + "\", \"" + "Unknown" + "\", \"" + date + "\", \"" + desc + "\", \"" + group + "\", \"" + title + "\", \"" + tags + "\");")
            if type(group) == type(author) and type(coll) == type(author) and type(desc) != type(author):
                print("INSERT INTO manga (mID, mAuthor, mCollection, mDate, mDesc, mGroup, mName, mTags) VALUES (" + mID + ", \"" + author + "\", \"" + coll + "\", \"" + date + "\", \"" + "Unknown" + "\", \"" + group + "\", \"" + title + "\", \"" + tags + "\");")
            if type(group) == type(author) and type(coll) == type(author) and type(desc) == type(author):
                print("INSERT INTO manga (mID, mAuthor, mCollection, mDate, mDesc, mGroup, mName, mTags) VALUES (" + mID + ", \"" + author + "\", \"" + coll + "\", \"" + date + "\", \"" + desc + "\", \"" + group + "\", \"" + title + "\", \"" + tags + "\");")

    #Close the files.
    manga.close()

def main():

    #Get the title.
    getTitles()

    #Turn them into SQL
    makeSQL()


if __name__ == '__main__':
    main()