import shutil

def save_file(file, path):
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)