#TODO add header commments

from tkinter import *
from turtle import pos
from BookWurmple import *
from PIL import Image, ImageTk

WRONG_COLOR = '#565656'
PARTIAL_COLOR = '#f5c131'
RIGHT_COLOR = '#1a8224'
BACKGROUND_COLOR = '#919191'
BST_BACKGROUND_COLOR = '#4287f5'
gameOver = False

#evenly spaced w/ 0.1 on either sided
def evenSpacing(n, size):
	ret = 0.8 * (n / (size-1)) + 0.1
	return  ret

guessList = []
possibilities = getAllPokemon() #possible answers based on guesses so far, starts as all
answer = randomPokemon()
guess = None
bstCeiling = 2000 #bounds for determining possible answers
bstFloor = 0 
def submitAnswer(event = None): # 'event = None' allows both the button & the Enter key to submit
	global gameOver
	global guessEntry
	global possibilities
	global guess
	global answer

	if gameOver:
		return
	
	guess = getPokemon(guessEntry.get())

	lblSuggest.config(text = '')
	if guess == None: #invalid entry
		suggestions = spellCheck(guessEntry.get())
		if len(suggestions) == 0:
			lblSuggest.config(text = 'Pokemon not found.')
		else:
			str = 'Did you mean:\n'
			for s in suggestions:
				str += s + '\n'
			lblSuggest.config(text = str)
		guessEntry.delete(0,END)
		return

	# set label colors
	colors = [WRONG_COLOR,WRONG_COLOR,WRONG_COLOR,WRONG_COLOR,WRONG_COLOR,WRONG_COLOR]

	if guess.name == answer.name:
		colors[0] = RIGHT_COLOR
		possibilities = [guess]
	else:
		colors[0] = BACKGROUND_COLOR
	
	sharedTypes = list(set(guess.types) & set(answer.types))
	if len(sharedTypes) == 0:
		colors[1] = WRONG_COLOR
	elif len(sharedTypes) == len(guess.types) == len(answer.types):
		colors[1] = RIGHT_COLOR
	else:
		colors[1] = PARTIAL_COLOR

	if guess.gen == answer.gen:
		colors[2] = RIGHT_COLOR

	if guess.numEvos == answer.numEvos:
		colors[3] = RIGHT_COLOR

	sharedAbilities = list(set(guess.abilities) & set(answer.abilities))
	if len(sharedAbilities) == 0:
		colors[4] = WRONG_COLOR
	elif len(sharedAbilities) == len(answer.abilities) == len(guess.abilities):
		colors[4] = RIGHT_COLOR
	else:
		colors[4] = PARTIAL_COLOR

	if guess.bst == answer.bst:
		colors[5] = RIGHT_COLOR
	else:
		colors[5] = BST_BACKGROUND_COLOR

	# set label values
	sprite = ImageTk.PhotoImage(Image.open(getSprite(guess.name)))
	types = ''
	for t in guess.types:
		types += t + '\n'
	types = types[:-1]
	gen = guess.gen
	numEvos = guess.numEvos
	abilities = ''
	for a in guess.abilities:
		abilities += a + '\n'
	abilities = abilities[:-1]
	bst = guess.bst

	global bstFloor
	global bstCeiling
	if int(guess.bst) < int(answer.bst): 
		if int(guess.bst) > int(bstFloor): 
			bstFloor = guess.bst
		bst = '^\n' + bst # higher/lower indication
	elif int(guess.bst) > int(answer.bst):
		if int(guess.bst) < int(bstCeiling):
			bstCeiling = guess.bst
		bst = bst + '\nv'

	# place/move labels
	ht = 7  # this is as small as the squares can be & still fit all ability names
	wd = 14
	guessLabels = [
	Label(root, image=sprite, bg=colors[0], height = 107, width=100), #ht/wd bc images size differently than text
	Label(root, text=types, bg=colors[1], height=ht, width=wd),
	Label(root, text=gen, bg=colors[2], height=ht, width=wd),
	Label(root, text=numEvos, bg=colors[3], height=ht, width=wd),
	Label(root, text=abilities, bg=colors[4], height=ht, width=wd),
	Label(root, text=bst, bg=colors[5], height=ht, width=wd)
	]
	guessLabels[0].image = sprite

	guessEntry.delete(0,END)
	guessList.insert(0,guessLabels)
	for i in range(0,len(guessLabels)):
		guessLabels[i].place(relx = evenSpacing(i,len(guessLabels)), rely = 0.9, anchor = 's')

	for g in guessList:
		for label in g:
			h = label.winfo_height()
			i = guessList.index(g)
			offset = -1 * ((h * i) + (10 * i))
			label.place(y = offset) # using rely and y together sums them (i.e. y is an offset here)

	if guess == answer:
		lblWinLose.config(text = 'You Win!')
		gameOver = True
		guessEntry.config(state = 'disabled')

	if len(guessList) == 7 and guess != answer:
		lblWinLose.config(text = 'You Lose! The answer was ' + answer.name)
		gameOver = True
		guessEntry.config(state = 'disabled')
	
	#trim possibilities
	possibilities = list(filter(possFilter, possibilities))

	# set pokedex list
	if pokedexRoot != None:
		str = ''
		for p in possibilities:
			str += p.name + ', '
		lblPokedex.config(text = str[:-2])

