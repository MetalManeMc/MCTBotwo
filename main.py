import json
from pathlib import Path
import interactions as di
from cogs.variables import *
from cogs.translatefuncs import *

if beta==True:
    TOKEN_PATH = Path(PATH, "token.txt")
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
bot = di.Client(token=TOKEN)

hook = "<:bighook:937813704316158072>"

@bot.event
async def on_ready():
    if beta:
        json.dump({"0000000000000000000": ["search", "target", "source", "edition", "9999999999.9999999", "000000000000000000"]}, open("loadedmessages.json", "w"))
    print("Online!")
    print(f"Path towards the lang folder is {DATA_DIR}\nCogs loaded: {COGS}")

############################################################################
#                             Code starts here                             #
############################################################################


@bot.command(name = "translate", description = "Returns the translation found in-game for a string", scope=SCOPES)
@di.option(str, name = "search", description = "String or key to translate.", required=True)
@di.option(str, name = "target", description = "Language code, name or region or 'key' to translate to.", required = False, autocomplete=True)
@di.option(str, name = "source", description = "Language code, name or region or 'key' to translate from.", required = False, autocomplete=True)
@di.option(str, name = "edition", description = "Java or Bedrock Edition translation?", required=False, choices=[
    di.Choice(name="java", value="java"),
    di.Choice(name="bedrock", value="bedrock")
])
@di.option(int, name = "page", description = "Result page number.", required=False)
async def translate(ctx: di.CommandContext, search: str, target:str=None, source:str="en_us", edition:str=None, page:int=1):
    hidden=False
    try:
        if target == None:
            try:
                target = fetch_default(str(ctx.guild_id), "server", "targetlang")
            except:
                target="en_us"
        if edition == None:
             try:
                 edition = fetch_default(str(ctx.guild_id), "server", "edition")
             except:
                 edition="java"
        edition=edition.lower()
        target=target
        source=source
        found=find_translation(search, target, source, edition, page)
        list_message = found[0]
        exact = found[1]
        buttons = found[2]
        npages = found[3]
        pagenum = found[4]
        if len(list_message)>0:
            if exact == None:
                message = "\n".join(list_message)
                title = "No perfect matches"
                embedfields = [di.EmbedField(name="Close matches:",value=message)._json]
            else:
                try:
                    list_message.remove(exact)
                except ValueError:pass
                message = "\n".join(list_message)
                title = exact
                if len(list_message) == 0:
                    embedfields = []
                else:
                    embedfields = [di.EmbedField(name="Close matches:",value=message)._json]
            if edition=="java":
                try:
                    targetcode=lang(target, edition).replace("_", "")
                except embederr:
                    targetcode="enuk"
                url=f"https://crowdin.com/translate/minecraft/all/enus-{targetcode}?filter=basic&value=0#q={search.replace(' ', '%20')}"
            elif edition=="bedrock":
                url=None
            embed=di.Embed(
                title=title,
                fields=embedfields,
                url=url,
                footer=di.EmbedFooter(text=f"Page {pagenum}/{npages}", icon_url=avatar)._json,
                color=0x10F20F)
            hide=False
        else:
            targetcode=lang(target, edition).replace("_", "")
            raise embederr(
                "Couldn't find the translation",
                f"https://crowdin.com/translate/minecraft/all/enus-{targetcode}?filter=basic&value=0#q={search.replace(' ', '%20')}",
                color=0xff7f00,
                description="Click the title to search in Crowdin.")
    except embederr as e:
            """if beta==True:
            raise e
        else:"""
            embed=di.Embed(
                title=e.title,
                thumbnail=e.image,
                url=e.url,
                fields=e.field,
                color=e.color,
                description=e.desc
                )
            hidden=True
    except Exception as ex:
        if beta:
            raise ex
        else:
            embed=di.Embed(title="Something happened", description=f"Error description:\n{ex}", thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg")._json, color=0xff0000)
            hidden=True
    try:
        msg=await ctx.send(embeds=embed, ephemeral=hidden, components=buttons)
        remove = register_comp(msg.id, search, target, source, edition, msg.channel_id)
        for i in remove.items():
            rem_message=await di.get(bot, di.Message, object_id=i[0], parent_id=i[1])
            await rem_message.edit(components=None)
    except Exception as ex:
        if beta:
            raise ex
        else:
            await ctx.send(embeds=di.Embed(title="Something happened while sending message", description=f"Error description:\n{ex}", thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg")._json, color=0xff0000),ephemeral=True)

@bot.autocomplete("translate", "target")
async def autocomplete(ctx: di.CommandContext, user_input: str = ""):
    return await lang_autocomplete(ctx, user_input)
@bot.autocomplete("translate", "source")
async def autocomplete(ctx: di.CommandContext, user_input: str = ""):
    return await lang_autocomplete(ctx, user_input)

@bot.component("prevpage")
async def prevpage(ctx: di.CommandContext):
    embed=ctx.message.embeds[0]
    msg=json.load(open("loadedmessages.json"))[str(ctx.message.id)]
    #print(embed._json, ctx.message.id)
    pagenum=get_pagenum(embed, "-")
    if pagenum[0]==None:
        pass
    else:
        found=find_translation(msg[0], msg[1], msg[2], msg[3], pagenum[0])
        newtext="\n".join(found[0])
        newfooter=f"Page {str(pagenum[0])}/{str(pagenum[1])}"
        embed=di.Embed(
            title=embed.title,
            fields=[di.EmbedField(name="Close matches:",value=newtext)._json],
            url=embed.url,
            footer=di.EmbedFooter(text=newfooter, icon_url=avatar)._json,
            color=0x10F20F
            )
    await ctx.edit(embeds=embed)
@bot.component("nextpage")
async def nextpage(ctx: di.CommandContext):
    embed=ctx.message.embeds[0]
    msg=json.load(open("loadedmessages.json"))[str(ctx.message.id)]
    #print(embed._json, ctx.message.id)
    pagenum=get_pagenum(embed, "+")
    if pagenum[0]==None:
        pass
    else:
        found=find_translation(msg[0], msg[1], msg[2], msg[3], pagenum[0])
        newtext="\n".join(found[0])
        newfooter=f"Page {str(pagenum[0])}/{str(pagenum[1])}"
        embed=di.Embed(
            title=embed.title,
            fields=[di.EmbedField(name="Close matches:",value=newtext)._json],
            url=embed.url,
            footer=di.EmbedFooter(text=newfooter, icon_url=avatar)._json,
            color=0x10F20F
            )
    await ctx.edit(embeds=embed)

@bot.command(name="settings", description="Bot settings", scope=SCOPES, default_member_permissions=di.Permissions.ADMINISTRATOR, options=[
        di.Option(
            name="default-target-language",
            description="Sets the default server target language",
            type=di.OptionType.SUB_COMMAND,
            options=[
                di.Option(
                    name="targetlang",
                    description="The target language",
                    type = di.OptionType.STRING,
                    required=True,
                    autocomplete=True),
                    ]),
        di.Option(
            name="default-edition",
            description="Sets the default edition to translate to",
            type=di.OptionType.SUB_COMMAND,
            options=[
                di.Option(
                    name="edition",
                    description="Java or Bedrock edition?",
                    type = di.OptionType.STRING,
                    required=True,
                    choices=[
                        di.Choice(name="java", value="java"),
                        di.Choice(name="bedrock", value="bedrock")
                        ])])])
async def settings(ctx:di.CommandContext, sub_command, targetlang=None, edition=None):
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
            embed=di.Embed(title="Something happened",color=0xff0000,thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg")._json)
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
            embed=di.Embed(title="Something happened",color=0xff0000,thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg")._json)
    try:
        await ctx.send(embeds=embed,ephemeral=hide)
    except Exception as exc:
        if beta==True:
            raise exc
        else:
            await ctx.send(embeds=di.Embed(title="Something happened while sending message",color=0xff0000,thumbnail=di.EmbedImageStruct(url="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg")._json),ephemeral=True)
    json.dump(f, open("serverdefaults.json", "w"))
@bot.autocomplete("settings", "targetlang")
async def autocomplete(ctx: di.CommandContext, user_input: str = ""):
    return await lang_autocomplete(ctx, user_input)

for cog in COGS:
    if cog!="variables" and cog!="translatefuncs":
        bot.load("cogs." + cog)

bot.start()