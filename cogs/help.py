import interactions
import cogs.variables as var

SCOPES = var.SCOPES


class HelpCMD(interactions.Extension):
    
    def __init__(self, client) -> None:
        self.client = client
    
    @interactions.extension_command(
        name="help",
        description="Funnily enough, this text never shows up in Discord's UI. Kudos to anyone who finds this!",
        scope = SCOPES,
        options=[
            interactions.Option(
                name="settings",
                description="Shows more information about the bot's settings",
                type=interactions.OptionType.SUB_COMMAND,
                options=[]
            ),
            interactions.Option(
                name="crowdin",
                description="Shows more information about Crowdin-related commands",
                type=interactions.OptionType.SUB_COMMAND,
                options=[]
            ),
            interactions.Option(
                name="translate",
                description="Shows more information about the /translate command",
                type=interactions.OptionType.SUB_COMMAND,
                options=[]
            )
        ]
    )
    async def _help(self, ctx: interactions.CommandContext, sub_command: str = None):
        if not sub_command: sub_command = ctx.data.options[0].name # Without this line, the whole thing wouldn't work at all. Shoutout to Joe and Dworv <3
        hook = "<:bighook:937813704316158072>"
        if sub_command == "settings":
            await ctx.send(embeds = interactions.Embed(
            title="Minecraft Translator Bot's help",
            fields=[interactions.EmbedField(name="/settings",value="Allows you to change some of the bot's settings for the current server.", inline=True)._json,
                    interactions.EmbedField(name=f"{hook}   /settings default-target-language **<language>**", value="Sets the default target language for `/translate` to use when none is specified.")._json,
                    interactions.EmbedField(name=f"{hook}   /settings default-edition **<edition>**", value="Sets the default edition for `/translate` to use when none is specified. Can be `java` or `bedrock`.")._json,
                    ],
            thumbnail=interactions.EmbedImageStruct(url="https://cdn.discordapp.com/icons/906169345007304724/abb4f8f7659b9e790d4f02d24a500a37")._json,
            color=0x3180F0
            ))
            
        elif sub_command == "crowdin":
            await ctx.send(embeds = interactions.Embed(
            title="Minecraft Translator Bot's help",
            fields=[
                interactions.EmbedField(name="/profile **<username>**", value="Generates a Crowdin link for someone's profile if it exists.", inline=True),
                interactions.EmbedField(name="/search **<string>**", value="Generates a Crowdin link to search for a string in the Minecraft project.", inline=True),
            ],
            thumbnail=interactions.EmbedImageStruct(url="https://cdn.discordapp.com/avatars/913119714400677899/3eec5517806481c6165eaddf1e438f33.png")._json,
            color=0x3180F0))

        elif sub_command == "translate":
            await ctx.send(embeds = interactions.Embed(
                    fields = [
                    interactions.EmbedField(name="/translate **<query>** **[target]** **[source]** **[edition]**", value="Searches through the current Miencraft translations, currently present in the game's files, and returns a list of matches.")._json,
                    interactions.EmbedField(name=f"{hook}   **<query>**", value="Specifies what to search for. To search for context (ex. 'block.minecraft.dirt') enter `key` as the language.")._json,
                    interactions.EmbedField(name=f"{hook}   **[target]**", value="Specifies the language that your `<query>` will be translated **to**. Takes in a language code, name or region of said language.")._json,
                    interactions.EmbedField(name=f"{hook}   **[source]**", value="Specifies the language that your `<query>` will be translated **from**. Takes in a language code, name or region of said language.")._json,
                    interactions.EmbedField(name=f"{hook}   **[edition]**", value="Specifies the Minecraft edition your <query> will be searched in.")._json],
                    color=0x3180F0,
                    thumbnail=interactions.EmbedImageStruct(url="https://cdn.discordapp.com/icons/906169345007304724/abb4f8f7659b9e790d4f02d24a500a37")._json))
        


                    
def setup(bot):
    HelpCMD(bot)
