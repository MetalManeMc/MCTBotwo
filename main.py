import json
import os
from pathlib import Path
import interactions as di
import requests
from random import choice

PATH = Path(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = Path(PATH, 'lang')
JAVA_DIR=Path(DATA_DIR, 'java')
BEDROCK_DIR=Path(DATA_DIR, 'bedrock')

Footers="See /help for more info.","The blue text will be an exact match, if one is found.", "This is NOT a machine translation (except maybe if you used the Bedrock translations)."

if "\\" in str(DATA_DIR): beta=True
else: beta=False

if beta==True:
    TOKEN_PATH = Path(PATH, 'token.txt')
    SCOPES = [906169345007304724]
else:
    TOKEN_PATH = Path(PATH, 'token-main.txt')
    SCOPES=[]
    print("Running hosted version")

with open(TOKEN_PATH) as f:
    TOKEN = f.read()

"""
We craft a path towards the /lang/ folder using the host's information. 
This path is absolute and independent of the OS in which it may be running.
DATA_DIR should *not* be altered at any point.
"""

bot = di.Client(token=TOKEN, log_level=31)
hook = '<:bighook:937813704316158072>'

@bot.event
async def on_ready():
    print("Online!")
    print(f"Path towards //lang// is {DATA_DIR}")

############################################################################
#                             Code starts here                             #
############################################################################

class embederr(Exception):
    def __init__(c, title=None, url=None, hidden=True, color=0xff0000, description=None, hasfield=False, field=["name","value"], hasimage=True, image="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg") -> None:
        c.title=title
        c.url=url
        c.hidden=hidden
        c.color=color
        c.desc=description
        if hasimage:
            c.image=di.EmbedImageStruct(url=image)._json
        else:c.image=None
        if hasfield:
            c.field=[di.EmbedField(name=field[0],value=field[1])._json]
        else:c.field=None


def open_json(jsonfile, edition="java"): 

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
    if edition=="java":
        json_path = Path(JAVA_DIR, jsonfile).with_suffix(".json")
    elif edition=="bedrock":
        json_path = Path(BEDROCK_DIR, jsonfile).with_suffix(".json")
    with open(json_path, encoding='utf-8') as js:
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

def find_translation(string:str, targetlang:str, sourcelang:str, edition):

    """
    This function finds translations and returns the list of matches.
    """

    string = string.lower()
    # we can put something like find(languages) for user to be able to insert uncomplete languages
    try:
        if targetlang!="key": # if either are key, they should not be searched for as files, instead use jsdef
            jstarget = open_json(lang(targetlang, edition), edition)
        if sourcelang!="key":
            jssource = open_json(lang(sourcelang, edition), edition)
        jsdef = open_json("en_us") # this will get used everytime to key or from key is used... (json default... change the name if you want)
    except IndexError:
        return

    exact=None
    if targetlang=="key": # figures out, which mode to use
        if sourcelang=="key":
            result = complete(string, jsdef) #ktk
        else:
            result = [i for i in jsdef if string in jssource[i].lower()] #stk
            for i in result:
                if jssource[i].lower()==string:
                    exact=i
                    break
    else:
        if sourcelang=="key":
            result = [jstarget[i] for i in complete(string, jsdef)] #kts
            try: exact=jstarget[string]
            except: pass
        else:
            result = [jstarget[i] for i in [i for i in jssource if string in jssource[i].lower()]] #sts(string, jstarget, jssource)
            for i in jssource:
                if jssource[i].lower()==string:
                    exact=jstarget[i]
                    break
    if len(result)>10:
        del result[10:]
        result.append("**…and more!**")
    return result,exact

def lang(search:str, edition):

    '''
    Returns a complete internal language code to be used for file opening.
    Input can be the expected output too.
    Input can be approved language code, name, region or internal code (searching in this order)
    '''

    search = search.lower()
    if edition=="java":
        for i in range(len(langcodesapp)): # We can't use complete here because we would have no clue which langcode to use. The thing we need is index of langcode, not completed langname or whatever.
            if search in langcodesapp[i].lower():
                return langcodes[i]
        for i in range(len(langnames)):
            if search in langnames[i].lower():
                return langcodes[i]
        for i in range(len(langregions)):
            if search in langregions[i].lower():
                return langcodes[i]
    elif edition=="bedrock":
        for i in range(len(belangcodes)): # We can't use complete here because we would have no clue which langcode to use. The thing we need is index of langcode, not completed langname or whatever.
            if search in belangcodes[i].lower():
                return belangcodes[i]
        for i in range(len(belangnames)):
            if search in belangnames[i].lower():
                return belangcodes[i]
        for i in range(len(belangregions)):
            if search in belangregions[i].lower():
                return belangcodes[i]

    ret=complete(search, langcodes)
    if len(ret)>0:
        return ret[0]
    else:
        raise embederr("Language not found")


###########
#Translate#
###########

""",
                    choices=[
                        di.Choice(
                            name = "Java Edition",
                            value ="java"
                        ),
                        di.Choice(
                            name = "Bedrock Edition",
                            value="bedrock"
                        )
                    ]"""

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
                ),
                di.Option(
                    name = "edition",
                    description = "Java or Bedrock Edition translation?",
                    type = di.OptionType.STRING,
                    required = False
                )
            ])
