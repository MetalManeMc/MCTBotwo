import json
import os
from pathlib import Path
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

DATA_DIR = Path(os.getcwd(), 'lang')
TOKEN_PATH = Path(os.getcwd(), 'token.txt')
GUILD_IDS = [906169345007304724]
with open(TOKEN_PATH) as f:
    TOKEN = f.read()

"""
We craft a path towards the /lang/ folder using the host's information. 
This path is absolute and independent of the OS in which it may be running.
DATA_DIR should *not* be altered at any point. 
"""

@client.event
async def on_ready():
    print("Online!")
    print(f"Path towards //lang// is {DATA_DIR}")

############################################################################
#                             Code starts here                             #
############################################################################

def open_json(jsonfile): 

    """
    This function open a file that's specified through the command.
    The first line establishes that json_path is 
    Path (a .join for paths, part of the Pathlib) DATA_DIR (the base path towards /lang/)
    and jsonfile, jsonfile is established by the command and automatically 
    transforms an input such as "es_es" into "es_es.json". 

    After this, it json.loads the file into memory by turning it into a 
    dictionary called dictionary_json. The file is then closed and 
    from now on ONLY the dictionary that was returned will be used.

    """

    json_path = Path(DATA_DIR, jsonfile).with_suffix(".json")

    with open(json_path) as js:
        dictionary_json = json.load(js)

    return dictionary_json

  
def search_str(js, string):

    """
    This is the soul of the bot. It takes in js and string
    as arguments. js is the file that will be searched (the langcode specified
    by the user) and string is the text that will be searched by the bot.

    Firstly, it defines an emtpy list called result, afterwards it 
    runs a loop through the keys in the dictionary and searches for
    any matches that contain string. If a key that contains string is found
    the program will append the value associated with that key to the empty
    list, and will repeat the loop.

    Once the loop is done, another check is ran. If the length of result is 0
    the bot will assume that no matches were found. If this is the case, the
    same operation from before is ran again, but in inverse order. It searches
    for any value in the dictionary that contains string and appends its key
    to result.

    At the end of the function, result is returned.
    """

    result = []

    for k in js.keys():
        if string in k:
            result.append(js[k])

    if len(result) == 0:
        result = [k for v in js.values() if string in v]
    return result



def find_translation(jsonfile:str, string:str):

    """
    This function takes in 2 parameters: jsonfile and string. Both of these are
    specified to be strings. 
    It first converts the parameters into variables that can be used by the program.
    In this case, jsonfile is turned into jsonfile.lower() and then fed into
    open_json. The result of that is turned into the variable js.

    Similarly, the string is turned into string.lower and fed into search_str
    alongside js so it can return a list called result. This result is then returned 
    for the bot to interpret and embed into a message.
    """

    js = open_json(jsonfile.lower())
    result = search_str(js, string.lower())

    return result


#########################
## HUGE WARNING HERE!  ##
## ERROR HANDLING HAS  ##
## NOT BEEN YET ADDED  ##
#########################

# TODO Implement proper error handling (No try/except stacks, those are hard to read)
# TODO Implement a result limit for the embed, we don't want to flood everything
# TODO Make it user friendly through descriptions, a help command and whatnot
# TODO Make cool looking embeds, these are just a placeholder
# TODO Re-implement the default language per channel/server thing (Sorry -Nan)
# TODO The command simply vomits the contents of the list result into chat with no order or format, should be formatted

@slash.slash(name="translate",
             description="Returns the translation found in-game for a string",
             guild_ids=GUILD_IDS,
             options=[
                 create_option(
                     name="language",
                     description="PLACEHOLDER",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="target",
                     description="PLACEHOLDER",
                     option_type=3,
                     required=True
                 )
             ]
             )
async def translate(ctx, language, target):
    list_message = find_translation(language, target)
    message = ', '.join(list_message)
    if message == '':
        await ctx.send('Empty')
        return
    await ctx.send(message)

client.run(TOKEN)
