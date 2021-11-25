import json
import os
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
path="C:\\Users\\matej\\Desktop\\" #full path for debug. can be a blank string.
debug=True #True if you are on your pc and don't want to turn the bot on

for a, b, c in os.walk(path+"lang"): #Gives a list of language codes, so i can search in them
    filenames=c
    break
langcodes=[]
for i in filenames:
    langcodes.append(i.split(".")[0])
#language.name is the key of language names


        

guild_ids = [906169345007304724]
@client.event
async def on_ready():
    print("Online!")


def find(search,inside=langcodes,outputlist=False,isdictionary=False,errorOut=False): #returns list or first find of found searches inside a list (by default, searches in langcodes)
    o=[]
    if not isdictionary: #Searches for keys or if it is list, the values of the list
        for i in inside:
            if search.lower() in i.lower():
                if outputlist:
                    o.append(i)
                else:
                    return i
    else: #Searches for values instead of keys
        for i in inside:
            if search.lower() in inside[i].lower():
                if outputlist:
                    o.append(i)
                else:
                    return i
    if outputlist and len(o)>0:
        return o
    elif errorOut: #if nothing is found and we want it to, it will throw an error
        raise Exception("Did not find the term")
    else: #If nothing is found, return the same value inputted
        return search


def unpack(string, file): #Bool on the [1] means if it was searched for (Unexact match)
    for key in file: #tries to match exactly with lowercase
        if file[key].lower() == string:
            key=[key]
            return key, False
    
    keys=[] #tries to search the string
    for key in find(string,file,True,True):
        keys.append(key)
    if len(keys)>0:
        return keys, True
    raise Exception("Did not find string")

def fetch(key,file): #Bool on the [1] means if it was searched for (Unexact match)
    try: #tries to match exactly with lowercase
        return [file[key].lower()], False
    except: #searches every key in the file
        strings=[]
        for i in find(key,file,True):
            strings.append(i)
        if len(strings)>0:
            return strings, True
        raise Exception("Did not find the key")
                    

    
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
    await ctx.send(google(string,target,source))

def google(string, target, source):
    #File finding section-----------V
    try: #this is a language file which we will use for keyfinding when source is key
        en_us=json.load(open(path+"lang/en_us.json"))
    except:
        print("DID NOT FIND THE EN_US LANGUAGE!!! PLZ FIX")
    if target!="key":
        try: #find the target language files
            sourcesrch=find(source) #if the code is full, this function will return the same thing, so no need to check
        except:
            return "This source language is not in the game."
        try:
            sourcefile=json.load(open(path+f"lang/{sourcesrch}.json"))
        except:
            return "This source language's file does not exist!"
    if source!="key":
        try: #find the source language files
            targetsrch=find(target)
        except:
            return "This target language is not in the game."
        try:
            targetfile=json.load(open(path+f"lang/{targetsrch}.json"))
        except:
            return "This target language's file does not exist!"
    #File finding section-----------^


    if source=="key": #searches if the key even exists
        try:
            if fetch(string,en_us)[1]: #using the fetch function as a validation of exact match... True in [1] means it exists but was searched for, False means it's exact... It also errors out when the key doesn't exist
                keys=[find(string,en_us,True),True]
            else:
                keys=[[string],False]
        except:
            return "The key you searched for doesn't exist!"
    else: #If we are not searching with key, unpack the string's key(s)
        try:
            keys=unpack(string,sourcefile)
        except:
            return "Did not find the string."
    

    if target=="key":
        if not keys[1]:#If it wasn't searched for
            return keys[0][0]
        else:#If it was searched for
            if len(keys[0])>1:
                return "Near matches: '"+"', '".join(keys[0])+"'"
            else:
                return "Near match: "+keys[0][0]
    else:
        try:
            strings=[]
            for i in keys[0]:
                try:
                    strings.append(fetch(i,targetfile)[0])
                except:
                    pass
            if len(strings)==0:
                raise Exception("")
            elif len(strings)>1:
                return "Near matches: '"+"', '".join(strings)+"'"

        except:
            return "An unspecified error has popped up."
        
        
    
if debug: #tries to make all possible outcomes...
    strings=["gold","zlato","Gold Ingot","Zlatá tehlička","item.minecraft.gold_ingot","asdf"]
    codes1=["sk","us","key","sk_sk","en_us","asdf"]
    codes2=["sk","us","key","sk_sk","en_us","asdf"]
    for a in strings:
        for b in codes1:
            for c in codes2:
                print(a,b,c+":",google(a,b,c))


    




while debug:#this runs when you want to test this offline
    print(google(input("string: "), input("target: "), input("source: ")))

client.run(open(path+"token.txt").read())
