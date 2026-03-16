import shutil

# Service function to save uploaded file to a specified path
def save_file(file, path):
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)