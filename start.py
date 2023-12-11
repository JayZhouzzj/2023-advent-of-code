import os
import shutil


def create_day_folder(day):
    # Create folder name
    folder_name = f"day{day}"
    file_name = f"{folder_name}.py"
    prev_day_file = f"day{day-1}/day{day-1}.py"

    # Create the folder
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Create files in the folder
    open(os.path.join(folder_name, file_name), "a").close()
    open(os.path.join(folder_name, "input.txt"), "a").close()
    open(os.path.join(folder_name, "sample.txt"), "a").close()

    # Copy content from previous day's file if it exists
    if day > 1 and os.path.isfile(prev_day_file):
        shutil.copy(prev_day_file, os.path.join(folder_name, file_name))


# Take input
day = int(input("Enter the day number: "))
create_day_folder(day)
