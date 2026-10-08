import zipfile
import sys


zip_filename = sys.argv[1]

with open(zip_filename, "rb") as file:
    with zipfile.ZipFile(file, "r") as zip_file:
        for filename in zip_file.namelist():
            with zip_file.open(filename, "r") as in_file:
                with open(filename, "wb") as out_file:
                    out_file.write(in_file.read())
