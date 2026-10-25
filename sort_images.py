import os
import shutil
import pathlib

from PIL import Image
#from PIL.ExifTags import TAGS
from typing import Any


# -------- Global Variables -----------------
images_suffixes = [".png", ".jpg", ".gif", ".PNG", ".JPG", ".jpeg", ".JPEG"]
movies_suffixes = [".MOV", ".mov"]

# -------- Functions / Methods -------------

def make_filename_from_datetime(date_time : Any, original_filename : str, suffix : str)-> tuple[Any, bool]:
    """
    Args:
        date_time (str) : 
        suffix : .JPG, etc, have to figure out this
    """
    if date_time == None:
        return original_filename, False

    date_time_rep1 = date_time.replace(":", "_")
    date_time_rep2 = date_time_rep1.replace(" ", "_")
    date_time_fname = f"{date_time_rep2}{suffix}"
    
    return date_time_fname, True

def get_suffix(input_string : str):

    suffix = (pathlib.Path(input_string)).suffix
    return suffix

def get_datetime_from_imagepath(image_fpath : str,  suffix : str)-> Any:
    """
    Args:
        image_fpath (str) :
    Returns:
        Any (string or None):
    """
    try:
        image = (Image.open(image_fpath))
        image_info = image.getexif()
        date_time = image_info.get(306)
        return date_time
    except Exception as e:
        print(e)
        return None

def get_subdirs(path : str)-> list[str]:
    """
    Args : 
        path (str) : path to start from 
    """
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return dirs

def get_fnames_from_path(path : str)-> list[str]:
    """
    Args : 
        path (str) : path to start from 
    """
    current_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return current_files


def get_all_subdirectories_with_files(path : str, all_paths : list[str], ignore_folders : list[str]):
    """
    Args:
        path (str) : 
        all_paths (list[str]) :
        ignore_folders (list[str]) :
    """

    if len(get_fnames_from_path(path)) > 0:
        all_paths.append(path)
    current_subdirs = get_subdirs(path)

    for ignore_entry in ignore_folders:
        if ignore_entry in current_subdirs:
            current_subdirs.remove(ignore_entry)

    for current_subdir in current_subdirs:
        new_path = os.path.join(path, current_subdir)
        get_all_subdirectories_with_files(new_path, all_paths, ignore_folders)


def check_if_filename_exist(path : str, fname : str)-> bool:
    existing_fnames = get_fnames_from_path(path)
    return (fname in existing_fnames)

def move_file(original_fpath : str, new_fpath : str):
    #check_if_filename_exist(original_fpath, new_fpath)
    shutil.move(original_fpath, new_fpath)


def initial_fname_update(new_file_name, suffix):
    updated_fname = f"{new_file_name.strip(suffix)}_1{suffix}"
    return updated_fname



def make_duplicate_fname(new_file_name, suffix, num_duplicates):
    updated_fname = f"{new_file_name.strip(suffix)}_{num_duplicates}{suffix}"
    return updated_fname
#                   "Pictures_With_Dates",
def most_of_the_logic(folder_to_check, new_file_name, current_fpath, current_suffix):
    if check_if_filename_exist("Pictures_Potential_Duplicates", new_file_name):
        criteria = True
        num_duplicates = 1
        fnames_potential_duplicates = os.listdir("Pictures_Potential_Duplicates")
        while(criteria):
            new_dupicate_fname = make_duplicate_fname(new_file_name, current_suffix, num_duplicates)
            if new_dupicate_fname in fnames_potential_duplicates:
                num_duplicates += 1
            else:
                criteria = False
        new_dupicate_fname = make_duplicate_fname(new_file_name, current_suffix, num_duplicates)
        move_file(current_fpath, os.path.join("Pictures_Potential_Duplicates",new_dupicate_fname))

    elif check_if_filename_exist(folder_to_check, new_file_name):
        move_file(os.path.join(folder_to_check, new_file_name), os.path.join("Pictures_Potential_Duplicates", new_file_name))
        file_name_init_duplicate = initial_fname_update(new_file_name, current_suffix)
        move_file(current_fpath, os.path.join("Pictures_Potential_Duplicates", file_name_init_duplicate))
    else:
        move_file(current_fpath, os.path.join(folder_to_check, new_file_name))


if __name__ == '__main__':
    print(__name__)

    # Make directories to put all the images in
    dirs_to_make = ["Pictures_With_Dates", "Pictures_Potential_Duplicates", "Pictures_Without_Date"]
    
    # Not check already in use Direcotries, could make this part of the code much more efficient, but not neccessary
    dirs_to_ignore = (dirs_to_make.copy())
    dirs_to_ignore.append(".venv")
    dirs_to_ignore.append(".ipynb_checkpoints")

    # Create the directories
    for directory in dirs_to_make:
        os.makedirs(directory, exist_ok=True)
    # Init all paths
    all_paths = []
    
    working_dir = os.getcwd()
    get_all_subdirectories_with_files(working_dir, all_paths, dirs_to_ignore)
    
    total_paths = len(all_paths)

    for i, current_path in enumerate(all_paths):
        current_fnames =  get_fnames_from_path(current_path)
        for fname in current_fnames:
            current_suffix = get_suffix(fname)
            if current_suffix in images_suffixes:
                current_fpath = os.path.join(current_path,fname)
                current_date_time = get_datetime_from_imagepath(current_fpath,  current_suffix)
                new_file_name, date_available  = make_filename_from_datetime(current_date_time, fname, current_suffix)

                if date_available:
                    most_of_the_logic("Pictures_With_Dates",new_file_name, current_fpath, current_suffix)
                else:
                    most_of_the_logic("Pictures_Without_Date",new_file_name, current_fpath, current_suffix)
                print(f"New filename is:\t {new_file_name}")

            else:
                print(f"Suffix NOT okay:\t {current_suffix}")
        # Test block in order to not run forever
        #if i > 10:
        #    break
        print(f"Directory {i} of {total_paths} DONE")
