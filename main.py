import json
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [906169345007304724]


def translater(string, target, source):
    source = json.load(open("lang/"+source+".json"))
    target = json.load(open("lang/"+target+".json"))
    for key in source:
        if source[key] == string:
            return target[key]
        else: #if it doesn't match perfectly, try to match with lowercase
            fallb = ""
            for i in source[key]:
                if ord("Z") >= ord(i) >= ord("A"):
                    fallb += chr(ord(i) + 32)
                else:
                    fallb += i
            if fallb == string:
                return target[key] #until here is my code
    return "Invalid string"

def fetch_translation(target, string):
    t = json.load(open(f"lang/{target}.json")) 
    key = f"{string}"
    return t.get(key)

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
                     description="Language code in which the string is going to be sent. EX: es_es",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="sourcelang",
                     description="Language code in which the string is going to be retrieved. EX: fr_fr",
                     option_type=3,
                     required=False
                 )
             ]
             )
async def translate(ctx, string, target,  sourcelang="en_us"):
    if sourcelang== "key":
        await ctx.send(fetch_translation(target, string))
    else:
        await ctx.send(translater(string, target, sourcelang))

client.run(open("token.txt").read())
