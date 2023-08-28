import interactions
import cogs.variables as var

SCOPES = var.SCOPES


class HelpCMD(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client

    @interactions.slash_command(
        name="help",
        description="DIsplays help for the bot",
        scopes=SCOPES,
    )
    @interactions.slash_option(
        name="section",
        description="The command to show more information on.",
        opt_type=interactions.OptionType.STRING,
        required=False,
        choices=[
            interactions.SlashCommandChoice(name="settings", value="settings"),
            interactions.SlashCommandChoice(name="crowdin", value="crowdin"),
            interactions.SlashCommandChoice(name="translate", value="translate"),
            interactions.SlashCommandChoice(name="credits", value="credits"),
        ],
    )
    async def _help(self, ctx: interactions.SlashContext, section: str = None):
        if section == "settings":
            await ctx.send(
                embeds=interactions.Embed(
                    title="Minecraft Translator Bot's help",
                    fields=[
                        interactions.EmbedField(
                            name="/settings",
                            value="Allows you to change some of the bot's settings for the current server.",
                            inline=True,
                        ),
                        interactions.EmbedField(
                            name=f"{ var.HOOK}   /settings server targetlang **<edition>** **<language>**",
                            value="Sets the default target language for `/translate` to use in this guild when none is specified.",
                        ),
                        interactions.EmbedField(
                            name=f"{ var.HOOK}   /settings server edition **<edition>**",
                            value="Sets the default edition for `/translate` in this guild to use when none is specified. Can be `java` or `bedrock`.",
                        ),
                    ],
                    thumbnail=interactions.EmbedAttachment(
                        url="https://cdn.discordapp.com/icons/906169345007304724/abb4f8f7659b9e790d4f02d24a500a37"
                    ),
                    color=0x10F20F,
                )
            )

        elif section == "crowdin":
            await ctx.send(
                embeds=interactions.Embed(
                    title="Minecraft Translator Bot's help",
                    fields=[
                        interactions.EmbedField(
                            name="/crowdin profile **<username>**",
                            value="Generates a Crowdin link for someone's profile if it exists.",
                            inline=True,
                        ),
                        interactions.EmbedField(
                            name="/crowdin search **<string>**",
                            value="Generates a Crowdin link to search for a string in the Minecraft project.",
                            inline=True,
                        ),
                    ],
                    thumbnail=interactions.EmbedAttachment(
                        url="https://cdn.discordapp.com/avatars/913119714400677899/3eec5517806481c6165eaddf1e438f33.png"
                    ),
                    color=0x10F20F,
                )
            )

        elif section == "translate":
            await ctx.send(
                embeds=interactions.Embed(
                    title="Minecraft Translator Bot's help",
                    fields=[
                        interactions.EmbedField(
                            name="/translate **<query>** **[target]** **[source]** **[edition]**",
                            value="Searches through the current Minecraft translations, currently present in the game's files, and returns a list of matches.",
                        ),
                        interactions.EmbedField(
                            name=f"{ var.HOOK}   **<query>**",
                            value="Specifies what to search for. To search for context (ex. 'block.minecraft.dirt') enter `key` as the language.",
                        ),
                        interactions.EmbedField(
                            name=f"{ var.HOOK}   **[target]**",
                            value="Specifies the language that your `<query>` will be translated **to**. Takes in a language code, name or region of said language.",
                        ),
                        interactions.EmbedField(
                            name=f"{ var.HOOK}   **[source]**",
                            value="Specifies the language that your `<query>` will be translated **from**. Takes in a language code, name or region of said language.",
                        ),
                        interactions.EmbedField(
                            name=f"{ var.HOOK}   **[edition]**",
                            value="Specifies the Minecraft edition your `<query>` will be searched in.",
                        ),
                        interactions.EmbedField(
                            name=f"{ var.HOOK}   **[page]**",
                            value="Specifies the page of results shown. Defaults to `1`.",
                        ),
                    ],
                    color=0x10F20F,
                    thumbnail=interactions.EmbedAttachment(
                        url="https://cdn.discordapp.com/icons/906169345007304724/abb4f8f7659b9e790d4f02d24a500a37"
                    ),
                )
            )
        elif section == "credits":
            await ctx.send(
                embeds=interactions.Embed(
                    title="Minecraft Translator Bot's credits",
                    fields=[
                        interactions.EmbedField(
                            name="Developers",
                            value=f"{var.HOOK}   <:flag_fr:1007929012804386816><@668349394529157131>,\n{var.HOOK}   <:flag_sk:1007930291488292885><@275248043828314112>",
                        ),
                        interactions.EmbedField(
                            name="Former Developers",
                            value=f"{var.HOOK}   <:flag_es:1007929300600758345><@452954731162238987>",
                        ),
                        interactions.EmbedField(
                            name="Minecraft versions",
                            value=f"{var.HOOK}   **Java Edition:** 1.20,\n{var.HOOK}   **Bedrock Edition:** 1.20.0",
                        ),
                        interactions.EmbedField(
                            name="Java Edition translations",
                            value="The amazing Minecraft Translators community!",
                        ),
                        interactions.EmbedField(
                            name="Have a question? Found a bug? Want to help?",
                            value="[Join our Discord server!](https://discord.gg/t8dtssPmK2)"
                        )
                    ],
                    color=0x10F20F,
                    thumbnail=interactions.EmbedAttachment(
                        url="https://cdn.discordapp.com/icons/906169345007304724/abb4f8f7659b9e790d4f02d24a500a37"
                    ),
                )
            )
        else:
            await ctx.send(
                embeds=interactions.Embed(
                    title="List of commands",
                    fields=[
                        interactions.EmbedField(
                            name="/translate",
                            value="Searches for a Minecraft translation from a given language to a given language in a given edition.",
                        ),
                        interactions.EmbedField(
                            name="/settings",
                            value="Changes the bot settings.",
                        ),
                        interactions.EmbedField(
                            name="/crowdin",
                            value="Searches for something on Crowdin.",
                        ),
                    ],
                    color=0x10F20F,
                    thumbnail=interactions.EmbedAttachment(
                        url="https://cdn.discordapp.com/icons/906169345007304724/abb4f8f7659b9e790d4f02d24a500a37"
                    ),
                )
            )
