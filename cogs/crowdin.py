import interactions, requests
import cogs.variables as var

SCOPES = var.SCOPES


class CrowdinCMD(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client
    @interactions.extension_command(
        name="search",
        description="Returns a link to a search in the Minecraft: Java Edition Crowdin project.",
        scope=SCOPES,
        options = [
                interactions.Option(
                    name = "search",
                    description = "String or key to search for.",
                    type = interactions.OptionType.STRING,
                    required = True
                )
            ]
    )
    async def _search(self, ctx: interactions.CommandContext, search: str):
        await ctx.send(f"https://crowdin.com/translate/minecraft/all?filter=basic&value=0#q={search.replace(' ', '%20')}")

    @interactions.extension_command(
        name="profile",
        description="Returns the link to a Crowdin profile if that profile exists.",
        scope=SCOPES,
        options = [
                interactions.Option(
                    name = "nick",
                    description = "String or key to search for.",
                    type = interactions.OptionType.STRING,
                    required = True
                )
            ]
    )
    async def _profile(self, ctx: interactions.CommandContext, nick: str):
        re=requests.get(f"https://crowdin.com/profile/{nick}")
        if re.status_code==200:
            await ctx.send(f"https://crowdin.com/profile/{nick}")
        elif re.status_code==404:
            await ctx.send("This user doesn't exist", ephemeral=True)
        else:
            await ctx.send(f"A {re.status_code} error occured.", ephemeral=True)

def setup(bot):
    CrowdinCMD(bot)