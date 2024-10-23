'''
Author: arunkumar-js25
Script: Files Sync to external harddisk
Language: Python
'''

import filecmp
import os
from datetime import datetime
import shutil

files_ignore = []
files_format_ignore = [".ini"]
alldirs = []
allfiles = []
allfileslist = []
mergefileslist = []
removedirs = []
removefiles = []
ErrorList = []

ExceptionFoldersList=[]
ExceptionFilesList=[r"E:\Storage\Museum\2024\2024 09 08 My Engagement\Album 01\ENGAGEMENT.mpg"]

def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))

    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

def ReadSrc(source_folder,destination_folder):
    for (srcroot, srcdirs, srcfiles) in os.walk(source_folder):
        try:
            testfiles = srcfiles
        except:
            ErrorList.append(["FileName has Invalid Character",srcroot])

        # Create Missing Directories
        destroot = srcroot.replace(source_folder,destination_folder)
        alldirs.append(destroot)
        if ( os.path.isdir(destroot) == False ):
            os.mkdir(destroot)

        for file in srcfiles:
            filename,fileextension = os.path.splitext(file)
            srcfile = os.path.join(srcroot, file)
            destfile = srcfile.replace(source_folder, destination_folder)
            allfiles.append(destfile)

            # Fetching SOURCE File Details
            try:
                src_mtime = os.path.getmtime(srcfile)
            except OSError:
                src_mtime = 0

            try:
                src_file_size = os.path.getsize(srcfile)
            except:
                src_file_size = 0

            src_last_modified_date = datetime.fromtimestamp(src_mtime)
            allfileslist.append([file, src_file_size, src_last_modified_date, srcfile, destfile])

            if (file not in files_ignore
                    and filename not in files_ignore
                    and fileextension not in files_format_ignore
                ):

                if( os.path.isfile(destfile) == False ):
                    #shutil.copyfile(srcfile,destfile)
                    mergefileslist.append([file, src_file_size, src_last_modified_date , srcfile, destfile, 'COPY'])
                else:
                    # Fetching DESTINATION File Details
                    try:
                        dest_mtime = os.path.getmtime(destfile)
                    except OSError:
                        dest_mtime = 0
                    dest_last_modified_date = datetime.fromtimestamp(dest_mtime)
                    dest_file_size = os.path.getsize(destfile)

                    #print(dest_last_modified_date,src_last_modified_date,src_file_size,dest_file_size)
                    if ( src_last_modified_date > dest_last_modified_date and src_file_size != dest_file_size):
                        #shutil.copyfile(srcfile, destfile)
                        mergefileslist.append([file, src_file_size, src_last_modified_date , srcfile, destfile , 'REPLACE'])

def ReadDes(destination_folder):
    for (desroot, desdirs, desfiles) in os.walk(destination_folder):
        if desroot not in alldirs and desroot not in ExceptionFoldersList:
            # print(desroot)
            removedirs.append(desroot)

        for file in desfiles:
            desfile = os.path.join(desroot, file)
            if desfile not in allfiles and desfile not in ExceptionFilesList:
                #print(desfile)
                removefiles.append(desfile)

def RemoveData():
    print(
        'Choose the below Option: \n 1.View All Extra Files \n 2.View All Extra Dirs \n 3.Proceed to Erase \n')
    while (True):
        choice = int(input("YOUR CHOICE >> "))
        if choice == -1:
            print("Operation Cancelled!!")
            break
        if choice == 1:
            for desfile in removefiles:
                print(desfile)
        elif choice ==2:
            for desdir in removedirs:
                print(desdir)
        elif choice ==3:
            for desfile in removefiles:
                os.remove(desfile)

            for desdir in removedirs:
                os.rmdir(desdir)

            print("Sync Completed!!")
            break
        else:
            print("Please Enter Valid Choice Again")

def AddData():
    print(
        'Choose the below Option: \n 1.View All Files to Merge\n 2.View New files \n 3.View Replace files\n 4.Proceed\n')
    while (True):
        choice = int(input("YOUR CHOICE >> "))
        if choice == -1:
            print("Operation Cancelled!!")
            break
        if choice == 1:
            for name, size, lmd, srcfile, destfile, type in mergefileslist:
                print(name.ljust(50) + str(size).ljust(10) + str(lmd) + "  " + type.ljust(10) + srcfile)
        elif choice == 2:
            for name, size, lmd, srcfile, destfile, type in mergefileslist:
                if type == 'COPY':
                    print(name.ljust(50) + str(size).ljust(10) + str(lmd) + "  " + type.ljust(10) + srcfile)
        elif choice == 3:
            for name, size, lmd, srcfile, destfile, type in mergefileslist:
                if type == 'REPLACE':
                    print(name.ljust(50) + str(size).ljust(10) + str(lmd) + "  " + type.ljust(10) + srcfile)
        elif choice == 4:
            for name, size, lmd, srcfile, destfile, type in mergefileslist:
                try:
                    shutil.copyfile(srcfile, destfile)
                except:
                    ErrorList.append(["Copy Interrupted", " file: " + name, "location: " + destfile])
            print("Transfer Completed!!")
            break
        else:
            print("Please Enter Valid Choice Again")

    if len(ErrorList) > 0:
        print("Warnings & Errors Faced: ")
        for error in ErrorList:
            print(error)


if __name__ == "__main__":
    source_folder = r"D:\Arun Kumar"
    destination_folder = r"E:\Storage\Arun Kumar"

    #source_folder = r"D:\\SourceCodes\\"
    #destination_folder = r"Z:\\SourceCodes\\"

    ReadSrc(source_folder, destination_folder)
    ReadDes(destination_folder)

    print('Total Files in Source Folder: ', len(allfileslist))
    print('Files Pending to Merge: ', len(mergefileslist))

    print('Extra Folders in Destination to Erase: ', len(removedirs))
    print('Extra Files in Destination to Erase: ', len(removefiles))

    Option = int(input("\n Select Options Available: \n 1. Add Files to Destination \n 2. Erase Extra Files in Destination \n\n"))
    if Option == 1:
        AddData()
    elif Option == 2:
        RemoveData()
    else:
        print("Try Again!!")

    #Compares the files present in both dir
    #dcmp = filecmp.dircmp(source_folder,destination_folder)
    #print_diff_files(dcmp)
