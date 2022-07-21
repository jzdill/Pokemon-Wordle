import os

class Pokemon:
    def __init__(self, dexNum, name, gen, type1, type2, abil1, abil2, abil3, bst):
        self.dexNum = dexNum
        self.name = name
        self.gen = gen
        self.type1 = type1
        self.type2 = type2
        self.abil1 = abil1
        self.abil2 = abil2
        self.abil3 = abil3
        self.bst = bst
    
    def toString(self):
        ret = '{},{},{},{},{},{},{},{},{}'
        return ret.format(self.dexNum,self.name,self.gen,self.type1,self.type2,self.abil1,self.abil2,self.abil3,self.bst)

# read data from file into pokedex
f = open("pokedata.dat",encoding="utf8")
pokedex = []

for line in f:
    attrList = line.split(',')
    dexNum = int(attrList[1])
    name = attrList[2]
    gen = int(attrList[5])
    type1 = attrList[11]
    type2 = attrList[12]
    abil1 = attrList[16]
    abil2 = attrList[17]
    abil3 = attrList[18]
    #some of the BSTs have .0 appended for some reason
    bstStr = attrList[19]
    if '.0' in bstStr: 
        bstStr = bstStr[:-2]
    bst = int(bstStr)
    pokedex.append(Pokemon(dexNum,name,gen,type1,type2,abil1,abil2,abil3,bst))
f.close()

# write pokedex to new file
if os.path.exists('pokedex.dat'): os.remove('pokedex.dat')
f = open('pokedex.dat','w',encoding='utf8')

for p in pokedex: f.write(p.toString() + '\n')
f.close()