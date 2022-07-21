import os
import shutil


def savePokedex(fMain, fTemp):
    for l in fMain:
        fTemp.write(l)
    fTemp.close()
    fMain.close()

    #pokedextemp.dat has the data we want now
    if os.path.exists('pokedexFinal.dat'): os.remove('pokedexFinal.dat')
    os.rename('pokedextemp.dat','pokedexFinal.dat')

    print("Saved!")


#load in the previous save, if it exists
if os.path.exists('pokedexFinal.dat'):
    os.remove('pokedex.dat')
    shutil.copy('pokedexFinal.dat','pokedex.dat')

fMain = open('pokedex.dat','r+',encoding='utf8')
if os.path.exists('pokedextemp.dat'): os.remove('pokedextemp.dat')
open('pokedextemp.dat','a',encoding='utf8')
fTemp = open('pokedextemp.dat','r+',encoding='utf8')

for l in fMain:
    line = l.split(',')
    if len(line) == 10: 
        fTemp.write(l)
        continue
    
    name = line[1]

    num = 0
    saved = False
    #get user input
    while num < 1 or num > 3:
        str = "How many stages are in {}\'s evolution chain? Megas don't count. Answers are 1-3. (Type 'save' to save your progress & quit.) \n\n\n\n\n\n\n\n\n\n\n"
        inp = input(str.format(name))

        #save & quit
        if inp.capitalize() == 'Save':
            print('Saving...')
            fTemp.write(l)
            savePokedex(fMain, fTemp)
            exit()

        #number check
        try:
            num = int(inp)
        except:
            print("Invalid input.")
            continue

        if num < 1 or num > 3:
            print("Must be 1-3.")
            continue

    s = l[:-1] + ',{}\n'
    fTemp.write(s.format(num))
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    
savePokedex(fMain,fTemp)
print("You finished!")

    
