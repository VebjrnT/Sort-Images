from pymediainfo import MediaInfo

import os
import shutil
import pathlib

from typing import Any


movies_suffixes = [".MOV", ".mov"]


def get_video_date_time(path_to_video : str)-> tuple[Any,bool] : 
    media_info = MediaInfo.parse(path_to_video)
    general_track = media_info.general_tracks[0]

    date = general_track.encoded_date

    if type(date) != None:
        return date, False

    else:
        return date, True


def video_file_string_to_fname_date(video_time_string : str, suffix :str)-> str:
    #"2014-12-13 17:04:35 UTC"
    video_time_string_1 = video_time_string.strip(" UTC")
    video_time_string_2 = video_time_string_1.replace("-", "_")
    video_time_string_3 = video_time_string_2.replace(":", "_")
    video_time_string_4 = video_time_string_3.replace(" ", "_")

    return f"{video_time_string_4}{suffix}"


if __name__ == "__main__":
    test_path = "/home/vebjornt/AirStore2/Pictures/iPhoto Library.migratedphotolibrary/Previews/2014/12/18/20141218-153255/9ReMInzyQbqXGjy6PVBmfg/MVI_1699.MOV"
    print(__name__)

    test_date = get_video_date_time(test_path)

    new_fname = video_file_string_to_fname_date(test_date[0], ".MOV")
    print(f"New Video Filename is:\t {new_fname}")
