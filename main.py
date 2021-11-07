import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = discord.Client(intents = discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [906169345007304724]


@slash.slash(name = "translate",
             description = "Translates a Minecraft string from a language to another.",
             options = [
                 create_option(
                     name = "string",
                     description = "The string or key to translate",
                     option_type = 3,
                     required = True
                 ),
                 create_option(
                     name = "sourcelang",
                     description = "Source language code. Will be the translation key if not defined",
                     option_type = 3,
                     required = False
                 ),
                 create_option(
                     name = "target",
                     description = "Target language code. Will be the translation key if not defined",
                     option_type = 3,
                     required = False
                 )
             ],
             guild_ids = guild_ids
            )
async def translate(ctx, string,  sourcelang="key", target="key"):
    await ctx.send(content = f"{string}, {sourcelang}, {target}")

client.run(open("token.txt").read())
