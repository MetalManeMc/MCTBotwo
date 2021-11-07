import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = discord.Client(intents = discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [906169345007304724]


@slash.slash(name = "translate",
             description = "Translates a Minecraft string from a language to another.",
             guild_ids = guild_ids
             options = [
                 create_option(
                     name = "string",
                     description = "The string or key to translate.",
                     option_type = 3,
                     required = True
                 ),
                 create_option(
                     name = "target",
                     description = "Code of the language, in which the string is going to be sent.",
                     option_type = 3,
                     required = True
                 ),
                 create_option(
                     name = "sourcelang",
                     description = "Code of the language, in which you wrote the string. (English is default)",
                     option_type = 3,
                     required = False
                 )
             ]
            )
async def translate(ctx, string, target,  sourcelang = "en_us"):
    await ctx.send(content = f"{string}, {sourcelang}, {target}")

client.run(open("token.txt").read())
