'''
Author: arunkumar-js25
Script: Files Sync to external harddisk
Language: Python
'''

import os
import shutil
import logging
from datetime import datetime
import time

# Configure logging for better output control
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

files_ignore = []
files_format_ignore = [".ini"]
ExceptionFoldersList = []
ExceptionFilesList = [r"E:\Storage\Museum\2024\2024 09 08 My Engagement\Album 01\ENGAGEMENT.mpg"]

# Function to sync files from source to destination
def sync_folders(source_folder, destination_folder):
    alldirs = set()  # Using set for faster lookup
    allfiles = set()
    allfileslist = []
    files_to_merge = []
    dirs_to_remove = []
    files_to_remove = []
    ErrorList = []

    # Walk through source directory
    for srcroot, srcdirs, srcfiles in os.walk(source_folder):
        try:
            destroot = srcroot.replace(source_folder, destination_folder)
            alldirs.add(destroot)
            os.makedirs(destroot, exist_ok=True)

            for file in srcfiles:
                filename, fileextension = os.path.splitext(file)
                srcfile = os.path.join(srcroot, file)
                destfile = os.path.join(destroot, file)
                allfiles.add(destfile)

                try:
                    src_mtime = os.path.getmtime(srcfile)
                    src_file_size = os.path.getsize(srcfile)
                except OSError as e:
                    logging.error(f"Error getting file details for {srcfile}: {e}")
                    src_mtime = 0
                    src_file_size = 0

                src_last_modified_date = datetime.fromtimestamp(src_mtime)
                allfileslist.append([file, src_file_size, src_last_modified_date, srcfile, destfile])

                if file not in files_ignore and fileextension not in files_format_ignore:
                    if not os.path.exists(destfile):
                        files_to_merge.append([file, src_file_size, src_last_modified_date, srcfile, destfile, 'COPY'])
                    else:
                        try:
                            dest_mtime = os.path.getmtime(destfile)
                            dest_file_size = os.path.getsize(destfile)
                        except OSError as e:
                            logging.error(f"Error accessing destination file {destfile}: {e}")
                            dest_mtime = 0
                            dest_file_size = 0

                        dest_last_modified_date = datetime.fromtimestamp(dest_mtime)

                        if src_last_modified_date > dest_last_modified_date and src_file_size != dest_file_size:
                            files_to_merge.append([file, src_file_size, src_last_modified_date, srcfile, destfile, 'REPLACE'])
        except Exception as e:
            ErrorList.append([f"Error processing directory {srcroot}", str(e)])

    # Walk through destination directory and find extra files/folders
    for desroot, desdirs, desfiles in os.walk(destination_folder):
        if desroot not in alldirs and desroot not in ExceptionFoldersList:
            dirs_to_remove.append(desroot)

        for file in desfiles:
            desfile = os.path.join(desroot, file)
            if desfile not in allfiles and desfile not in ExceptionFilesList:
                files_to_remove.append(desfile)

    return files_to_merge, dirs_to_remove, files_to_remove, ErrorList

# Function to add new/modified files
def add_data(files_to_merge):
    logging.info('Choose an option:\n1. View All Files to Merge\n2. View New Files\n3. View Replace Files\n4. Proceed to Merge\n')
    while True:
        try:
            choice = int(input("YOUR CHOICE >> "))
        except ValueError:
            logging.error("Invalid input. Please enter a number.")
            continue

        if choice == -1:
            logging.info("Operation Cancelled!!")
            break

        if choice == 1:
            for name, size, lmd, srcfile, destfile, file_type in files_to_merge:
                logging.info(f"{name.ljust(50)} {str(size).ljust(10)} {str(lmd)}  {file_type.ljust(10)} {srcfile}")
        elif choice == 2:
            for name, size, lmd, srcfile, destfile, file_type in files_to_merge:
                if file_type == 'COPY':
                    logging.info(f"{name.ljust(50)} {str(size).ljust(10)} {str(lmd)}  {file_type.ljust(10)} {srcfile}")
        elif choice == 3:
            for name, size, lmd, srcfile, destfile, file_type in files_to_merge:
                if file_type == 'REPLACE':
                    logging.info(f"{name.ljust(50)} {str(size).ljust(10)} {str(lmd)}  {file_type.ljust(10)} {srcfile}")
        elif choice == 4:
            for name, size, lmd, srcfile, destfile, file_type in files_to_merge:
                try:
                    start_time = time.time()
                    shutil.copyfile(srcfile, destfile)
                    end_time = time.time()
                    logging.info(f"Copied {srcfile} to {destfile} in {end_time - start_time:.2f} seconds")
                except shutil.Error as e:
                    ErrorList.append(["Copy interrupted", srcfile, str(e)])
            logging.info("Transfer Completed!!")
            break
        else:
            logging.error("Please Enter a Valid Choice Again")

    if ErrorList:
        logging.warning("Warnings & Errors Encountered: ")
        for error in ErrorList:
            logging.warning(error)

# Function to remove extra files/folders
def remove_data(dirs_to_remove, files_to_remove):
    logging.info('Choose an option:\n1. View Extra Files\n2. View Extra Dirs\n3. Proceed to Erase\n')
    while True:
        try:
            choice = int(input("YOUR CHOICE >> "))
        except ValueError:
            logging.error("Invalid input. Please enter a number.")
            continue

        if choice == -1:
            logging.info("Operation Cancelled!!")
            break

        if choice == 1:
            for desfile in files_to_remove:
                logging.info(desfile)
        elif choice == 2:
            for desdir in dirs_to_remove:
                logging.info(desdir)
        elif choice == 3:
            for desfile in files_to_remove:
                try:
                    os.remove(desfile)
                    logging.info(f"Removed file: {desfile}")
                except OSError as e:
                    logging.error(f"Failed to remove {desfile}: {e}")

            for desdir in dirs_to_remove:
                try:
                    os.rmdir(desdir)
                    logging.info(f"Removed directory: {desdir}")
                except OSError as e:
                    logging.error(f"Failed to remove directory {desdir}: {e}")

            logging.info("Cleanup Completed!!")
            break
        else:
            logging.error("Please Enter a Valid Choice Again")

if __name__ == "__main__":
    source_folder = r"D:\Arun Kumar"
    destination_folder = r"E:\Storage\Arun Kumar"

    files_to_merge, dirs_to_remove, files_to_remove, ErrorList = sync_folders(source_folder, destination_folder)

    logging.info(f'Total Files in Source Folder: {len(files_to_merge)}')
    logging.info(f'Extra Folders in Destination to Erase: {len(dirs_to_remove)}')
    logging.info(f'Extra Files in Destination to Erase: {len(files_to_remove)}')

    try:
        Option = int(input("\n Select Options Available: \n1. Add Files to Destination\n2. Erase Extra Files in Destination\n\n"))
        if Option == 1:
            add_data(files_to_merge)
        elif Option == 2:
            remove_data(dirs_to_remove, files_to_remove)
        else:
            logging.error("Invalid Option! Try Again.")
    except ValueError:
        logging.error("Invalid input. Please enter a number.")
