from pathlib import Path
import os

if "\\" in str(Path(os.path.dirname(os.path.realpath(__file__)))):
    beta=True
else:
    beta=False

if beta==True:
    SCOPES=[906169345007304724]
else:
    SCOPES=[]

avatar="https://cdn.discordapp.com/avatars/913119714400677899/aa2670b8669f0301e47b097639a1959a.webp"