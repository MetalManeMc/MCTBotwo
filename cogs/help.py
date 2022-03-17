import interactions
SCOPES = []


class HelpCMD(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client
    @interactions.extension_command(
        name="help",
        description="Shows a help command with some information about the bot and its usage.",
        scope=SCOPES,
    )
    async def _help(self, ctx: interactions.CommandContext):
        hook = '<:bighook:937813704316158072>'
        await ctx.send(embeds = interactions.Embed(
            title="Minecraft Translator Bot's help",
            fields=[interactions.EmbedField(name='/settings',value="Allows you to change some of the bot's settings for the current server.", inline=True)._json,
                    interactions.EmbedField(name=f'{hook}   /settings default-target-language **<language>**', value="Sets the default target language for `/translate` to use when none is specified.")._json,
                    interactions.EmbedField(name=f'{hook}   /settings default-edition **<edition>**', value="Sets the default edition for `/translate` to use when none is specified. Can be `java` or `bedrock`.")._json,
                    interactions.EmbedField(name='/profile **<username>**', value="Generates a Crowdin link for someone's profile if it exists.", inline=True)._json,
                    interactions.EmbedField(name='/search **<string>**', value="Generates a Crowdin link to search for a string in the Minecraft project.", inline=True)._json,
                    interactions.EmbedField(name='/translate **<query>** **[target]** **[source]** **[edition]**', value="Searches through the current Miencraft translations, currently present in the game's files, and returns a list of matches.")._json,
                    interactions.EmbedField(name=f'{hook}   **<query>**', value="Specifies what to search for. To search for context (ex. 'block.minecraft.dirt') enter `key` as the language.")._json,
                    interactions.EmbedField(name=f'{hook}   **[target]**', value="Specifies the language that your `<query>` will be translated **to**. Takes in a language code, name or region of said language.")._json,
                    interactions.EmbedField(name=f'{hook}   **[source]**', value="Specifies the language that your `<query>` will be translated **from**. Takes in a language code, name or region of said language.")._json,
                    interactions.EmbedField(name=f'{hook}   **[edition]**', value="Specifies the Minecraft edition your <query> will be searched in.")._json],
            thumbnail=interactions.EmbedImageStruct(url="https://cdn.discordapp.com/icons/906169345007304724/abb4f8f7659b9e790d4f02d24a500a37")._json,
            color=0x3180F0
        ))


def setup(bot):
    HelpCMD(bot)
