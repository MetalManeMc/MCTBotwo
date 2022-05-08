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