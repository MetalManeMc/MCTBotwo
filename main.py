import json
import os
from pathlib import Path
import interactions as di
import requests

DATA_DIR = Path(os.path.dirname(os.path.realpath(__file__)), 'lang')
PATH = Path(os.path.dirname(os.path.realpath(__file__)))

if "\\" in str(DATA_DIR): beta=True
else: beta=False

if beta==True:
    TOKEN_PATH = Path(os.path.dirname(os.path.realpath(__file__)), 'token.txt')
    SCOPES = [906169345007304724]
else:
    TOKEN_PATH = Path(os.path.dirname(os.path.realpath(__file__)), 'token-main.txt')
    SCOPES=None
    print("Running hosted version")

with open(TOKEN_PATH) as f:
    TOKEN = f.read()

"""
We craft a path towards the /lang/ folder using the host's information. 
This path is absolute and independent of the OS in which it may be running.
DATA_DIR should *not* be altered at any point.
"""

#client = discord.Client(intents=discord.Intents.all())  # Unused as of right now, and hopefully shouldn't be
bot = di.Client(token=TOKEN, log_level=31)

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

def fetch_default(code, category, data):
    '''
    This function fetches defaults in serverdefaults.json
    '''
    f = json.load(open("serverdefaults.json"))
    return f[code][category][data]

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
                di.Option(
                    name = "search",
                    description = "String or key to translate.",
                    type = di.OptionType.STRING,
                    required = True
                ),
                di.Option(
                    name = "target",
                    description = "Language code, name or region or 'key' to translate to.",
                    type = di.OptionType.STRING,
                    required = False
                ),
                di.Option(
                    name = "source",
                    description = "Language code, name, or region or 'key' to translate from.",
                    type = di.OptionType.STRING,
                    required = False
                )
            ])
async def translate(ctx: di.CommandContext, search, target=None, source="en_us"):

    if target == None:
        try:
            target = fetch_default(str(ctx.guild_id), "server", "targetlang")
        except:
            target="en_us"
    
    list_message = find_translation(search, target, source)
    message = '\n'.join(list_message)
    if len(list_message)>0:
        r = await bot._http.get_guild(ctx.guild_id)
        ic = ctx.author.user.username
        ids = ctx.author.user.id
        av = ctx.author.user.avatar
        embed = di.Embed(
            title="Found translation",
            fields=[di.EmbedField(name=search,value=message)],
            url=f"https://crowdin.com/translate/minecraft/all/enus-{target}?filter=basic&value=0#q={search}",
            thumbnail=di.EmbedImageStruct(url=f"https://cdn.discordapp.com/icons/{ctx.guild_id}/{r['icon']}")._json,
            author=di.EmbedAuthor(name=f"{ic}",icon_url=f"https://cdn.discordapp.com/avatars/{ids}/{av}"),
        )
        hide=False
    else:
        embed = di.Embed(
            title="Didn't find the translation!",
            description="Click the title to search in Crowdin.",
            url=f"https://crowdin.com/translate/minecraft/all/enus-{target}?filter=basic&value=0#q={search}"
            )
        hide=True
    await ctx.send(embeds=embed,ephemeral=hide)


@bot.command(name = "search",
             description = "Returns a link of searching in Crowdin.",
             scope=SCOPES,
             options = [
                di.Option(
                    name = "search",
                    description = "String or key to search for.",
                    type = di.OptionType.STRING,
                    required = True
                )
            ])
async def search(ctx:di.CommandContext, search):
    await ctx.send(f"https://crowdin.com/translate/minecraft/all?filter=basic&value=0#q={search}")


@bot.command(name = "profile",
             description = "Returns a link of searching in Crowdin.",
             scope=SCOPES,
             options = [
                di.Option(
                    name = "nick",
                    description = "String or key to search for.",
                    type = di.OptionType.STRING,
                    required = True
                )
            ])
async def profile(ctx:di.CommandContext, nick):
    re=requests.get(f"https://crowdin.com/profile/{nick}")
    if re.status_code==200:
        await ctx.send(f"https://crowdin.com/profile/{nick}")
    elif re.status_code==404:
        await ctx.send("This user doesn't exist",ephemeral=True)
    else:
        await ctx.send(f"A {re.status_code} error occured.",ephemeral=True)


@bot.command(name="settings", description="Bot settings", scope=SCOPES,options=[
        di.Option(
            name="default-target-language",
            description="Set the default server target language",
            type=di.OptionType.SUB_COMMAND,
            options=[
                di.Option(
                    name="targetlang",
                    description="The target language",
                    type = di.OptionType.STRING,
                    required=True)])])
async def settings(ctx:di.CommandContext, sub_command, targetlang):
    if sub_command=="default-target-language":
        f=json.load(open(Path(PATH,"serverdefaults.json")))
        try:
            currentlang=f[str(ctx.guild_id)]["server"]["targetlang"]
            if targetlang in langcodes or targetlang in langnames:
                f[str(ctx.guild_id)]["server"]["targetlang"]=targetlang
                await ctx.send(f"Default target language changed to `{targetlang}`.")
            else:
                await ctx.send(f"`{targetlang}` isn't a valid language. Default target language reset to `{currentlang}`.")
        except KeyError:
            if targetlang in langcodes or targetlang in langnames:
                f[str(ctx.guild_id)]={"server":{"targetlang": targetlang}}
                await ctx.send(f"Default target language set to `{targetlang}`.")
            else:
                await ctx.send(f"`{targetlang}` isn't a valid language.")
        json.dump(f, open("serverdefaults.json", "w"))


langcodes, langcodesapp, langnames, langregions = [], [], [], []

for a, b, c in os.walk(DATA_DIR): # Gives a list of language codes, so i can search in them
    for i in c:
        langcodes.append(i.split(".")[0].lower())
        langnames.append(open_json(i)["language.name"].lower())
        langcodesapp.append(open_json(i)["language.code"].lower())
        langregions.append(open_json(i)["language.region"].lower())
    break

bot.start()
