from pymediainfo import MediaInfo

import os
import shutil
import pathlib

from typing import Any


from sort_images import get_all_subdirectories_with_files, get_suffix, get_fnames_from_path, check_if_filename_exist, make_duplicate_fname, move_file, initial_fname_update

movies_suffixes = [".MOV", ".mov"]


def get_video_date_time(path_to_video : str)-> tuple[Any,bool] : 
    media_info = MediaInfo.parse(path_to_video)
    general_track = media_info.general_tracks[0]

    date = general_track.encoded_date

    if type(date) != None:
        return date, True

    else:
        return date, False


def video_file_string_to_fname_date(video_time_string : str, suffix :str)-> str:
    #"2014-12-13 17:04:35 UTC"
    video_time_string_1 = video_time_string.strip(" UTC")
    video_time_string_2 = video_time_string_1.replace("-", "_")
    video_time_string_3 = video_time_string_2.replace(":", "_")
    video_time_string_4 = video_time_string_3.replace(" ", "_")

    return f"{video_time_string_4}{suffix}"


# TODO: MAKE THIS THE RICHT ONE
def most_of_the_logic_video(folder_to_check, new_file_name, current_fpath, current_suffix):
    if check_if_filename_exist("Videos_Potential_Duplicates", new_file_name):
        criteria = True
        num_duplicates = 1
        fnames_potential_duplicates = os.listdir("Videos_Potential_Duplicates")
        while(criteria):
            new_dupicate_fname = make_duplicate_fname(new_file_name, current_suffix, num_duplicates)
            if new_dupicate_fname in fnames_potential_duplicates:
                num_duplicates += 1
            else:
                criteria = False
        new_dupicate_fname = make_duplicate_fname(new_file_name, current_suffix, num_duplicates)
        move_file(current_fpath, os.path.join("Videos_Potential_Duplicates",new_dupicate_fname))

    elif check_if_filename_exist(folder_to_check, new_file_name):
        move_file(os.path.join(folder_to_check, new_file_name), os.path.join("Videos_Potential_Duplicates", new_file_name))
        file_name_init_duplicate = initial_fname_update(new_file_name, current_suffix)
        move_file(current_fpath, os.path.join("Videos_Potential_Duplicates", file_name_init_duplicate))
    else:
        move_file(current_fpath, os.path.join(folder_to_check, new_file_name))

if __name__ == "__main__":
    
    working_dir = os.getcwd()
    working_dir = os.path.join(working_dir, "reflink_never_videos")

    # Make directories to put all the images in
    dirs_to_make = ["Videos_With_Dates", "Videos_Potential_Duplicates", "Videos_Without_Date"]
    
    # Not check already in use Direcotries, could make this part of the code much more efficient, but not neccessary
    dirs_to_ignore = ["Videos_With_Dates", "Videos_Potential_Duplicates", 
                      "Videos_Without_Date","__pycache__","Pictures_Potential_Duplicates",
                      "Pictures_Without_Date", "Pictures_With_Dates"]

    # TODO: WRITE THSIS MANUALLY
    dirs_to_ignore.append(".venv")
    dirs_to_ignore.append(".ipynb_checkpoints")

    # Create the directories
    for directory in dirs_to_make:
        os.makedirs(directory, exist_ok=True)
    # Init all paths
    all_paths = []
    
    get_all_subdirectories_with_files(working_dir, all_paths, dirs_to_ignore)
    
    total_paths = len(all_paths)

    for i, current_path in enumerate(all_paths):
        current_fnames =  get_fnames_from_path(current_path)
        for fname in current_fnames:
            current_suffix = get_suffix(fname)
            if current_suffix in movies_suffixes:
                current_fpath = os.path.join(current_path,fname)
                current_date_time, date_available = get_video_date_time(current_fpath)
                if date_available:
                    new_file_name = video_file_string_to_fname_date(current_date_time, current_suffix)
                else:
                    new_file_name = fname
                if date_available:
                    most_of_the_logic_video("Videos_With_Dates", new_file_name, current_fpath, current_suffix)
                else:
                    most_of_the_logic_video("Videos_Without_Date",new_file_name, current_fpath, current_suffix)
            else:
                print(f"Suffix NOT okay:\t {current_suffix}")
        print(f"Directory {i} of {total_paths} DONE")
