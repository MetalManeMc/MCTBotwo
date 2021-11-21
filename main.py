import json
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [906169345007304724]


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
                     description="The string (key) to translate.",
                     option_type=3,
                     required=True
                 ),
                 create_option(
                     name="target",
                     description="Code of the language in which the string is going to be sent. EX: es_es",
                     option_type=3,
                     required=True
                 )
             ]
             )
async def translate(ctx, target, string):
    await ctx.send(fetch_translation(target, string))

client.run(open("token.txt").read())
