import random
import pandas as pd
import numpy as np
import tkinter as tk
import json

# Opens up the items file
with open('items.json', 'r') as f:
  UNIQUEITEMS = json.load(f)

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
def groupfetcher(ginputs):
  group = ginputs
  if group == 0:
    type = 'G'
    return(type)
  elif group == 1:
    type = 'I'
    return(type)
  else:
    print('You should not have been able to do this')
    groupfetcher()

# Does currency for individual
def currency(dict, range):
  cp = dictcreator(dict["CP"])[range]
  sp = dictcreator(dict["SP"])[range]
  ep = dictcreator(dict["EP"])[range]
  gp = dictcreator(dict["GP"])[range]
  pp = dictcreator(dict["PP"])[range]

  tcp = tk.Label(root, text = str(diceroller(cp)) + " CP").grid(row = 6, column = 1, columnspan = 2)
  tsp = tk.Label(root, text = str(diceroller(sp)) + " SP").grid(row = 7, column = 1, columnspan = 2)
  tep = tk.Label(root, text = str(diceroller(ep)) + " EP").grid(row = 8, column = 1, columnspan = 2)
  tgp = tk.Label(root, text = str(diceroller(gp)) + " GP").grid(row = 9, column = 1, columnspan = 2)
  tpp = tk.Label(root, text = str(diceroller(pp)) + " PP").grid(row = 10, column = 1, columnspan = 2)

# Fetches the CR
def crfetcher(crinputs):
  cr = crinputs
  try:
    value = int(cr)
    if int(cr) < 50:
      return(challenge_rating[int(cr)])
    else:
      clear()
      terror = tk.Label(root, text = 'CR must be less than 50.').grid(row = 6, columnspan = 2)
      return("whoops")
  except ValueError:
    clear()
    terror = tk.Label(root, text = 'CR must be a whole number.').grid(row = 6, columnspan = 2)
    return("whoops")

# Defines the dice rolled
def multiplier(curr, length):
  s = 0
  x = 0
  while x < len(length):
    n = x
    x += 1
    s += int(curr[n])*(10**(len(length)-x))
  return(s)

# Rolls the dice and does the math
def diceroller(cur):
  if cur == 0:
    return(0)
  else:
    number = multiplier(cur, cur[0:cur.find('d')])
    dice = multiplier(cur[cur.find('d')+1:cur.find('x')], cur[cur.find('d')+1:cur.find('x')])
    end = multiplier(cur[cur.find('x')+1:len(cur)], cur[cur.find('x')+1:len(cur)])
    x = 0
    count = 0
    while x < number:
      x += 1
      count += random.randint(1,dice)
    return(count*end)

# Outputs the individual currency
def currency(dict, range):
  cp = dictcreator(dict["CP"])[range]
  sp = dictcreator(dict["SP"])[range]
  ep = dictcreator(dict["EP"])[range]
  gp = dictcreator(dict["GP"])[range]
  pp = dictcreator(dict["PP"])[range]

  tcp = tk.Label(root, text = str(diceroller(cp)) + " CP").grid(row = 6, column = 1, columnspan = 2)
  tsp = tk.Label(root, text = str(diceroller(sp)) + " SP").grid(row = 7, column = 1, columnspan = 2)
  tep = tk.Label(root, text = str(diceroller(ep)) + " EP").grid(row = 8, column = 1, columnspan = 2)
  tgp = tk.Label(root, text = str(diceroller(gp)) + " GP").grid(row = 9, column = 1, columnspan = 2)
  tpp = tk.Label(root, text = str(diceroller(pp)) + " PP").grid(row = 10, column = 1, columnspan = 2)


# Returns Gems and/or Art Objects
def art(dict,roll, row):
  if dictcreator(dict['GA Numb'])[roll] != '0':
    timesa = diceroller(dictcreator(dict['GA Numb'])[roll])
    z = 0
    artdict = {}
    try:
      ranges = UNIQUEITEMS['Gem Art Ranges']['Max']
      arts = UNIQUEITEMS[dictcreator(dict['Gems or Art'])[roll]]['Item']
      while z < timesa:
        rolls = random.randint(1, ranges[dictcreator(dict['Gems or Art'])[roll]])
        artdict["var_" + str(z)] = tk.Label(root, text = (dictcreator(dict['Gems or Art'])[roll] + ' ' + (arts[str(rolls)]))).grid(row = row + 1, column = 0, columnspan = 8)
        z += 1 
        row += 1
    except KeyError:
      pass

