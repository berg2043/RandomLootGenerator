import random
import pandas as pd
import numpy as np

#Imports the excel file holding all the loot tables
df = pd.read_excel('Items.xlsx', sheet_name = 'CR1', index_col = 0, usecols = 'E:F')

#Creates the initial dictionary
diction = df.to_dict()['Item']

#Keys were strings and I couldn't figure out another way to turn them into ranges
dictionary = {}
for n in diction:
  dictionary[eval(n)] = diction[n]

#clear this variable
diction = None

#The Table Finder
class RangeDict(dict):
    def __getitem__(self, item):
        if type(item) != range:
            for key in self:
                if item in key:
                    return self[key]
        else:
            return super().__getitem__(item)

cr_one = RangeDict(dictionary)
roll = random.randint(1,50)
print(str(roll) + ': ' + str(cr_one[roll]))
