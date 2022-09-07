import random

def randomPokemon():
    return random.choice(list(pokedex.values()))

def getPokemon(str):
    try: return pokedex[str.upper()]
    except: return None

# check for pokemon that contain str (ex. 'king' in Kingdra)
# return list if len <= 10
def spellCheck(str):
    ret = []
    for p in pokedex:
        if str.upper() in p:
            ret.append(p)
        if len(ret) > 10: return []
    return ret

# returns list of all pokemon
def getAllPokemon():
    return list(pokedex.values())

class Pokemon:
    def __init__(self,dexNum,name,types,gen,numEvos,bst,abilities,):
        self.dexNum = dexNum
        self.name = name
        self.types = types
        self.gen = gen
        self.numEvos = numEvos
        self.bst = bst
        self.abilities = abilities

    def toString(self):
        ret = "{}: {} & {}"
        return ret.format(self.name,self.types[0],self.types[1])

#returns filename for given pokemon name. returns None if no file found
def getSprite(n):
    fname = './sprites/' + imageFileName(n) + '.png'
    try: 
        file = open(fname)
        file.close()
        return fname
    except: 
        print(fname + ' not found')
        return None

#format name to find .png
def imageFileName(n):
    name = n.lower()
    name = name.replace('.','')
    name = name.replace('\'','')
    name = name.replace(':','')
    name = name.replace('%','')
    name = name.replace(' ','-')

    if 'mega-' in name:
        if 'charizard' in name or 'mewtwo' in name:
            name = name[5:-2] + '-mega' + name[-2:]
        else:
            name = name.partition('mega-')[2] + '-mega'
    if 'alolan-' in name:
        name = name[7:] + '-alola'
    if 'galarian-' in name and 'darmanitan' not in name:
        name = name[9:] + '-galar'
    if 'hisuian-' in name:
        name = name[8:] + '-hisui'
    if '-form' in name:
        name = name.partition('-form')[0]
    if 'primal-' in name:
        name = name.partition('-')[2] + '-primal'
    if 'incarnate' in name:
        name = name.partition('-incarnate')[0]
    if 'urshifu' in name:
        name = 'urshifu'
    if 'hero-of' in name:
        name = name.partition('-')[0]
    if '-crowned' in name:
        name = name.partition('-')[0] + '-crowned'
    if '-necrozma' in name:
        name = 'necrozma-' + name.partition('-')[0]
    if 'minior-m' in name:
        name = 'minior'
    if 'minior-c' in name:
        name = 'minior-blue'
    if 'oricorio' in name:
        name = name.partition('-style')[0]
    if name == 'ash-greninja':
        name = 'greninja-ash'
    if '-kyurem' in name:
        name = 'kyurem-' + name.partition('-kyurem')[0]
    if 'darmanitan' in name:
        n = 'darmanitan'
        if 'galar' in name: n += '-galar'
        if 'zen' in name: n += '-zen'
        name = n
    if '-rotom' in name:
        name = 'rotom-' + name.partition('-')[0]
    if 'wormadam-' in name:
        name = name.partition('-cloak')[0]

    return name

#check that sprite files exist for every pokemon
def checkSprites():
    for p in pokedex:
        f = getSprite(p)
    print("All sprites checked.")

#data is formatted as:
#dexNum,name,gen,type1,type2,ability1,ability2,ability3,bst,numEvos
f = open('pokedex.dat')

#load pokedex
pokedex = {}
for l in f:
    line = l.split(',')
    name = line[1]
    types = line[3:5]
    #remove blank types
    for t in types:
        if t == '': types.remove(t)
    if name == 'Rockruff':
        types.append('Own Tempo') #Rockruff is the only Pokemon w/ 4 abilities
    abilities = line[5:8]
    try: numEvos = line[9][:-1] #trim the \n char
    except: numEvos = 0
    #remove blank abilties, has to loop twice bc of pokemon w/ only 1 ability
    for a in abilities:
        if a == '': abilities.remove(a)
    for a in abilities:
        if a == '': abilities.remove(a)
    newPoke = Pokemon(line[0],name,types,line[2],numEvos,line[8],abilities)
    pokedex[name.upper()] = newPoke
f.close()

""" ------------------- CODE TO RUN TEXT VERSION OF THE GAME -------------------

#select the secret pokemon
answer = random.choice(list(pokedex.values()))

#run the game
done = False
turn = 1
while not done:
    turnStr = '=*=*=*=*=*=*=*=*=*=*=*=*=* TURN {} =*=*=*=*=*=*=*=*=*=*=*=*=*=*='
    print(turnStr.format(turn))
    turn += 1

    inp = input('Guess a Pokemon: ')
    if inp.capitalize() == 'Exit': break
    if inp.capitalize() == 'Give up':
        print("You Lose!")
        s = 'The answer was {}.'
        print(s.format(answer.name))
        if input("Type 'Yes' to play again! ").capitalize() == 'Yes':
            print('\n\n\n')
            answer = random.choice(list(pokedex.values()))
            turn = 1
            continue
        else: break

    try:
        guess = pokedex[inp.upper()]
    except:
        print("Pokemon not found.")
        turn -= 1
        continue
    
    if guess == answer: 
        print("You Win!")
        if input("Type 'Yes' to play again! ").capitalize() == 'Yes':
            print('\n\n\n')
            answer = random.choice(list(pokedex.values()))
            turn = 1
            continue
        else: break

    if guess.gen == answer.gen:
        s = "The answer is gen {}."
        print(s.format(guess.gen))
    else:
        s = "The answer is not Gen {}."
        print(s.format(guess.gen))

    if guess.numEvos == answer.numEvos:
        s = "The answer has a {} evolution chain."
        print(s.format(guess.numEvos))
    else:
        s = "The answer does not have a {} evolution chain."
        print(s.format(guess.numEvos))

    if guess.bst == answer.bst:
        s = "The answer has the same BST as {}"
        print(s.format(guess.name))
    elif guess.bst > answer.bst:
        s = "The answer has a lower BST than {}."
        print(s.format(guess.name))
    else:
        s = "The answer has a higher BST than {}."
        print(s.format(guess.name))

    sharedAbilities = list(set(guess.abilities) & set(answer.abilities))

    if len(sharedAbilities) == 0:
        s = "The answer shares no abilities with {}."
        print(s.format(guess.name))
    elif len(sharedAbilities) > 0 and len(sharedAbilities) != len(answer.abilities):
        s = "The answer shares some abilties with {}, but not all."
        print(s.format(guess.name))
    else:
        s = "The answer shares all abilities with {}."
        print(s.format(guess.name))

    sharedTypes = list(set(guess.types) & set(answer.types))
    if len(sharedTypes) == 0:
        s = "The answer shares no types with {}."
        print(s.format(guess.name))
    elif len(sharedTypes) == len(guess.types) == len(answer.types):
        s = "The answer is the exact same type(s) as {}."
        print(s.format(guess.name))
    else:
        s = "The answer only shares one type with {}."
        print(s.format(guess.name))
"""