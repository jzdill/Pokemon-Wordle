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