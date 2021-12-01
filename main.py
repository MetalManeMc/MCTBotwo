from inspect import stack
import json
import os
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
path = os.path.dirname(os.path.realpath(__file__)) + "\\" # Full path for debug. Blank string when in the same directory.
langpath=path+"lang\\"
print("Langpath print out: "+langpath)
debug=False # Mark as True if you are on your pc and don't want to turn the bot on
guild_ids = [906169345007304724]


def find(search, inside, outputlist = False, isdictionary = False, errorOut = True): # Function that returns a list or first find of found searches inside a list or dictionary
    o = []
    if not isdictionary: # Searches for keys or if it is list, the values of the list
        for i in inside:
            if search.lower() in i.lower():
                if outputlist:
                    o.append(i)
                else:
                    return i
    else: # Searches for values instead of keys
        for i in inside:
            if search.lower() in inside[i].lower():
                if outputlist:
                    o.append(i)
                else:
                    return i
    if outputlist and len(o) > 0:
        return o
    elif errorOut: # If nothing is found and we want it to, it will throw an error
        raise Exception("Did not find the term")
    else: # If nothing is found, return the same value inputted
        return search


def unpack(string, file): # Bool on the [1] means if it was searched for (Unexact match)
    for key in file: # Tries to match exactly with lowercase
        if file[key].lower() == string:
            return key, False
    
    keys=[] # Tries to search the string
    for key in find(string,file,True,True):
        keys.append(key)
    if len(keys) > 0:
        return keys, True
    raise Exception("Did not find string")

def fetch(key,file): # Bool on the [1] means if it was searched for (Unexact match)
    try: # Tries to match exactly with lowercase
        return file[key].lower(), False
    except: # Searches every key in the file
        strings=[]
        for i in find(key, file, True):
            strings.append(i)
        if len(strings) > 0:
            return strings, True
        raise Exception("Did not find the key")
                    
def google(input, target, source): # Renamed string to input to avoid confusion
    # File finding section-----------V
    try: # This is a language file which we will use for keyfinding when source is key
        en_us = json.load(open(langpath + "en_us.json"))
    except:
        print("DID NOT FIND THE EN_US LANGUAGE!!! PLZ FIX")
        
    if source!="key":
        try: # Find the target language files
            sourcesrch = find(source, langcodes) # If the code is full, this function will return the same thing, so no need to check
        except:
            return "This source language is not in the game."
        try:
            sourcefile = json.load(open(langpath + sourcesrch+".json"))
        except:
            return "This source language's file does not exist!"
    if target!="key":
        try: # Find the source language files
            targetsrch = find(target, langcodes)
        except:
            return "This target language is not in the game."
        try:
            targetfile = json.load(open(langpath + targetsrch + ".json"))
        except:
            return "This target language's file does not exist!"
    # File finding section-----------^

    if source == "key":
        if target == "key":
            try:
                return ktk(input, en_us)
            except:
                return "An unexpected error has occured at ktk."
        else:
            try:
                return kts(input, targetfile)
            except:
                return "An unexpected error has occured at kts."
    else:
        if target=="key":
            try:
                return stk(input, sourcefile)
            except:
                return "An unexpected error has occured at stk."
        else:
            try:
                return sts(input, sourcefile, targetfile)
            except:
                return "An unexpected error has occured at sts."

def ktk(key, file): # Key to key
    if debug:
        print("ktk")
    keys = []
    try:
        for i in find(key, file, True):
            keys.append(i)
    except:
        return "No keys found. I guess you are stuck outside now ¯\\_(ツ)_/¯"
    return nearMatch(keys)

def kts(key, targetfile): # Key to string
    if debug:
        print("kts")
    try:
        strings = fetch(key, targetfile)
    except:
        return "Did not find the key."
    if strings[1]:
        return nearMatch(strings[0])
    else:
        return strings[0]

def stk(string, sourcefile): # String to key
    if debug:
        print("stk")
    try:
        keys=unpack(string, sourcefile)
    except:
        return "Did not find the string."
    if keys[1]:
        return nearMatch(keys[0])
    else:
        return keys[0]

def sts(string, sourcefile, targetfile): # String to string
    if debug:
        print("sts")
    try:
        keys=unpack(string, sourcefile)
    except:
        return "Did not find the string."
    if keys[1]:
        strings=[]
        for i in keys[0]:
            strings.append(targetfile[i])
        return nearMatch(strings)
    else:
        return fetch(keys[0],targetfile)[0]

def nearMatch(of):
    if len(of) == 1:
        return "Near match: " + of[0]
    else:
        return "Near matches found: '"+"', '".join(of)+"'"
    

for a, b, c in os.walk(langpath): # Gives a list of language codes, so i can search in them
    filenames = c
    break
langcodes = []
for i in filenames:
    langcodes.append(i.split(".")[0])
for i in filenames:
    langcodes.append(fetch("language.name", json.load(open(langpath+i)))[0])
# Language names get found and we can fill them in with find() but it isn't the file name so it outputs "file not found" for now... pls fix
    
@slash.slash(name="translate",
             description="Returns the translation found in-game for a string",
             guild_ids=guild_ids,
             options=[
                 create_option(
                     name="string",
                     description="The string or key to translate.",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="target",
                     description="Language code, in which the string is going to be sent. EX: es_es",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="source",
                     description="'key' or language code, in which the string is going to be retrieved. EX: fr_fr, key",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def translate(ctx, string, target, source = "en_us"):
    try:
        await ctx.send(google(string, target, source))
    except:
        print("Error has occured, trying to fallback", string,target ,source)
        try:
            await ctx.send("Error has occured, but fallback works: " + " ".join(google(string,target,source)))
        except:
            print("Error fallback did not work!")
            await ctx.send("Error has occured and fallback did not work!")

@slash.subcommand(base="settings", name="default-language",
                    description="Sets the default target language of a server", guild_ids=guild_ids,
                    options=[create_option(
                        name="target-language",
                        description="language code",
                        option_type=3,
                        required=True
                    )])
async def settings_default_language(ctx, language):
    await ctx.send("wip " + language)

@client.event
async def on_ready():
    print("Online!")

if debug: # Tries to make all possible outcomes...
    input("Press Enter")
    debugstr=["gold","zlato","Gold Ingot","Zlatá tehlička","item.minecraft.gold_ingot","asdf"]
    dabuglangcode1=["sk","us","key","sk_sk","en_us","Slove","Slovenčina","asdf"]
    dabuglangcode2=["sk","us","key","sk_sk","en_us","Slove","Slovenčina","asdf"]
    for a in debugstr:
        for b in dabuglangcode1:
            for c in dabuglangcode2:
                print(a, b,c + ":", google(a, b, c))

while debug:# This runs when you want to test this offline
    print(google(input("string: "), input("target: "), input("source: ")))

client.run(open(path + "token.txt").read())