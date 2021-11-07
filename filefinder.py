# This filters the lang files from the assets

import os
import json

langs = json.load(open("langcodes.json"))   # Opens the language index (from the minecraft assets)
codes = []

for lang in langs:                          # For all element in the index
    codes.append(langs[lang]["hash"])       # Notes the "hash", which is the code of used for the game to know which assets are which

for dirpath, dirnames, filenames in os.walk("objects"): # Runs through the minecraft assets
    for file in filenames:                              # For each file
        if file not in codes and ".json" not in file:   # If the name of the files aren't in the language hash list
            os.remove(os.path.join(dirpath, file))      # Deletes them
        elif "json" not in file:                        # Else
            os.rename(os.path.join(dirpath, file), os.path.join(dirpath, file) + ".json")   # Renames them in ".json"

for dirpath, dirnames, filenames in os.walk("objects"):
    for file in filenames:
        os.replace(os.path.join(dirpath, file), os.path.join("lang", file))