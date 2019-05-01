import random
import time
import string

# Print a field with cols and rows
def printField(inputField):
	
	colHeaders = ['-'] + list(string.ascii_uppercase[0:COLS])
	print('\t'.join(colHeaders))

	rowHeaders = list(range(1, ROWS + 1))

	for x in range(0, ROWS):
		print('\t'.join([str(rowHeaders[x])] + inputField[x]))

	print('-'*int(8.33*COLS)) # ~ 8.33 dashes per column

# Plant bombs in the field
def plantBombs():

	# Generate X unique positions
	bombPositions = []
	while len(bombPositions) < BOMBS:
		pos = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
		if pos not in bombPositions:
			bombPositions.append(pos)

	# Plant bombs in field
	for pos in bombPositions:
		x, y = pos
		field[x][y] = '💣'

# Calculate surrounding number of bombs for all non-bomb positions
def calculateFieldNumbers():
	for x in range(0, ROWS):
		for y in range(0, COLS):
			
			if (field[x][y] != '💣'):

				bombsAtBorders = 0

				# Check all neighbours
				for a in range(-1, 2): # delta X
					for b in range(-1, 2): # delta Y
						if (x + a >= 0) and (x + a <= ROWS-1) and (y + b >= 0) and (y + b <= COLS-1): # valid position
							
							if (field[x+a][y+b] == '💣'):
								bombsAtBorders += 1

				field[x][y] = str(bombsAtBorders)

# Gets index values for row and column input values
def translateToIndexValues(row, col):
	rows = map(str, list(range(1, ROWS + 1)))
	cols = list(string.ascii_uppercase[0:COLS])

	return rows.index(row), cols.index(col)

def sweep(row, col):
	if field[row][col] == '💣':
		gameover()
	else:
		updateKnownField(row, col)

def flag(row, col):
	updateKnownField(row, col, 'f')		

# Puts a flag (flag='f') or uncovers the field (no third argument passed)
def updateKnownField(x, y, flag=None):
	if flag == 'f':
		knownField[x][y] = '⚑'
	else:
		knownField[x][y] = field[x][y]
		if field[x][y] == '0':
			uncoverZeroesAndTheirNeighbours(x, y)

# Recursive function that uncovers zero fields and all their neighbours
def uncoverZeroesAndTheirNeighbours(x, y):
	knownField[x][y] = field[x][y]

	for a in range(-1, 2):
		for b in range(-1, 2):
			if (x + a >= 0) and (x + a <= ROWS-1) and (y + b >= 0) and (y + b <= COLS-1): # valid position
				
				if(field[x+a][y+b]=='0' and knownField[x+a][y+b]!='0'): # Check if knownField isn't set to zero yet (first line of function) to prevent infinite recursion from occuring
					uncoverZeroesAndTheirNeighbours(x+a,y+b)

				knownField[x+a][y+b] = field[x+a][y+b]

# Checks all cells to check if either bombs can be marked or whether neighbours can be swept.
# If nothing is found after checking all cells: sweep a random cell.
def solveOneTile():

	unsweptPositions = []

	for x in range(0, ROWS):
		for y in range(0, COLS):
			if knownField[x][y] == '*':
				unsweptPositions.append((x,y))
			elif knownField[x][y] == '⚑':
				pass
			else: # number between 1 and 8
				fieldValue = knownField[x][y]
				surroudingCells = 0
				neighboursUnknown = []
				neighboursFlagged = []

				for a in range(-1, 2):
					for b in range(-1, 2):

						if (x + a >= 0) and (x + a <= ROWS-1) and (y + b >= 0) and (y + b <= COLS-1) and not(a == 0 and b == 0): # valid and not itself
							
							surroudingCells += 1

							if (knownField[x+a][y+b] == '*'):
								neighboursUnknown.append((x+a, y+b))
							elif (knownField[x+a][y+b] == '⚑'):
								neighboursFlagged.append((x+a, y+b))
				
				# If the amount of flagged neighbours equals the value of the field 
				# and there are remaining unknown neighbours then all remaining unknown neighbours MUST be swept
				if(len(neighboursFlagged) == int(fieldValue) and len(neighboursUnknown) > 0):
					print('All neighbouring bombs flagged for %s,%s. Sweeping remaining neighbours.' % (x,y))
					for pos in neighboursUnknown:
						x, y = pos
						sweep(x, y)
					return True # stop checking

				# If the amount of unknown neighbours + flagged neighbours equal the value of the field
				# and there are remaining unknown neighbours then all remaining unknown neighbours MUST be flagged
				elif(len(neighboursFlagged) + len(neighboursUnknown) == int(fieldValue) and len(neighboursUnknown) > 0):
					print('All remaining neighbours must be bombs for %s,%s. Flagging remaining neighbours.' % (x,y))
					for pos in neighboursUnknown:
						x, y = pos
						flag(x, y)
					return True # stop checking
	
	# Sweeps a random unswept position because nothing has been found
	x, y = random.choice(unsweptPositions)
	print('No certainties found, sweeping %s, %s' % (x,y))
	sweep(x, y)

# Loops over all known fields to see if they are all uncovered or flagged
def checkWinCondition():
	flags = 0
	for x in range(0, ROWS):
		for y in range(0, COLS):
			
			if knownField[x][y] == '*': # Player has remaining uncleared fields
				return False

			if knownField[x][y] == '⚑':
				flags += 1

	if flags == BOMBS: # Player has no remaining uncleared fields and all bombs have been flagged
		return True
	else:
		print('bombs need to be planted %s %s ' % (flags, BOMBS))
		return False

def gameover():
	print('Kabooom!\nGame over!')
	printField(knownField)
	printField(field)
	exit()

# Settings
BOMBS = 40
ROWS = 14
COLS = 12

# Build field
field = []
knownField = []

for x in range(ROWS):
	field.append(['*']*COLS)
	knownField.append(['*']*COLS)

# Setup
plantBombs()
calculateFieldNumbers()
startTime = 0

# Print game instructions
print("Welcome to Minesweeper!\nType \'q\' to quit the game.\n"
	  "Enter row number and column letter to sweep that field (eg \'1A\').\n"
	  "Add an \'m\' to flag that field (eg \'1Am\').\n"
	  "Press \'s\' to make best possible move.\n"
	  "Press \'as\' to auto complete the game.")

# Start main game loop
printField(knownField)
autoSolve = False

while True:
	if autoSolve == False:
		userInput = input('>') 
	else:
		userInput = 's'

	if startTime == 0:
		startTime = time.time()

	if userInput == 'q':
		print('K thx bye')
		exit()
	
	elif userInput == 's':
		solveOneTile()

	elif userInput == 'as':
		autoSolve = True

	else:
		if((len(userInput) in [2, 3])): # valid input lengths

			row = userInput[0:1]
			col = userInput[1:2]

			if 'm' in userInput:
				flag(translateToIndexValues(row, col))

			else: 
				sweep(translateToIndexValues(row, col))

		else: 
			print('Invalid input.')
			continue

	# printField(knownField)

	if checkWinCondition():
		print('You won!')
		print('In %s minutes and %s seconds.' % (int((time.time()-startTime)/60), round((time.time()-startTime)%60,5)))
		exit()