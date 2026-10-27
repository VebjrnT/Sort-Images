import os

from sort_images import get_suffix, move_file, check_if_filename_exist, make_duplicate_fname
from sort_videos import get_video_date_time, video_file_string_to_fname_date


if __name__ == "__main__":
    print(os.listdir())

    directories = ['Videos_With_Dates', 'Videos_Potential_Duplicates', 'Videos_Without_Date']

    for directory in directories:
        fnames = os.listdir(directory)
        for fname in fnames:
            current_suffix = get_suffix(fname)
            img_path = os.path.join(directory,fname)
            time_string, time_exist = get_video_date_time(img_path)
            
            if time_exist:
                time_fname = video_file_string_to_fname_date(time_string,current_suffix)
                new_fpath = os.path.join(directory, time_fname)

                if check_if_filename_exist(directory, new_fpath):

                    criteria = True
                    num_duplicates = 1
                    fnames_potential_duplicates = os.listdir(directory)
                    new_dupicate_fname = make_duplicate_fname(new_fpath, current_suffix, num_duplicates)

                    while(criteria):
                        new_dupicate_fname = make_duplicate_fname(new_dupicate_fname, current_suffix, num_duplicates)
                        if check_if_filename_exist(directory,new_dupicate_fname):
                            num_duplicates += 1
                        else:
                            criteria = False

                    new_dupicate_fname = make_duplicate_fname(new_dupicate_fname, current_suffix, num_duplicates)
                    move_file(img_path, os.path.join(directory, new_dupicate_fname))

                else:
                    move_file(img_path, new_fpath)


            else:
                print("Time NOT FOUND")
