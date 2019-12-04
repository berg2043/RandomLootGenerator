import random
import pandas as pd
import numpy as np
import tkinter as tk

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
    print('Invalid Input')
    groupfetcher()

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

# Outputs the currency
def currency(range):
  cp = range["CP"]
  sp = range["SP"]
  ep = range["EP"]
  gp = range["GP"]
  pp = range["PP"]

  tcp = tk.Label(root, text = str(diceroller(cp)) + " cp").grid(row = 6, column = 1, columnspan = 2)
  tsp = tk.Label(root, text = str(diceroller(sp)) + " sp").grid(row = 7, column = 1, columnspan = 2)
  tep = tk.Label(root, text = str(diceroller(ep)) + " ep").grid(row = 8, column = 1, columnspan = 2)
  tgp = tk.Label(root, text = str(diceroller(gp)) + " gp").grid(row = 9, column = 1, columnspan = 2)
  tpp = tk.Label(root, text = str(diceroller(pp)) + " pp").grid(row = 10, column = 1, columnspan = 2)

# Returns Gems and/or Art Objects
def art(dict,roll, row):
  if dict[roll]['GA Numb'] != '0':
    timesa = diceroller(dict[roll]['GA Numb'])
    z = 0
    artdict = {}
    try:
      ranges = pd.read_excel('Items.xlsx', sheet_name = 'Gem Art Ranges', index_col = 0, usecols = 'A:B').to_dict('index')
      arts = pd.read_excel('Items.xlsx', sheet_name = dict[roll]['Gems or Art'], index_col = 0, usecols = 'A:B').to_dict('index')
      while z < timesa:
        rolls = random.randint(1, ranges[dict[roll]['Gems or Art']]['Max'])
        artdict["var_" + str(z)] = tk.Label(root, text = (dict[roll]['Gems or Art'] + ' ' + arts[rolls]['Item'])).grid(row = row + 1, column = 0, columnspan = 8)
        z += 1 
        row += 1
    except SyntaxError:
      pass

# Retruns Magic Items
## Recieved a SyntaxError: unexpected EOF when a magic item wasn't rolled.  Used try to prevent.
def magicitems(dict, roll, row):
  if dict[roll]['MI Numb'] != '0':
    if dict[roll]['MI Numb 2'] != '0':
      times2 = diceroller(dict[roll]['MI Numb 2'])
      y = 0
      items2dict = {}
      try:
        mdf2 = pd.read_excel('Items.xlsx', sheet_name = dict[roll]['Item 2'], index_col = 0, usecols = 'E:F')
        mitems2 = dictcreator(mdf2)
        while y < times2:
          rolls = random.randint(1,100)
          items2dict['var_' + str(y)] = tk.Label(root, text = mitems2[rolls]['Item']).grid(row = row + 1, column = 1, columnspan = 2)
          y += 1
          row += 1
      except SyntaxError:
        pass
    times = diceroller(dict[roll]['MI Numb'])
    x = 0
    itemsdict = {}
    try:
      mdf = pd.read_excel('Items.xlsx', sheet_name = dict[roll]['Item'], index_col = 0, usecols = 'E:F')
      mitems = dictcreator(mdf)
      while x < times:
        rolls = random.randint(1,100)
        itemsdict["var_" + str(x)] = tk.Label(root, text = mitems[rolls]['Item']).grid(row = row + 1, column = 1, columnspan = 2)
        itemsdict["var_" + str(x)] = tk.Label(root, text = mitems[rolls]['Item']).grid(row = row + 1, column = 1, columnspan = 2)
        itemsdict["var_" + str(x)] = tk.Label(root, text = mitems[rolls]['Item']).grid(row = row + 1, column = 1, columnspan = 2)
        x += 1
        row += 1
    except SyntaxError:
      pass
  art(dict, roll, row)

# Keys were strings and I couldn't figure out another way to turn them into ranges  
def dictcreator(dfs):
  diction = dfs.to_dict('index')
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
    df = pd.read_excel('Items.xlsx', sheet_name = str(groupfetcher(types.get())) + str(crfetcher(e1.get())), index_col = 0, usecols = 'E:K')

    items = dictcreator(df)
    clear()
    roll = random.randint(1,100)

# What's done for Group Loot
    if str(groupfetcher(types.get())) == "G":
      magicitems(items, roll, 11)
      groupc = pd.read_excel('Items.xlsx', sheet_name = "Group Gold", index_col = 0, usecols = 'A:F')
      cdiction = groupc.to_dict('index')
      crange = cdiction[str(crfetcher(e1.get()))]
      currency(crange)

# Individual Loot
    else:
      currency(items[roll])

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