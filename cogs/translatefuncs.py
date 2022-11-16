import interactions as di
import json
import time
import os
from cogs.variables import *


def complete(search:str, inside:list):

    """
    This function is essentially an autocompletion.
    It takes a string and a list, in which it"s going to find complete strings.
    Walks through the list and asks whether the search is in the value. If it is,
    it appends the value to result. If none are found, it returns an empty list.
    """

    return [i for i in inside if search.lower() in i.lower()]


def fetch_default(code, category, data):
    """
    This function fetches defaults in serverdefaults.json
    """
    f = json.load(open("serverdefaults.json"))
    return f[code][category][data]


def find_translation(string:str, targetlang:str, sourcelang:str, edition:str, page:int=1, pagesize:int=10):

    """
    This function finds translations and returns the list of matches.
    """
    string = string.lower()
    try:
        if targetlang!="key": # if either are key, they should not be searched for as files, instead use jsdef
            jstarget = open_json(lang(targetlang, edition), edition)
        if sourcelang!="key":
            jssource = open_json(lang(sourcelang, edition), edition)
        jsdef = open_json("en_us") # this will get used everytime to key or from key is used... (json default... change the name if you want)
    except IndexError:
        return

    exact=None
    if targetlang=="key": # figures out, which mode to use
        if sourcelang=="key":
            result = complete(string, jsdef) #ktk
        else:
            result = [i for i in jsdef if string in jssource[i].lower()] #stk
            for i in result:
                if jssource[i].lower()==string:
                    exact=i
                    break
    else:
        if sourcelang=="key":
            result = [jstarget[i] for i in complete(string, jsdef)] #kts
            try: exact=jstarget[string]
            except: pass
        else:
            result = [jstarget[i] for i in [i for i in jssource if string in jssource[i].lower()]] #sts(string, jstarget, jssource)
            for i in jssource:
                if jssource[i].lower()==string:
                    exact=jstarget[i]
                    break

    try:    #removes blank results
        while True:
            result.remove("")
    except ValueError:
        pass

    k=0    
    while True: #iterates through all results to make sure lat page number is consistant
        k+=1
        opagelen=len(" ".join(result[pagesize*(k-1):pagesize*k]))
        if opagelen==0:
            pagenum=k-1
            break
        elif opagelen>1000:
            pagesize-=1
            k=0
    
    if page>pagenum:page=pagenum
    elif page<1:page=1

    added=False
    if len(result)>10:  # if there are more than 10 results, sets result to the 10 strings following (page-1)
        result=result[pagesize*(page-1):pagesize*page]
        added=True

    if added:
        buttons = di.ActionRow.new(prevbutton, nextbutton)
    else:
        buttons=None

    if added and page<pagenum:
        result.append("**…and more!**")
    return result, exact, buttons, pagenum, page


def lang(search:str, edition):

    """
    Returns a complete internal language code to be used for file opening.
    Input can be the expected output too.
    Input can be approved language code, name, region or internal code (searching in this order)
    """
    search = search.lower()
    injava=False
    if edition=="java":
        for i in range(len(langcodesapp)): # We can't use complete here because we would have no clue which langcode to use. The thing we need is index of langcode, not completed langname or whatever.
            if search in langcodesapp[i].lower():
                return langcodes[i]
        for i in range(len(langcodes)):
            if search in langcodes[i].lower():
                return langcodes[i]
        for i in range(len(langnames)):
            if search in langnames[i].lower():
                return langcodes[i]
        for i in range(len(langregions)):
            if search in langregions[i].lower():
                return langcodes[i]
        for i in range(len(langfull)):
            if search in langfull[i].lower():
                return langcodes[i]
    elif edition=="bedrock":
        for i in range(len(belangcodes)): # We can't use complete here because we would have no clue which langcode to use. The thing we need is index of langcode, not completed langname or whatever.
            if search in belangcodes[i].lower():
                return belangcodes[i]
        for i in range(len(belangnames)):
            if search in belangnames[i].lower():
                return belangcodes[i]
        for i in range(len(belangregions)):
            try:
                if search in belangregions[i].lower():
                    return belangcodes[i]
            except AttributeError:pass
        for i in range(len(langfull)):
            if search in langfull[i].lower():
                injava=True
                for x in range(len(belangcodes)):
                    if langcodes[i]==belangcodes[x]:
                        return belangcodes[x]
                    
            
    ret=complete(search, langcodes)
    if len(ret)>0:
        return ret[0]
    else:
        if injava==False:
            raise embederr("Language not found…")
        elif injava==True:
            raise embederr("This language does not exist in Bedrock Edition.")

def get_pagenum(embed, op="+"):
    pagenum=embed.footer.text
    pagenum=pagenum.split("/")
    max=int(pagenum[1])
    pagenum=pagenum[0].split(" ")
    pagenum=int(pagenum[1])
    if op=="+":
        if pagenum-max>=0:
            pagenum=None
        else:
            pagenum+=1
    else:
        if pagenum<=1:
            pagenum=None
        else:
            pagenum-=1
    return pagenum, max

def register_comp(id:int, search, target, source, edition, channel):
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "loadedmessages.json"), "r") as f:
        t=time.time()
        cont=json.load(f)
        deletes={}
        for x in cont.items():
            if float(x[1][4])+900<t:
                deletes[x[0]]=x[1][5]
        for i in deletes:
            cont.pop(i)
        cont[str(id)]=[search, target, source, edition, str(t), str(channel)]
        json.dump(cont, open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "loadedmessages.json"), "w"))
    return deletes

async def lang_autocomplete(ctx: di.CommandContext, value: str = ""):
    items = langfull
    choices = [
        di.Choice(name=item, value=item) for item in items if value.lower() in item.lower()
    ] 
    await ctx.populate(choices[:25])