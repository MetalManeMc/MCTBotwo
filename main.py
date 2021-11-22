import json
import os
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
path="" #full path for debug. can be a blank string.
debug=False #True if you are on your pc and don't want to turn the bot on

for a, b, c in os.walk(path+"lang"): #Gives a list of language codes, so i can search in them
    filenames=c
    break
langcodes=[]
for i in filenames:
    langcodes.append(i.split(".")[0])


        

guild_ids = [906169345007304724]
@client.event
async def on_ready():
    print("Online!")



def finder(search,inside=langcodes,outputlist=False,isdictionary=False): #returns list of found searches inside a list (by default, searches in langcodes)
    o=[]
    if not isdictionary:
        for i in inside:
            if search.lower() in i.lower():
                if outputlist:
                    o.append(i)
                else:
                    return i
    else: #I believe that a problem is here... i don't know how can i not check for values in disctionary or something...
        for i in inside:
            if search in inside[i].lower():
                if outputlist:
                    o.append(i)
                else:
                    return i

    if outputlist:
        return o
    else:
        return search
                
    
def translater(string, target, source): #function for the non-key source language
    try: #tries to open source and target language files. we searched for the codes earlier in the code, so it should be ok
        sourcefile = json.load(open(path+"lang/"+source+".json"))
    except:
        return f"Source language was not found. {target}, {source}."
    try:
        targetfile = json.load(open(path+"lang/"+target+".json"))
    except:
        return f"Target language {target} was not found."
    

    for key in sourcefile: #tries to match exactly with lowercase
        if sourcefile[key].lower() == string:
            return targetfile[key]
    
    try: #tries to search in the dictionary or whatever
        return targetfile(finder(string,sourcefile,isdictionary=True)) #problem may be in here too...
    except:
        listreturn=[] #will return a list of unexact matches
        for i in finder(string,sourcefile,True):
            listreturn.append(targetfile[i])
        
        try: #this try except is here because i have a small expectation of error...
            if len(listreturn) > 1: #joins list or outputs one string
                return "Unexact matches: "+"|".join(listreturn)
            elif len(listreturn) > 0:
                return "Unexact match: "+listreturn[0]
        except:
            print(len(listreturn))
            return "Something went wrong when joining list..."
    
    print(string,target,source,listreturn) #the final return fallback. was: "Invalid string"
    return f"Did not find the {string} in {source} to {target}."


def fetch_translation(target, string): #finds a translation based on a key
    try:
        return json.load(open(path+f"lang/{target}.json"))[string] #changed .get() for [] bc we want an error raised, not None value | returns when matching exactly
    except: #my fallback fetcher
        try:
            file=json.load(open(path+f"lang/{target}.json"))
        except:
            return f"Did not find the {target} language code."
        try:
            return f"Found: '{file[string]}' in {target}."
        except:
            try:
                listreturn=[]
                for i in finder(string,file,True):
                    listreturn.append(file[i])
                return f"Found: '{'|'.join(listreturn)}' in {target}."
            except:
                return f"Did not find the string {string} in "+target
                    

    
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
                     name="sourcelang",
                     description="'key' or language code, in which the string is going to be retrieved. EX: fr_fr, key",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def translate(ctx, string, target, sourcelang = "en_us"): #moved out the googler bc it made the debugging a lot easier for me and does not change a thing
    await ctx.send(google(string,target,sourcelang))
def google(string, target,  sourcelang = "en_us"):
    if sourcelang == "key":
        return fetch_translation(finder(target.lower()), string.lower())
    else:
        return translater(string.lower(), finder(target.lower()), finder(sourcelang.lower()))




while debug:#this runs when you want to test this offline
    print(translate(input("string: ").lower(), finder(input("target: ").lower()), finder(input("source: ").lower())))

client.run(open(path+"token.txt").read())
