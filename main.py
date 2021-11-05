import discord
from discord_slash import SlashCommand, create_option


@slash.slash(name="translate",
             description="Translates a Minecraft string from a language to another.",
             options=[
                 create_option(
                     name="sourcelang",
                     description="Source language code. Will be the translation key if not defined",
                     option_type=3,
                     required=False),
                 create_option(
                     name="string",
                     description="The string to translate",
                     option_type=3,
                     required=True),
                 create_option(
                     name="target",
                     description="Source language code. Will be the translation key if not defined",
                     option_type=3,
                     required=False)])
async def translate(ctx, sourcelang="key"):
    await ctx.send(content=sourcelang)
