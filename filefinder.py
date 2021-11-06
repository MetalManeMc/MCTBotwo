import os
import json

langs=json.load(open("langcodes.json"))
codes=[]
keep=[]

for lang in langs:
    codes.append(langs[lang]["hash"])

for dirpath, dirnames, filenames in os.walk("objects"):
    for file in filenames:
        if file in codes:
            keep.append(file)

print(keep)
print(len(keep))