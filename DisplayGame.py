from tkinter import *
from BookWurmple import *

WRONG_COLOR = '#565656'
PARTIAL_COLOR = '#f5c131'
RIGHT_COLOR = '#82d459'
BACKGROUND_COLOR = '#919191'
BST_BACKGROUND_COLOR = '#4287f5'
gameOver = False

#evenly spaced w/ 0.1 on either side
def evenSpacing(n, size):
	ret = 0.8 * (n / (size-1)) + 0.1
	return  ret

# stats = current guess
guessList = []
answer = randomPokemon()
def submitAnswer(event = None): # 'event = None' allows both the button & the Enter key to submit
	global gameOver
	if gameOver:
		return
	
	global guessEntry
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
	elif len(sharedAbilities) > 0 and len(sharedAbilities) != len(answer.abilities):
		colors[4] = PARTIAL_COLOR
	else:
		colors[4] = RIGHT_COLOR

	if guess.bst == answer.bst:
		colors[5] = RIGHT_COLOR
	else:
		colors[5] = BST_BACKGROUND_COLOR

	# set label text values
	name = guess.name.replace(' ','\n')
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
	if guess.bst < answer.bst: # higher/lower indication
		bst = '^\n' + bst
	elif guess.bst > answer.bst:
		bst = bst + '\nv'

	ht = 7  # this is as small as the squares can be & still fit all ability names
	wd = 14
	guessLabels = [
	Label(root, text=name, bg=colors[0], height=ht, width=wd),
	Label(root, text=types, bg=colors[1], height=ht, width=wd),
	Label(root, text=gen, bg=colors[2], height=ht, width=wd),
	Label(root, text=numEvos, bg=colors[3], height=ht, width=wd),
	Label(root, text=abilities, bg=colors[4], height=ht, width=wd),
	Label(root, text=bst, bg=colors[5], height=ht, width=wd)
	]
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

	if len(guessList) == 7:
		lblWinLose.config(text = 'You Lose!')
		gameOver = True
		guessEntry.config(state = 'disabled')

def resetGame():
	global gameOver
	global answer
	global guessList

	gameOver = False
	answer = randomPokemon()
	for g in guessList:
		for label in g:
			label.destroy()
	guessList.clear()
	guessEntry.config(state = 'normal')
	lblWinLose.config(text = '')

# set up window & static GUI elements
root = Tk()
root.title("BookWurmple")
root.geometry('800x950')
root['bg'] = BACKGROUND_COLOR

btnSubmit = Button(root, text = 'Submit', command = submitAnswer)
btnSubmit.pack(side = 'bottom', pady = 10)

btnReset = Button(root, text = 'Reset', command = resetGame)
btnReset.place(rely = .99, relx = .01, anchor = 'sw')

guessEntry = Entry(root)
guessEntry.pack(side = 'bottom')

lblWinLose = Label(root, bg = BACKGROUND_COLOR, font=(72))
lblWinLose.place(rely = .99, relx = .99, anchor='se')

lblSuggest = Label(root, bg = BACKGROUND_COLOR)
lblSuggest.place(rely = .9, relx = .25, anchor = 'n')

root.bind('<Return>',submitAnswer)

headerLabels = [
	Label(root, text = 'Name', bg=BACKGROUND_COLOR),
	Label(root, text = 'Types', bg=BACKGROUND_COLOR),
	Label(root, text = 'Generation', bg=BACKGROUND_COLOR),
	Label(root, text = 'Evolution Line', bg=BACKGROUND_COLOR),
	Label(root, text = 'Abilities', bg=BACKGROUND_COLOR),
	Label(root, text = 'BST', bg=BACKGROUND_COLOR)
	]
for i in range(0,len(headerLabels)):
	headerLabels[i].place(relx = evenSpacing(i,len(headerLabels)), rely = 0, anchor = 'n')


root.mainloop()