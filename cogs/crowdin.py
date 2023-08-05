"""Imports Discord's interactions lib & HTTP requests"""
import interactions
import requests
import cogs.variables as var

SCOPES = var.SCOPES


class CrowdinCMD(interactions.Extension):
    """Commands linked to the Crowdin website"""

    def __init__(self, client) -> None:
        self.client = client

    @interactions.slash_command(
        sub_cmd_name="search",
        sub_cmd_description="Returns a link to a search in the Minecraft: Java Edition Crowdin project.",
        scopes=SCOPES,
        name="crowdin",
        description="Command used to query Crowdin.",
    )
    @interactions.slash_option(
        name="search",
        description="String or key to search for.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def _crowdin(self, ctx: interactions.SlashContext, search: str):
        await ctx.send(
            f"https://crowdin.com/translate/minecraft/all?filter=basic&value=0#q={search.replace(' ', '%20')}"
        )

    @_crowdin.subcommand(
        sub_cmd_name="profile",
        sub_cmd_description="Returns the link to a Crowdin profile if that profile exists.",
    )
    @interactions.slash_option(
        name="nick",
        description="User nickname.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def _profile(self, ctx: interactions.SlashContext, nick: str):
        res = requests.get(f"https://crowdin.com/profile/{nick}", timeout=30)
        if res.status_code == 200:
            await ctx.send(f"https://crowdin.com/profile/{nick}")
        elif res.status_code == 404:
            await ctx.send("This user doesn't exist", ephemeral=True)
        else:
            await ctx.send(f"A {res.status_code} error occured.", ephemeral=True)
