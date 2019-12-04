#You'll need to change all instance of "{ to { and }" to } and remove all \

import pandas as pd
import numpy as np
import json
import fileinput

# gets lif of sheets
x = pd.ExcelFile('Items_JSON.xlsx')

jsondict = {}

# turns each sheet from Items2 into a json file that you'll need to delete later
for n in x.sheet_names:
  jsondict[n] = pd.read_exl.cel('Items_JSON.xlsx', sheet_name = n, index_col = 0).to_json()

# Drops dictb into a json that needs to be edited.  See above
json = json.dumps(jsondict)
f = open('items.json', 'w')
f.write(json)
f.close()

# Does the Editing for you
def replace_word(infile,old_word,new_word):
  with open(infile, 'r') as fileone:
    f1=fileone.read()
  with open(infile, 'w') as filetwo:
    f2=filetwo
    m=f1.replace(old_word,new_word)
    f2.write(m)

replace_word('items.json', '"{', '{')
replace_word('items.json', '}"', '}')
replace_word('items.json', '\\', '')