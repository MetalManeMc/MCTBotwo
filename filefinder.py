# This filters the lang files from the assets

import os
import json

langs = json.load(open("langcodes.json"))
codes = []

for lang in langs:
    codes.append(langs[lang]["hash"])

for dirpath, dirnames, filenames in os.walk("objects"):
    for file in filenames:
        if file not in codes:
            os.remove(os.path.join(dirpath, file))
        else:
            os.rename(os.path.join(dirpath, file), file + ".json")