# Retruns Magic Items
## Recieved a KeyError when a magic item wasn't rolled.  Used try to prevent.
def magicitems(dict, roll, row):
  if dictcreator(dict['MI Numb'])[roll] != '0':
    if dictcreator(dict['MI Numb 2'])[roll] != '0':
      times2 = diceroller(dictcreator(dict['MI Numb 2'])[roll])
      y = 0
      items2dict = {}
      try:
        mitems2 = UNIQUEITEMS[dictcreator(dict['Item 2'])[roll]]
        while y < times2:
          rolls = random.randint(1,100)
          items2dict['var_' + str(y)] = tk.Label(root, text = dictcreator(mitems2['Item'])[rolls]).grid(row = row + 1, column = 1, columnspan = 2)
          y += 1
          row += 1
      except KeyError:
        pass
    times = diceroller(dictcreator(dict['MI Numb'])[roll])
    x = 0
    itemsdict = {}
    try:
      mitems = UNIQUEITEMS[dictcreator(dict['Item'])[roll]]
      while x < times:
        rolls = random.randint(1,100)
        itemsdict["var_" + str(x)] = tk.Label(root, text = dictcreator(mitems['Item'])[rolls]).grid(row = row + 1, column = 1, columnspan = 2)
        x += 1
        row += 1
    except KeyError:
      pass
  art(dict, roll, row)

# Keys were strings and I couldn't figure out another way to turn them into ranges  
def dictcreator(dfs):
  diction = dfs
  dictionarys = {}
  for n in diction:
    dictionarys[eval(n)] = diction[n]
  diction = None
  return(RangeDict(dictionarys))


#GUI Starts Here

root = tk.Tk()

#type variable
types = tk.IntVar()
types.set(0)

tk.Label(root, text = "Welcome to Blood Cobra's Loot Roller for Dungeons and Dragons 5th Eddition").grid(row = 0, columnspan = 6)

# Sets variable for type of loot
grouporsingle = [
    ("Group", 0),
    ("Single",1)
]

# Clears output
def clear():
  for label in root.grid_slaves():
    if int(label.grid_info()["row"]) >  5:
      label.grid_forget()

def roller():
# Retrieves the sheet that corresponds to the CR and type
  if crfetcher(e1.get()) != "whoops":
    items = UNIQUEITEMS[str(groupfetcher(types.get())) + str(crfetcher(e1.get()))]
    clear()
    roll = random.randint(1,100)
    counts = 6
# What's done for Group Loot
    if str(groupfetcher(types.get())) == "G":
      magicitems(items, roll, 11)
      moneydict = {}
      for n in UNIQUEITEMS['Group Gold']:
        temps = (str(diceroller(UNIQUEITEMS['Group Gold'][n][str(crfetcher(e1.get()))])) + ' ' + n)
        moneydict[str(n)] = tk.Label(root, text = temps).grid(row = counts, column = 1, columnspan = 2)
        counts += 1

# Individual Loot
    else:
      currency(items, roll)

tk.Label(root, 
         text="""What type of loot?""",
         justify = tk.LEFT,
         padx = 0).grid(row = 1)

tk.Radiobutton(root, text = "Horde", indicatoron = 0, width = 10, padx = 0, variable = types, value = 0).grid(row = 1, column = 1)
tk.Radiobutton(root, text = "Single", indicatoron = 0, width = 10, padx = 0, variable = types, value = 1).grid(row = 1, column = 2)

tk.Label(root, text = "CR raiting:").grid(row=2)

e1 = tk.Entry(root, width = 5)

e1.grid(row = 2, column = 1)

tk.Button(root, text = "roll", command = roller).grid(row = 3)
tk.Button(root, text = "Quit", command = root.quit).grid(row = 3, column = 3)

root.mainloop()
