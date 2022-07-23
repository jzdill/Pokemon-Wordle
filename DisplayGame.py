from tkinter import *

#evenly spaced w/ 0.1 on either side
def evenSpacing(n, size):
	ret = 0.8 * (n / (size-1)) + 0.1
	return  ret

def createLabels():
	testList = [
		Label(root,bg='blue',height=5,width=10),
		Label(root,bg='red',height=5,width=10),
		Label(root,bg='red',height=5,width=10),
		Label(root,bg='red',height=5,width=10),
		Label(root,bg='red',height=5,width=10),
		Label(root,bg='red',height=5,width=10)
		]	
	for i in range(0,len(testList)):
		testList[i].place(relx = evenSpacing(i,len(testList)), rely = 0.7, anchor = 's')
	testList[2].place(rely = 0.5)

# ctr = index in the list of guesses. higher index => older guess/further up
# stats = current guess
ctr = 1
def submitAnswer():
	for l in stats:
		global ctr
		h = l.winfo_height()
		offset = -1 * h * ctr
		l.place(y = offset) # using rely and y together sums them (i.e. y is an offset)
	ctr += 1

root = Tk()
root.title("Pokemon Wordle")
root.geometry('800x800')

btnKill = Button(root, text = 'kill', command = root.destroy)
btnKill.pack(side = 'top')

stats = [
	Label(root,text='pic/name',height=5,width=10),
	Label(root,text='types',bg='grey',height=5,width=10),
	Label(root,text='gen',bg='grey',height=5,width=10),
	Label(root,text='evos',bg='grey',height=5,width=10),
	Label(root,text='abilities',bg='grey',height=5,width=10),
	Label(root,text='BST',bg='grey',height=5,width=10)
	]
for i in range(0,len(stats)):
	stats[i].place(relx = evenSpacing(i,len(stats)), rely = 0.9, anchor = 's')

btnSubmit = Button(root, text = 'Submit', command = submitAnswer)
btnSubmit.pack(side = 'bottom', pady = 10)



root.mainloop()

