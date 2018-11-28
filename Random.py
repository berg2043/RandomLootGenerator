import random
import pandas as pd
import numpy as np

# Challenge Raiting Dictionary
crdic = { range(0, 5): 'CR 0-4', range(5, 11): 'CR 5-10', range(11, 17): 'CR 11-16', range(17, 50): 'CR 17+' }

# Finds if number is in the range
class RangeDict(dict):
    def __getitem__(self, item):
        if type(item) != range:
            for key in self:
                if item in key:
                    return self[key]
        else:
            return super().__getitem__(item)

# Class that finds which sheet to use
challenge_rating = RangeDict(crdic)

# Fetches what type of loot it is
def groupfetcher():
  group = input('Is this a group, horde, or individual loot? ')
  if group.lower() == 'group' or group.lower() == 'horde':
    type = 'G'
    return(type)
  elif group.lower() == 'individual':
    type = 'I'
    return(type)
  else:
    print('Invalid Input')
    groupfetcher()

# Fetches the CR
def crfetcher():
  cr = input('What is the CR of the monster or leader of the group? ')
  try:
    value = int(cr)
    if int(cr) < 50:
      return(challenge_rating[int(cr)])
    else:
      print('CR must be less than 50.')
      crfetcher()
  except ValueError:
    print('CR must be a whole number.')
    crfetcher()

# Retrieves the sheet that corresponds to the CR and type
df = pd.read_excel('Items.xlsx', sheet_name = str(groupfetcher()) + str(crfetcher()), index_col = 0, usecols = 'E:F')

# Keys were strings and I couldn't figure out another way to turn them into ranges
diction = df.to_dict()['Item']
dictionary = {}
for n in diction:
  dictionary[eval(n)] = diction[n]
diction = None

# Class that finds the item on the table
items = RangeDict(dictionary)

roll = random.randint(1,50)
print(str(roll) + ': ' + str(items[roll]))
