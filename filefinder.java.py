"""This filters the lang files from the assets"""
import os
import json

# Important: How to use
# 1 - Copy the latest index from .minecraft\assets\indexes
# 2 - Delete all non-language indexes and rename the file to langcodes.json
# 3 - Copy the objects folder from .minecraft\assets
# 4 - Run the filefinder
# 5 - Extract en_us form the version jar and manually insert it in the java lang folder

langs = json.load(open("langcodes.json", encoding="utf-8"))   # Opens the language index
codes = []

def rename(initname):
    """Renames files in language index"""
    for i in langs:
        if langs[i]["hash"] == initname:
            tempname=i
    newname=tempname.replace("minecraft/lang/", "")
    return newname


for lang in langs:                           # For all element in the index
    codes.append(langs[lang]["hash"])        # Notes the "hash"

for dirpath, dirnames, filenames in os.walk("objects"): # Runs through the minecraft assets
    for file in filenames:                              # For each file
        if file not in codes and ".json" not in file:   # If the file name isn't in the hash list
            os.remove(os.path.join(dirpath, file))      # Deletes them
        elif "json" not in file:                        # Else
            newfile=rename(file)                        # Renames the files variable...
            print(newfile)
            os.rename(                                  # Before renaming the file
                os.path.join(dirpath, file), os.path.join(dirpath, rename(file))
                )
            print(newfile)

for dirpath, dirnames, filenames in os.walk("objects"):
    for file in filenames:
        print(file)
        os.replace( # Places the lang files in the "lang/java" folder, emptying "objects"
            os.path.join(dirpath, file), os.path.join(r"lang\java", file)
            )

en=json.load(open(os.path.join("lang/java", file), "r", encoding="utf-8")) # Opens the english file
for dirpath, dirnames, filenames in os.walk(r"lang\java"):
    for file in filenames:
        if file!="en_us.json":
            with open(os.path.join("lang/java", file), "r", encoding="utf-8") as f:
                data = json.load(f)
                for x in list(en.keys()):
                    try:
                        n=data[x]
                    except KeyError:
                        data[x]=""
                        print(f"{x} added to {file}")
                json.dump(data, open(os.path.join("lang/java", file), "w", encoding="utf-8"))
