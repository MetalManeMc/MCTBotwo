# This filters the lang files from the assets

import os
import json

langs = json.load(open("langcodes.json"))   # Opens the language index (from the minecraft assets)
codes = []

def rename(initname):
    for x in langs:
        if langs[x]["hash"]+".json" == initname:
            tempname=x
    newname=tempname.replace("minecraft/lang/", "")
    return newname


for lang in langs:                          # For all element in the index
    codes.append(langs[lang]["hash"])       # Notes the "hash", which is the code of used for the game to know which assets are which

for dirpath, dirnames, filenames in os.walk("objects"): # Runs through the minecraft assets
    for file in filenames:                              # For each file
        if file not in codes and ".json" not in file:   # If the name of the files aren't in the language hash list
            os.remove(os.path.join(dirpath, file))      # Deletes them
        elif "json" not in file:                        # Else
            newfile=rename(file)                        # Renames the files variable...
            os.rename(os.path.join(dirpath, file), os.path.join(dirpath, rename(file)))         # ... before renaming the actual file
            os.rename(os.path.join(dirpath, newfile), os.path.join(dirpath, newfile) + ".json") # Renames them in ".json"

for dirpath, dirnames, filenames in os.walk("objects"):
    for file in filenames:
        os.replace(os.path.join(dirpath, file), os.path.join("lang", file)) # Places the lang files in the "lang" folder. The "objects" one should be empty

for dirpath, dirnames, filenames in os.walk("lang"):
    for file in filenames:
        if "-" not in file:                                                             # If not already done...
            os.rename(os.path.join(dirpath, file), os.path.join(dirpath, rename(file))) # ... renames the file