async def translate(ctx: di.CommandContext, search: str, target=None, source="en_us", edition=None):
    try:
        if target == None:
            try:
                target = fetch_default(str(ctx.guild_id), "server", "targetlang")
            except:
                target="en_us"
        if edition == None:
             try:
                 edition = fetch_default(str(ctx.guild_id), "server", "edition")
             except:
                 edition="java"
        edition=edition.lower()
        found=find_translation(search, target, source, edition)
        list_message = found[0]
        exact = found[1]

        if len(list_message)>0:
            if exact == None:
                message = '\n'.join(list_message)
                title = "No perfect matches"
                embedfields = [di.EmbedField(name="Close matches:",value=message)._json]
            else:
                list_message.remove(exact)
                message = '\n'.join(list_message)
                title = exact
                if len(list_message) == 0:
                    embedfields = []
                else:
                    embedfields = [di.EmbedField(name="Close matches:",value=message)._json]
            if edition=="java":
                url=f"https://crowdin.com/translate/minecraft/all/enus-{target}?filter=basic&value=0#q={search.replace(' ', '%20')}"
            elif edition=="bedrock":
                url=None
            embed=di.Embed(
                title=title,
                fields=embedfields,
                url=url,
                footer=di.EmbedFooter(text=choice(Footers), icon_url="https://cdn.discordapp.com/avatars/906169526259957810/d3d26f58da5eeec0d9c133da7b5d13fe.webp?size=128")._json,
                color=0x3180F0)
            hide=False
        else:
            raise embederr(
                "Couldn't find the translation",
                f"https://crowdin.com/translate/minecraft/all/enus-{target}?filter=basic&value=0#q={search.replace(' ', '%20')}",
                color=0xff7f00,
                description="Click the title to search in Crowdin.")
    except embederr as e: # This is where it returns when there was an error in the code or user made a mistake
        embed=di.Embed(
            title=e.title,
            thumbnail=e.image,
            url=e.url,
            fields=e.field,
            color=e.color,
            description=e.desc
            )
        hide=e.hidden
    except Exception:
        embed=di.Embed(title="Something happened",thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg")._json)
    try:
        await ctx.send(embeds=embed,ephemeral=hide)
    except:
        await ctx.send(embeds=di.Embed(title="Something happened while sending message",thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg")._json))


@bot.command(name = "search",
             description = "Returns a link to a search in the Minecraft: Java Edition Crowdin project.",
             scope=SCOPES,
             options = [
                di.Option(
                    name = "search",
                    description = "String or key to search for.",
                    type = di.OptionType.STRING,
                    required = True
                )
            ])
async def search(ctx:di.CommandContext, search: str):
    await ctx.send(f"https://crowdin.com/translate/minecraft/all?filter=basic&value=0#q={search.replace(' ', '%20')}")


@bot.command(name = "profile",
             description = "Returns a link for a Crowdin profile if it exists.",
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
            description="Sets the default server target language",
            type=di.OptionType.SUB_COMMAND,
            options=[
                di.Option(
                    name="targetlang",
                    description="The target language",
                    type = di.OptionType.STRING,
                    required=True),
                    ]),
        di.Option(
            name="default-edition",
            description="Sets the default edition to translate to",
            type=di.OptionType.SUB_COMMAND,
            options=[
                di.Option(
                    name="edition",
                    description="Java or Bedrock edition?",
                    type = di.OptionType.STRING,
                    required=True),
                    ])])
async def settings(ctx:di.CommandContext, sub_command, targetlang=None, edition=None):
    f=json.load(open(Path(PATH,"serverdefaults.json")))
    if sub_command=="default-target-language":
        try:
            currentlang=f[str(ctx.guild_id)]["server"]["targetlang"]
            if targetlang in langcodes or targetlang in langnames:
                f[str(ctx.guild_id)]["server"]["targetlang"]=targetlang
                await ctx.send(f"Default target language changed to `{targetlang}`.")
            else:
                await ctx.send(f"`{targetlang}` isn't a valid language. Default target language reset to `{currentlang}`.")
        except KeyError:
            if targetlang in langcodes or targetlang in langnames:
                f[str(ctx.guild_id)]["server"].update({"targetlang": targetlang})
                await ctx.send(f"Default target language set to `{targetlang}`.")
            else:
                await ctx.send(f"`{targetlang}` isn't a valid language.")
    elif sub_command=="default-edition":
        edition=edition.lower()
        try:
            currentedition=f[str(ctx.guild_id)]["server"]["edition"]
            if edition=="java" or edition=="bedrock":
                f[str(ctx.guild_id)]["server"]["edition"]=edition
                await ctx.send(f"Default edition changed to `{edition}`.")
            else:
                await ctx.send(f"`{edition}` isn't a valid edition. Default edition reset to `{currentedition}`.")
        except KeyError:
            if edition=="java" or edition=="bedrock":
                f[str(ctx.guild_id)]["server"].update({"edition": edition})
                await ctx.send(f"Default edition set to `{edition}`.")
            else:
                await ctx.send(f"`{edition}` isn't a valid edition.")
    json.dump(f, open("serverdefaults.json", "w"))


@bot.command(name='help', description='Shows a help command with some information about the bot and its usage.', scope=SCOPES)
async def help(ctx: di.CommandContext):
        await ctx.send(embeds = di.Embed(
            title="Minecraft Translator Bot's help",
            fields=[di.EmbedField(name='/settings',value="Allows you to change some of the bot's settings for the current server.", inline=True)._json,
                    di.EmbedField(name=f'{hook}   /settings default-target-language **<language>**', value="Sets the default target language for `/translate` to use when none is specified.")._json,
                    di.EmbedField(name=f'{hook}   /settings default-edition **<edition>**', value="Sets the default edition for `/translate` to use when none is specified. Can be `java` or `bedrock`.")._json,
                    di.EmbedField(name='/profile **<username>**', value="Generates a Crowdin link for someone's profile if it exists.", inline=True)._json,
                    di.EmbedField(name='/search **<string>**', value="Generates a Crowdin link to search for a string in the Minecraft project.", inline=True)._json,
                    di.EmbedField(name='/translate **<query>** **[target]** **[source]** **[edition]**', value="Searches through the current Miencraft translations, currently present in the game's files, and returns a list of matches.")._json,
                    di.EmbedField(name=f'{hook}   **<query>**', value="Specifies what to search for. To search for context (ex. 'block.minecraft.dirt') enter `key` as the language.")._json,
                    di.EmbedField(name=f'{hook}   **[target]**', value="Specifies the language that your `<query>` will be translated **to**. Takes in a language code, name or region of said language.")._json,
                    di.EmbedField(name=f'{hook}   **[source]**', value="Specifies the language that your `<query>` will be translated **from**. Takes in a language code, name or region of said language.")._json,
                    di.EmbedField(name=f'{hook}   **[edition]**', value="Specifies the Minecraft edition in which your `<query>` will be translated searched for.")._json],
            thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/icons/906169345007304724/abb4f8f7659b9e790d4f02d24a500a37")._json,
            color=0x3180F0
        ))



langcodes, langcodesapp, langnames, langregions = [], [], [], []

for a, b, c in os.walk(JAVA_DIR): # Gives a list of java language codes, names and regions, so i can search in them
    for i in c:
        langcodes.append(i.split(".")[0].lower())
        langnames.append(open_json(i)["language.name"].lower())
        langcodesapp.append(open_json(i)["language.code"].lower())
        langregions.append(open_json(i)["language.region"].lower())
    break


belangcodes, belangcodesandnames, belangnames, belangregions = [], [], [], []

names=json.load(open("language_names.json", encoding="utf-8"))
for i in names:
    belangcodes.append(i[0])
    belangcodesandnames.append(i[1])
    codeandname=i[1].split(" (")
    belangnames.append(codeandname[0])
    try:
        belangregions.append(codeandname[1].replace(")", ""))
    except IndexError:
        belangregions.append(None)

bot.start()
