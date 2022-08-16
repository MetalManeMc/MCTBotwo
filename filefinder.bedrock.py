# This filters the lang files from the default rp

import os
import json

def rename(initname):
    name=initname.replace('lang', "")
    name=name+"json"
    name=name.lower()
    return name

for dirpath, dirnames, filenames in os.walk("texts"):
    for file in filenames:
        if file=="language_names.json":
            os.replace(os.path.join(dirpath, file), file)
        if ".lang" in file:
            os.replace(os.path.join(dirpath, file), os.path.join("lang/bedrock", file)) # Places the lang files in the "lang/bedrock" folder. The "texts" one should be empty
            print(file, "moved")
        else:
              os.remove(os.path.join(dirpath, file))

for dirpath, dirnames, filenames in os.walk("lang/bedrock"):
    for file in filenames:
        if ".json" not in file:
            os.rename(f"{dirpath}/{file}", f"{dirpath}/{rename(file)}") # ... renames the file
            print(f"{file} renamed into .json")

for dirpath, dirnames, filenames in os.walk("lang/bedrock"):
    for file in filenames:
        try:
            f=open(os.path.join(dirpath, file), 'r+', encoding='utf-8').read()
            f=f.split("\n")
            for x in f:
                old=x
                #print(x)
                try:
                    removefrom = lambda s, ss: s[:s.index(ss) + len(ss)]
                    x=removefrom(x, "#")
                    x=x.replace("#", "")
                    #print(x)
                except ValueError: pass
                if "=" in x:
                    y=x.split("=")
                    try: 
                        a=y[2]
                        together=[y[1], y[2]]
                        y[1]="=".join(together)
                        del y[2]
                    except IndexError:pass
                    try: 
                        a=y[2]
                        together=[y[1], y[2]]
                        y[1]="=".join(together)
                        del y[2]
                    except IndexError:pass
                    for z in y:
                        oldz=z
                        z=z.replace("\t", "")
                        z=z.replace('\\', "\\"+"\\")
                        z=z.replace('"', r'\"')
                        y[y.index(oldz)]='"'+z+'"'
                    f[f.index(old)]=":".join(y)
                    x=":".join(y)
                    #print(x)
                else:pass
            delete=[]
            for i in f:
                if "#" in i:
                    delete.append(f.index(i))
            for k in delete:
                i=delete.index(k)
                f.remove(f[delete[-(i+1)]])
            f = list(filter(("").__ne__, f))
            f = list(filter((" ").__ne__, f))
            f="{"+",\n".join(f)+"}"
            f=f+"\n"
            open(os.path.join(dirpath, file), "r+", encoding='utf-8').write(f)
            #print(f)
        except UnicodeDecodeError:pass
print("Done.")