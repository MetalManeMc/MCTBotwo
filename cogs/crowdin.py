import interactions
import requests
import cogs.variables as var

SCOPES = var.SCOPES


class CrowdinCMD(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client

    @interactions.slash_command(
        name="search",
        description="Returns a link to a search in the Minecraft: Java Edition Crowdin project.",
        scopes=SCOPES
    )
    @interactions.slash_option(
        name="search",
        description="String or key to search for.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    async def _search(self, ctx: interactions.SlashContext, search: str):
        await ctx.send(
            f"https://crowdin.com/translate/minecraft/all?filter=basic&value=0#q={search.replace(' ', '%20')}"
        )

    @interactions.slash_command(
        name="profile",
        description="Returns the link to a Crowdin profile if that profile exists.",
        scopes=SCOPES)
    @interactions.slash_option(
        name="snick",
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
