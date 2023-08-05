"""
Imports Path & JSON tools
Interactions for Discord bot managment
Variable and functions for cogs
"""
import json
from pathlib import Path
import interactions as di
from interactions.api.events import Startup
from cogs.variables import PATH, BETA, DATA_DIR, COGS, SCOPES, AVATAR, belangamedict
from cogs.translatefuncs import (lang_autocomplete, fetch_default, find_translation, lang,
                                 embederr, register_comp, get_pagenum)

if BETA:
    TOKEN_PATH = Path(PATH, "token.txt")
    print("Running BETA version")
else:
    TOKEN_PATH = Path(PATH, "token-main.txt")
    print("Running hosted version")

with open(TOKEN_PATH, encoding="utf-8") as f:
    TOKEN = f.read()

# We craft a path towards the /lang/ folder using the host's information.
# This path is absolute and independent of the OS in which it may be running.
# DATA_DIR should *not* be altered at any point.

bot = di.Client(
    token=TOKEN,
    auto_defer=True,
    send_command_tracebacks=False,
)



@di.listen()
async def on_ready(event: Startup):
    """Indicated bot hes successfully established connecxion on launch"""
    if BETA:
        with open("loadedmessages.json", "w", encoding="utf-8") as file:
            json.dump(
                {
                    "0000000000000000000": [
                        "search",
                        "target",
                        "source",
                        "edition",
                        "9999999999.9999999",
                        "000000000000000000",
                    ]
                },
                file,
            )
    print("Online!")
    print(f"Path towards the lang folder is {DATA_DIR}\nCogs loaded: {COGS}")


############################################################################
#                             Code starts here                             #
############################################################################

@di.slash_command(
    name="translate",
    description="Returns the translation found in-game for a string",
    scopes=SCOPES,
)
@di.slash_option(
    name="search",
    description="String or key to translate.",
    required=True,
    opt_type=di.OptionType.STRING,
)
@di.slash_option(
    name="target",
    description="Language code, name or region or 'key' to translate to.",
    required=False,
    opt_type=di.OptionType.STRING,
    autocomplete=True,
)
@di.slash_option(
    name="source",
    description="Language code, name or region or 'key' to translate from.",
    required=False,
    opt_type=di.OptionType.STRING,
    autocomplete=True,
)
@di.slash_option(
    name="edition",
    description="Java or Bedrock Edition translation?",
    required=False,
    opt_type=di.OptionType.STRING,
    choices=[
        di.SlashCommandChoice(name="Java", value="java"),
        di.SlashCommandChoice(name="Bedrock", value="bedrock"),
    ],
)
@di.slash_option(
    name="page",
    description="Result page number.",
    required=False,
    opt_type=di.OptionType.INTEGER,
)
async def translate(
    ctx: di.SlashContext,
    search: str,
    target: str = None,
    source: str = "en_us",
    edition: str = None,
    page: int = 1,
):
    """Searches for translation of a string"""
    hidden = False
    try:
        if edition is None:
            try:
                edition = fetch_default(str(ctx.guild_id), "server", "edition")
            except KeyError:
                edition = "java"
        if target is None:
            try:
                target = fetch_default(
                    str(ctx.guild_id), "server", "targetlang", edition
                )
            except KeyError:
                target = "en_us"
        edition = edition.lower()
        list_message, exact, buttons, npages, pagenum = find_translation(
            search, target, source, edition, page
        )
        if len(list_message) > 0:
            if exact is None:
                message = "\n".join(list_message)
                title = "No perfect matches"
                embedfields = [di.EmbedField(name="Close matches:", value=message)]
            else:
                try:
                    list_message.remove(exact)
                except ValueError:
                    pass
                message = "\n".join(list_message)
                title = exact
                if len(list_message) == 0:
                    embedfields = []
                else:
                    embedfields = [di.EmbedField(name="Close matches:", value=message)]
            if edition == "java":
                try:
                    targetcode = lang(target, edition).replace("_", "")
                except embederr:
                    targetcode = "enuk"
                url = f"https://crowdin.com/translate/minecraft/all/enus-{targetcode}?filter=basic&value=0#q={search.replace(' ', '%20')}"
            elif edition == "bedrock":
                url = None
            embed = di.Embed(
                title=title,
                fields=embedfields,
                url=url,
                footer=di.EmbedFooter(text=f"Page {pagenum}/{npages}", icon_url=AVATAR),
                color=0x10F20F,
            )
        else:
            targetcode = lang(target, edition).replace("_", "")
            raise embederr(
                "Couldn't find the translation",
                f"https://crowdin.com/translate/minecraft/all/enus-{targetcode}?filter=basic&value=0#q={search.replace(' ', '%20')}",
                color=0xFF7F00,
                description="Click the title to search in Crowdin.",
            )
    except embederr as err:
        embed = di.Embed(
            title=err.title,
            thumbnail=err.image,
            url=err.url,
            fields=err.field,
            color=err.color,
            description=err.desc,
        )
        hidden = True
    except Exception as ex:
        if BETA:
            raise ex
        else:
            embed = di.Embed(
                title="Something happened",
                description=f"Error description:\n{ex}",
                thumbnail=di.EmbedAttachment(
                    url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg"
                ),
                color=0xFF0000,
            )
            hidden = True
    try:
        msg = await ctx.send(embeds=embed, ephemeral=hidden, components=buttons)
        remove = register_comp(msg.id, search, target, source, edition, msg.guild.id)
        for i in remove.items():
            rem_message = await bot.fetch_channel(i[1]).fetch_message(i[0])
            await rem_message.edit(components=None)
    except Exception as ex:
        if BETA:
            raise ex
        else:
            await ctx.send(
                embeds=di.Embed(
                    title="Something happened while sending message",
                    description=f"Error description:\n{ex}",
                    thumbnail=di.EmbedAttachment(
                        url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg"
                    ),
                    color=0xFF0000,
                ),
                ephemeral=True,
            )