def resetGame():
	global gameOver
	global answer
	global guessList
	global possibilities
	global bstFloor
	global bstCeiling

	gameOver = False
	answer = randomPokemon()
	for g in guessList:
		for label in g:
			label.destroy()
	guessList.clear()
	possibilities = getAllPokemon()
	bstFloor = 0
	bstCeiling = 1000
	guessEntry.config(state = 'normal')
	lblWinLose.config(text = '')
	closePokedex()

pokedexRoot = None
lblPokedex = None
#create pokedex window, if it doesn't already exist
def openPokedex():
	global pokedexRoot
	global lblPokedex
	global possibilities
	if pokedexRoot != None: return
	pokedexRoot = Tk()
	pokedexRoot.title("Pokedex")
	pokedexRoot.geometry('500x750')
	pokedexRoot['bg'] = BACKGROUND_COLOR
	pokedexRoot.protocol("WM_DELETE_WINDOW", closePokedex)

	lblPokedex = Label(pokedexRoot, bg = BACKGROUND_COLOR, wraplength = 500, justify = CENTER)
	str = ''
	for p in possibilities:
		str += p.name + ', '
	lblPokedex.config(text = str[:-2])
	lblPokedex.pack(side = 'top')

#reset variable to indicate pokedex window was closed
def closePokedex():
	global pokedexRoot
	pokedexRoot.destroy()
	pokedexRoot = None

#used to filter possibilities
def possFilter(p):
	global guess
	global answer

	if p.name == guess.name: return False

	#types
	sharedTypes = list(set(guess.types) & set(answer.types))
	if len(sharedTypes) == 0: #wrong
		if len(set(p.types) & set(guess.types)) > 0: #false if any types in common
			return False
	elif len(sharedTypes) == len(guess.types) == len(answer.types): #right
		if set(p.types) != set(guess.types):
			return False
	else: #partial
		if (set(p.types) == set(guess.types)) or (set(p.types) & set(guess.types) == set()): #all types or no types in common
			return False

	#gen
	if guess.gen == answer.gen:
		if p.gen != guess.gen:
			return False
	else:
		if p.gen == guess.gen:
			return False

	#numEvos
	if guess.numEvos == answer.numEvos:
		if p.numEvos != guess.numEvos:
			return False
	else:
		if p.numEvos == guess.numEvos:
			return False

	#abilities
	sharedAbilities = list(set(guess.abilities) & set(answer.abilities))
	if len(sharedAbilities) == 0:
		if len(set(p.abilities) & set(guess.abilities)) > 0:
			return False
	elif len(sharedAbilities) > 0 and ( len(sharedAbilities) != len(answer.abilities) or len(sharedAbilities) != len(guess.abilities) ):
		abilPossIntersect = set(p.abilities) & set(guess.abilities)
		if len(abilPossIntersect) == 0 or len(abilPossIntersect) == len(guess.abilities):
			return False
	else:
		if len(set(p.abilities) & set(guess.abilities)) != len(guess.abilities):
			return False

	#bst
	if guess.bst == answer.bst and p.bst != guess.bst:
		return False
	if int(guess.bst) < int(answer.bst) and int(p.bst) < int(guess.bst):
		return False
	elif int(guess.bst) > int(answer.bst) and int(p.bst) > int(guess.bst):
		return False

	return True

# set up window & static GUI elements
root = Tk()
root.title("BookWurmple")
root.geometry('800x950')
root['bg'] = BACKGROUND_COLOR

btnSubmit = Button(root, text = 'Submit', command = submitAnswer)
btnSubmit.pack(side = 'bottom', pady = 10)

btnReset = Button(root, text = 'Reset', command = resetGame)
btnReset.place(rely = .99, relx = .01, anchor = 'sw')

btnPokedex = Button(root, text = 'Show Pokedex', command = openPokedex)
btnPokedex.place(rely = .99, relx = .01, anchor = 'sw', y = -30)

guessEntry = Entry(root)
guessEntry.pack(side = 'bottom')

lblWinLose = Label(root, bg = BACKGROUND_COLOR, font=(72))
lblWinLose.place(rely = .99, relx = .99, anchor='se')

lblSuggest = Label(root, bg = BACKGROUND_COLOR)
lblSuggest.place(rely = .9, relx = .25, anchor = 'n')

root.bind('<Return>',submitAnswer)

headerLabels = [
	Label(root, text = 'Pokemon', bg=BACKGROUND_COLOR),
	Label(root, text = 'Types', bg=BACKGROUND_COLOR),
	Label(root, text = 'Generation', bg=BACKGROUND_COLOR),
	Label(root, text = 'Evolution Line', bg=BACKGROUND_COLOR),
	Label(root, text = 'Abilities', bg=BACKGROUND_COLOR),
	Label(root, text = 'BST', bg=BACKGROUND_COLOR)
	]
for i in range(0,len(headerLabels)):
	headerLabels[i].place(relx = evenSpacing(i,len(headerLabels)), rely = 0, anchor = 'n')

root.mainloop()