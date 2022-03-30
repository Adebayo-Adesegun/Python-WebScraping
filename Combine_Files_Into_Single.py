import os

# This code reads through a folder with files, gets text and append to an open file

path = 'D:\Jupyter_NoteBooks\Masters_Project\Project_Implementation\Random_Sample_Data_Sport'
file_name = 'Random_Sample_Data_Sport.txt'

os.chdir(path)


def append_text_to_file(text):
    try:
        with open(file_name, 'a+') as f:
            f.write(f"{text} %d\r\n")

    except Exception as e:
        print(e)


def read_text_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        file_path = f"{path}\{file}"

        # call read text file function
        text = read_text_file(file_path)
        print(len(text))
        append_text_to_file(text)
