#!python3.5

#check the request module compatibility before running the code. the code works but has a weird compatibility issue with certain request module versions


import argparse
import sys
import dropbox
from sentiment import *
import os

from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Access token
TOKEN =jd('localInfo.json')['dropboxaccesstoken']
dbx = dropbox.Dropbox(TOKEN)
#LOCALFILE = relativepath(sys.argv[1])
# must create /autobackup directory in dropbox before.
#BACKUPPATH = '/autobackup/'+sys.argv[1]# Keep the forward slash before destination filename


# Uploads contents of LOCALFILE to Dropbox
def relativebackup(localfile):
    filetobackup = relativepath(localfile)
    backuppath = '/autobackup/'+localfile
    with open(filetobackup, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + filetobackup + " to Dropbox as " + backuppath + "...")
        try:
            dbx.files_upload(f.read(), backuppath, mode=WriteMode('overwrite'))
            print("done")
        except ApiError as err:
            # This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
            print('error')

def absolutebackup(localfile):
    filetobackup = localfile
    backuppath = '/autobackup/'+localfile
    with open(filetobackup, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + filetobackup + " to Dropbox as " + backuppath + "...")
        try:
            dbx.files_upload(f.read(), backuppath, mode=WriteMode('overwrite'))
            print("done")
        except ApiError as err:
            # This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
            print('error')
        


# Adding few functions to check file details
def checkFileDetails():
    print("Checking file details")

    for entry in dbx.files_list_folder('').entries:
        print("File list is : ")
        print(entry.name)


# Run this script independently
if __name__ == '__main__':
    # Check for an access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. Open up backup-and-restore-example.py in a text editor and paste in your token in line 14.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")


    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit(
            "ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    try:
        checkFileDetails()
    except:
        sys.exit("Error while checking file details")

    print("Creating backup...")
    # Create a backup of the current settings file
    relativebackup(sys.argv[1])

    #print("Done!")