@translate.autocomplete("target")
async def autocomplete(ctx: di.AutocompleteContext):
    """Autocompletes Java & Bedrock language names"""
    await ctx.send(lang_autocomplete(ctx.input_text))


@translate.autocomplete("source")
async def autocomplete_source(ctx: di.AutocompleteContext):
    """Autocompletes Java & Bedrock language names"""
    await ctx.send(lang_autocomplete(ctx.input_text))


@di.component_callback("prevpage")
async def prevpage(ctx: di.ComponentContext):
    """Reruns translate on previous page"""
    embed = ctx.message.embeds[0]
    with open("loadedmessages.json", encoding="utf-8") as file:
        msg = json.load(file)[str(ctx.message.id)]
    # print(embed, ctx.message.id)
    pagenum = get_pagenum(embed, "-")
    if pagenum[0] is None:
        pass
    else:
        found = find_translation(msg[0], msg[1], msg[2], msg[3], pagenum[0])
        newtext = "\n".join(found[0])
        newfooter = f"Page {str(pagenum[0])}/{str(pagenum[1])}"
        embed = di.Embed(
            title=embed.title,
            fields=[di.EmbedField(name="Close matches:", value=newtext)],
            url=embed.url,
            footer=di.EmbedFooter(text=newfooter, icon_url=AVATAR),
            color=0x10F20F,
        )
    await ctx.edit_origin(embeds=embed)


@di.component_callback("nextpage")
async def nextpage(ctx: di.SlashContext):
    """Reruns translate on next page"""
    embed = ctx.message.embeds[0]
    with open("loadedmessages.json", encoding="utf-8") as file:
        msg = json.load(file)[str(ctx.message.id)]
    # print(embed, ctx.message.id)
    pagenum = get_pagenum(embed, "+")
    if pagenum[0] is None:
        pass
    else:
        found = find_translation(msg[0], msg[1], msg[2], msg[3], pagenum[0])
        newtext = "\n".join(found[0])
        newfooter = f"Page {str(pagenum[0])}/{str(pagenum[1])}"
        embed = di.Embed(
            title=embed.title,
            fields=[di.EmbedField(name="Close matches:", value=newtext)],
            url=embed.url,
            footer=di.EmbedFooter(text=newfooter, icon_url=AVATAR),
            color=0x10F20F,
        )
    await ctx.edit_origin(embeds=embed)


