from pathlib import Path
import os
import json
import interactions as di


def open_json(jsonfile, edition="java"):
    """
    This function open a file that's specified through the command.
    The first line establishes that json_path is
    Path (a .join for paths, part of the Pathlib) DATA_DIR (the base path towards /lang/)
    and jsonfile, jsonfile is established by the command and automatically
    transforms an input such as "es_es" into "es_es.json".
    After this, it json.loads the file into memory by turning it into a
    dictionary called dictionary_json. The file is then closed and
    from now on ONLY the dictionary that was returned will be used.
    """
    if edition == "java":
        json_path = Path(JAVA_DIR, jsonfile).with_suffix(".json")
    elif edition == "bedrock":
        json_path = Path(BEDROCK_DIR, jsonfile).with_suffix(".json")
    with open(json_path, encoding="utf-8") as js:
        return json.load(js)


class embederr(Exception):
    def __init__(
        self,
        title=None,
        url=None,
        hidden=True,
        color=0xFF0000,
        description=None,
        hasfield=False,
        field=["name", "value"],
        hasimage=True,
        image="https://cdn.discordapp.com/attachments/823557655804379146/940260826059776020/218-2188461_thinking-meme-png-thinking-meme-with-cup.jpg",
    ) -> None:
        self.title = title
        self.url = url
        self.hidden = hidden
        self.color = color
        self.desc = description
        if hasimage:
            self.image = di.EmbedAttachment(url=image)
        else:
            self.image = None
        if hasfield:
            self.field = [di.EmbedField(name=field[0], value=field[1])]
        else:
            self.field = None


PATH = Path(os.path.dirname(os.path.realpath(__file__))).parent
DATA_DIR = Path(PATH, "lang")
JAVA_DIR = Path(DATA_DIR, "java")
BEDROCK_DIR = Path(DATA_DIR, "bedrock")
COGS = [
    module[:-3]
    for module in os.listdir(f"{Path(PATH, 'cogs')}")
    if module not in ("variables.py", "down_checker.py") and module[-3:] == ".py"
]

Footers = (
    "See /help for more info.",
    "The blue text will be an exact match, if one is found.",
    "This is NOT a machine translation (except maybe if you used the Bedrock translations).",
)


if "\\" in str(Path(os.path.dirname(os.path.realpath(__file__)))):
    BETA = True
else:
    BETA = False

if BETA == True:
    SCOPES = [906169345007304724]
else:
    SCOPES = []

prevbutton = di.Button(style=di.ButtonStyle.PRIMARY, label="◀", custom_id="prevpage")
nextbutton = di.Button(style=di.ButtonStyle.PRIMARY, label="▶", custom_id="nextpage")


langcodes, langcodesapp, langnames, langregions, langfull = [], [], [], [], []

for a, b, c in os.walk(
    JAVA_DIR
):  # Gives a list of java language codes, names and regions, so i can search in them
    for i in c:
        langcodes.append(i.split(".")[0].lower())
        langnames.append(open_json(i)["language.name"].lower())
        langcodesapp.append(open_json(i)["language.code"].lower())
        langregions.append(open_json(i)["language.region"].lower())
        langfull.append(
            open_json(i)["language.name"] + " (" + open_json(i)["language.region"] + ")"
        )
    langcodes.append("key")
    langfull.append("key")
    break


belangcodes, belangcodesandnames, belangnames, belangregions, belangamedict = (
    [],
    [],
    [],
    [],
    {},
)


names = json.load(open("language_names.json", encoding="utf-8"))
for i in names:
    belangcodes.append(i[0].lower())
    belangcodesandnames.append(i[1])
    codeandname = i[1].split(" (")
    belangnames.append(codeandname[0])
    try:
        belangregions.append(codeandname[1][:-1])
    except IndexError:
        belangregions.append(None)
    belangamedict[belangcodes[-1]] = belangcodesandnames[-1]


ALL_LANGUAGES = langfull + [
    lang for lang in belangcodesandnames if lang not in langfull
]

AVATAR = "https://cdn.discordapp.com/avatars/913119714400677899/aa2670b8669f0301e47b097639a1959a"

HOOK = "<:bighook:937813704316158072>"
