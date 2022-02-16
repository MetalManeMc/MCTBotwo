# This filters the lang files from the default rp

import os

def rename(initname):
    name=initname.replace('lang', "")
    name=name+"json"
    return name

for dirpath, dirnames, filenames in os.walk("texts"):
    for file in filenames:
        if ".lang" in file:
            os.replace(os.path.join(dirpath, file), os.path.join("lang/bedrock", file)) # Places the lang files in the "lang/bedrock" folder. The "texts" one should be empty
            print(file, "moved")
        else:
            os.remove(os.path.join(dirpath, file))

for dirpath, dirnames, filenames in os.walk("lang/bedrock"):
    for file in filenames:
        print(dirpath, file)
        os.rename(f"{dirpath}/{file}", f"{dirpath}/{rename(file)}") # ... renames the file