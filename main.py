import json
from pathlib import Path
import interactions as di
from interactions.api.events import Startup, Component
from cogs.variables import *
from cogs.translatefuncs import *

if BETA == True:
    TOKEN_PATH = Path(PATH, "token.txt")
    print("Running BETA version")
else:
    TOKEN_PATH = Path(PATH, "token-main.txt")
    print("Running hosted version")

with open(TOKEN_PATH) as f:
    TOKEN = f.read()
"""
We craft a path towards the /lang/ folder using the host's information. 
This path is absolute and independent of the OS in which it may be running.
DATA_DIR should *not* be altered at any point.
"""
bot = di.Client(token=TOKEN, auto_defer=True)

HOOK = "<:bighook:937813704316158072>"


@di.listen()
async def on_ready(event: Startup):
    if BETA:
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
            open("loadedmessages.json", "w"),
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
)  ##, autocomplete=true
@di.slash_option(
    name="source",
    description="Language code, name or region or 'key' to translate from.",
    required=False,
    opt_type=di.OptionType.STRING,
)  ##, autocomplete=true
@di.slash_option(
    name="edition",
    description="Java or Bedrock Edition translation?",
    required=False,
    opt_type=di.OptionType.STRING,
    choices=[
        di.SlashCommandChoice(name="java", value="java"),
        di.SlashCommandChoice(name="bedrock", value="bedrock"),
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
    hidden = False
    try:
        if target is None:
            try:
                target = fetch_default(str(ctx.guild_id), "server", "targetlang")
            except:
                target = "en_us"
        if edition is None:
            try:
                edition = fetch_default(str(ctx.guild_id), "server", "edition")
            except:
                edition = "java"
        edition = edition.lower()
        target = target
        source = source
        found = find_translation(search, target, source, edition, page)
        list_message = found[0]
        exact = found[1]
        buttons = found[2]
        npages = found[3]
        pagenum = found[4]
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
                footer=di.EmbedFooter(text=f"Page {pagenum}/{npages}", icon_url=avatar),
                color=0x10F20F,
            )
            hide = False
        else:
            targetcode = lang(target, edition).replace("_", "")
            raise embederr(
                "Couldn't find the translation",
                f"https://crowdin.com/translate/minecraft/all/enus-{targetcode}?filter=basic&value=0#q={search.replace(' ', '%20')}",
                color=0xFF7F00,
                description="Click the title to search in Crowdin.",
            )
    except embederr as err:
        """if BETA==True:
            raise err
        else:"""
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
            # rem_message=await di.get(bot, di.Message, object_id=i[0], parent_id=i[1])
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


"""
@bot.autocomplete("translate", "target")
async def autocomplete(ctx: di.SlashContext, user_input: str = ""):
    return await lang_autocomplete(ctx, user_input)
@bot.autocomplete("translate", "source")
async def autocomplete(ctx: di.SlashContext, user_input: str = ""):
    return await lang_autocomplete(ctx, user_input)
"""



@di.component_callback("prevpage")
async def prevpage(ctx: di.ComponentContext):
    embed=ctx.message.embeds[0]
    msg=json.load(open("loadedmessages.json"))[str(ctx.message.id)]
    #print(embed, ctx.message.id)
    pagenum=get_pagenum(embed, "-")
    if pagenum[0] is None:
        pass
    else:
        found=find_translation(msg[0], msg[1], msg[2], msg[3], pagenum[0])
        newtext="\n".join(found[0])
        newfooter=f"Page {str(pagenum[0])}/{str(pagenum[1])}"
        embed=di.Embed(
            title=embed.title,
            fields=[di.EmbedField(name="Close matches:",value=newtext)],
            url=embed.url,
            footer=di.EmbedFooter(text=newfooter, icon_url=avatar)
            ,
            color=0x10F20F
            )
    await ctx.edit_origin(embeds=embed)

@di.component_callback("nextpage")
async def nextpage(ctx: di.SlashContext):
    embed=ctx.message.embeds[0]
    msg=json.load(open("loadedmessages.json"))[str(ctx.message.id)]
    #print(embed, ctx.message.id)
    pagenum=get_pagenum(embed, "+")
    if pagenum[0] is None:
        pass
    else:
        found=find_translation(msg[0], msg[1], msg[2], msg[3], pagenum[0])
        newtext="\n".join(found[0])
        newfooter=f"Page {str(pagenum[0])}/{str(pagenum[1])}"
        embed=di.Embed(
            title=embed.title,
            fields=[di.EmbedField(name="Close matches:",value=newtext)],
            url=embed.url,
            footer=di.EmbedFooter(text=newfooter, icon_url=avatar),
            color=0x10F20F
            )
    await ctx.edit_origin(embeds=embed)


"""
@di.slash_command(name="settings", description="Bot settings", scopes=SCOPES, default_member_permissions=di.Permissions.ADMINISTRATOR, options=[
        di.slash_option(
            name="default-target-language",
            description="Sets the default server target language",
            type=di.OptionType.SUB_COMMAND,
            options=[
                di.slash_option(
                    name="targetlang",
                    description="The target language",
                    type = di.OptionType.STRING,
                    required=True,
                    autocomplete=True),
                    ]),
        di.slash_option(
            name="default-edition",
            description="Sets the default edition to translate to",
            type=di.OptionType.SUB_COMMAND,
            options=[
                di.slash_option(
                    name="edition",
                    description="Java or Bedrock edition?",
                    type = di.OptionType.STRING,
                    required=True,
                    choices=[
                        di.Choice(name="java", value="java"),
                        di.Choice(name="bedrock", value="bedrock")
                        ])])])
async def settings(ctx:di.SlashContext, sub_command, targetlang=None, edition=None):
    f=json.load(open(Path(PATH,"serverdefaults.json")))
    hide=False
    if sub_command=="default-target-language":
        try:
            currentlang=f[str(ctx.guild_id)]["server"]["targetlang"]
            try:
                f[str(ctx.guild_id)]["server"]["targetlang"]=lang(targetlang,"java")
                embed=di.Embed(title=f"Default target language set to `{find_translation('language.name',lang(targetlang,'java'),'key','java')[1]+', '+find_translation('language.region',lang(targetlang,'java'),'key','java')[1]}`.",color=0x10F20F)
            except embederr as e:
                e.desc=f"Default target language reset to `{find_translation('language.name',lang(currentlang,'java'),'key','java')[1]+', '+find_translation('language.region',lang(currentlang,'java'),'key','java')[1]}`."
                raise e
        except embederr as e:
            embed=di.Embed(
                title=e.title,
                thumbnail=e.image,
                url=e.url,
                fields=e.field,
                color=e.color,
                description=e.desc
                )
            hide=e.hidden
        except Exception as ex:
            hide=True
            embed=di.Embed(title="Something happened",color=0xff0000,thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg"))
    elif sub_command=="default-edition":
        edition=edition.lower()
        try:
            currentedition=f[str(ctx.guild_id)]["server"]["edition"]
            if edition=="java" or edition=="bedrock":
                f[str(ctx.guild_id)]["server"]["edition"]=edition
                embed=di.Embed(title=f"Default edition changed to `{edition}`.",color=0x10F20F)
            else:
                raise embederr("Edition not found",description=f"Default edition reset to `{currentedition}`.")
        except embederr as e:
            embed=di.Embed(
                title=e.title,
                thumbnail=e.image,
                url=e.url,
                fields=e.field,
                color=e.color,
                description=e.desc
                )
            hide=e.hidden
        except Exception as ex:
            hide=True
            embed=di.Embed(title="Something happened",color=0xff0000,thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg"))
    try:
        await ctx.send(embeds=embed,ephemeral=hide)
    except Exception as exc:
        if BETA==True:
            raise exc
        else:
            await ctx.send(embeds=di.Embed(title="Something happened while sending message",color=0xff0000,thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg")),ephemeral=True)
    json.dump(f, open("serverdefaults.json", "w"))
@bot.autocomplete("settings", "targetlang")
async def autocomplete(ctx: di.SlashContext, user_input: str = ""):
    return await lang_autocomplete(ctx, user_input)
"""
for cog in COGS:
    if cog not in ("variables", "translatefuncs", "help"):
        bot.load_extension("cogs." + cog)

bot.start()
