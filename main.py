import json
import os
from pathlib import Path
import interactions

DATA_DIR = Path(os.path.dirname(os.path.realpath(__file__)), 'lang')
TOKEN_PATH = Path(os.path.dirname(os.path.realpath(__file__)), 'token.txt')
SCOPES = [906169345007304724]
with open(TOKEN_PATH) as f:
    TOKEN = f.read()

"""
We craft a path towards the /lang/ folder using the host's information. 
This path is absolute and independent of the OS in which it may be running.
DATA_DIR should *not* be altered at any point.
"""

#client = discord.Client(intents=discord.Intents.all())  # Unused as of right now
bot = interactions.Client(token=TOKEN)

@bot.event
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
        return json.load(js)


def complete(search:str, inside:list):

    '''
    This function is essentially an autocompletion.
    It takes a string and a list, in which it's going to find complete strings.

    Walks through the list and asks whether the search is in the value. If it is,
    it appends the value to result. If none are found, it returns an empty list.
    '''

    return [i for i in inside if search.lower() in i.lower()]


def find_translation(string:str, targetlang:str, sourcelang:str): # outputs a list of found items

    """
    This function does not make a documentation by itself. It needs to be made up by someone else.
    """

    string = string.lower()
    # we can put something like find(languages) for user to be able to insert uncomplete languages

    if targetlang!="key": # if either are key, they should not be searched for as files, instead use jsdef
        jstarget = open_json(lang(targetlang))
    if sourcelang!="key":
        jssource = open_json(lang(sourcelang))
    jsdef = open_json("en_us") # this will get used everytime to key or from key is used... (json default... change the name if you want)


    if targetlang=="key": # figures out, which mode to use
        if sourcelang=="key":
            result = complete(string, jsdef) #ktk
        else:
            result = [i for i in jsdef if string in jssource[i].lower()] #stk
    else:
        if sourcelang=="key":
            result = [jstarget[i] for i in complete(string, jsdef)] #kts
        else:
            result = [jstarget[i] for i in [i for i in jssource if string in jssource[i].lower()]] #sts(string, jstarget, jssource)

    return result

def lang(search:str):

    '''
    Returns a complete internal language code to be used for file opening.

    Input can be the expected output too.
    Input can be approved language code, name, region or internal code (searching in this order)
    '''

    search = search.lower()

    for i in range(len(langcodesapp)): # We can't use complete here because we would have no clue which langcode to use. The thing we need is index of langcode, not completed langname or whatever.
        if search in langcodesapp[i].lower():
            return langcodes[i]

    for i in range(len(langnames)):
        if search in langnames[i].lower():
            return langcodes[i]

    for i in range(len(langregions)):
        if search in langregions[i].lower():
            return langcodes[i]

    return complete(search, langcodes)[0]


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

@bot.command(name = "translate",
             description = "Returns the translation found in-game for a string",
             scope=SCOPES,
             options = [
                interactions.Option(
                    name = "search",
                    description = "String or key to translate.",
                    option_type = interactions.OptionType.STRING,
                    required = True
                ),
                interactions.Option(
                    name = "target",
                    description = "Language code, name or region or 'key' to translate to.",
                    option_type = interactions.OptionType.STRING,
                    required = True
                ),
                interactions.Option(
                    name = "source",
                    description = "Language code, name, or region or 'key' to translate from.",
                    option_type = interactions.OptionType.STRING,
                    required = False
                )
            ])
async def translate(ctx, search, target, source="en_us"):
    list_message = find_translation(search, target, source)
    message = ', '.join(list_message)
    
    if message != '':
        await ctx.send(message)
    else:
        await ctx.send('Empty')

langcodes, langcodesapp, langnames, langregions = [], [], [], []

for a, b, c in os.walk(DATA_DIR): # Gives a list of language codes, so i can search in them
    for i in c:
        langcodes.append(i.split(".")[0].lower())
        langnames.append(open_json(i)["language.name"].lower())
        langcodesapp.append(open_json(i)["language.code"].lower())
        langregions.append(open_json(i)["language.region"].lower())
    break



bot.start()