@di.slash_command(
    name="settings",
    description="Change bot settings",
    scopes=SCOPES,
    default_member_permissions=di.Permissions.ADMINISTRATOR,
    group_name="server",
    group_description="Changes settings for the current guild.",
    sub_cmd_name="targetlang",
    sub_cmd_description="Sets the default server target language",
)
@di.slash_option(
    name="edition",
    description="The edition for which to set new defaul target language. ",
    required=True,
    opt_type=di.OptionType.STRING,
    choices=[
        di.SlashCommandChoice(name="Java", value="java"),
        di.SlashCommandChoice(name="Bedrock", value="bedrock"),
    ],
)
@di.slash_option(
    name="targetlang",
    description="The target language to set.",
    required=True,
    opt_type=di.OptionType.STRING,
)
async def settings(ctx: di.SlashContext, edition: str, targetlang: str):
    """Sets the default server target language"""
    with open(Path(PATH, "serverdefaults.json"), encoding="utf-8") as rfile:
        file = json.load(rfile)

    if str(ctx.guild_id) not in file:
        file[str(ctx.guild_id)] = {
            "server": {
                "targetlang": {"java": "en_us", "bedrock": "en_us"},
                "edition": "java",
            }
        }

    try:
        if edition == "java":
            embedtitle = f"Default target language set to `{find_translation('language.name',lang(targetlang,'java'),'key','java')[1]+', '+find_translation('language.region',lang(targetlang,'java'),'key','java')[1]}`."
        else:
            embedtitle = f"Default target language set to `{belangamedict[lang(targetlang, 'bedrock')]}`"

        embed = di.Embed(
            title=embedtitle,
            color=0x10F20F,
        )

        file[str(ctx.guild_id)]["server"]["targetlang"][edition] = lang(
            targetlang, edition
        )

    except embederr:
        embed = di.Embed(
            title=f"The language `{targetlang}` has not been found in {edition.capitalize()} Edition.",
            color=0xFF0000,
        )
    with open("serverdefaults.json", "w", encoding="utf-8") as rfile:
        json.dump(file, rfile)
    await ctx.send(embed=embed)


@settings.autocomplete("targetlang")
async def settings_autocomplete(ctx: di.AutocompleteContext):
    """Autocompletes Java & Bedrock language names"""
    await ctx.send(lang_autocomplete(ctx.input_text))


@settings.subcommand(
    group_name="server",
    group_description="Changes settings for the current guild.",
    sub_cmd_name="edition",
    sub_cmd_description="Sets the default Minecraft edition for string source.",
)
@di.slash_option(
    name="edition",
    description="The Edition from which the strings are extracted.",
    required=True,
    opt_type=di.OptionType.STRING,
    choices=[
        di.SlashCommandChoice(name="Java", value="java"),
        di.SlashCommandChoice(name="Bedrock", value="bedrock"),
    ],
)
async def settings_edition(ctx: di.SlashContext, edition=None):
    """Sets the default server target edition"""
    with open(Path(PATH, "serverdefaults.json"), encoding="utf-8") as rfile:
        file = json.load(rfile)

    if str(ctx.guild_id) not in file:
        file[str(ctx.guild_id)] = {
            "server": {
                "targetlang": {"java": "en_us", "bedrock": "en_us"},
                "edition": "java",
            }
        }

    embed = di.Embed(
        title=f"Set default target edition to {edition.capitalize()} Edition.",
        color=0x10F20F,
    )

    file[str(ctx.guild_id)]["server"]["edition"] = edition

    with open("serverdefaults.json", "w", encoding="utf-8") as rfile:
        json.dump(file, rfile)
    await ctx.send(embed=embed)


for cog in COGS:
    if cog not in ("variables", "translatefuncs"):
        bot.load_extension("cogs." + cog)

bot.start()
