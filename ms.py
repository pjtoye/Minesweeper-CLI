import random

# Settings
BOMBS = 4

# Print a field with cols and rows
def printField(inputField):
	print('------------------------------------------------------------------')

	cols = ['X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
	print('\t'.join(cols))

	rows = ['1','2','3','4','5','6','7','8']

	for x in range(0, len(inputField)):
		print('\t'.join([rows[x]] + inputField[x]))

	print('------------------------------------------------------------------')

# Plant bombs in the field
def plantBombs():

	# Generate X unique numbers between 0 and 63
	bombPositions = []
	while len(bombPositions) < BOMBS:
		pos = random.randint(0, 63)
		if pos not in bombPositions:
			bombPositions.append(pos)

	# Plant bombs in field
	for pos in bombPositions:
		field[int(pos/8)][pos%8] = '💣'

# Calculate surrounding number of bombs for all non-bomb positions
def calculateFieldNumbers():
	
	# For every field position
	for x in range(0, 8):
		for y in range(0, 8):
			
			if (field[x][y] != '💣'):

				bombsAtBorders = 0

				# Check all neighbours
				for a in range(-1, 2):
					for b in range(-1, 2):
						if (x + a >= 0) and (x + a <= 7) and (y + b >= 0) and (y + b <= 7): # valid position
							
							if (field[x+a][y+b] == '💣'):
								bombsAtBorders += 1

				field[x][y] = str(bombsAtBorders)

def translateToCoordinates(row, col):
	rows = ['1','2','3','4','5','6','7','8']
	cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

	return rows.index(row), cols.index(col)

# Puts a flag (flag='f') or uncovers the field (no third argument passed)
def updateKnownField(x, y, flag=None):
	if flag == 'f':
		knownField[x][y] = '⚑'
	else:
		knownField[x][y] = field[x][y]
		if field[x][y] == '0':
			uncoverZeroesAndTheirNeighbours(x, y)

def uncoverZeroesAndTheirNeighbours(x, y):
	knownField[x][y] = field[x][y]
		
	for a in range(-1, 2):
		for b in range(-1, 2):
			if (x + a >= 0) and (x + a <= 7) and (y + b >= 0) and (y + b <= 7): # valid position
				
				if(field[x+a][y+b]=='0' and knownField[x+a][y+b]!='0'): # Check if knownField isn't set to zero yet (first line of function) to prevent infinite recursion from occuring
					uncoverZeroesAndTheirNeighbours(x+a,y+b)

				knownField[x+a][y+b] = field[x+a][y+b]

def sweep(row, col):
	x, y = translateToCoordinates(row, col)

	if field[x][y] == '💣':
		return 'death'
	else:
		updateKnownField(x, y)
		return 'success'

def flag(row, col):
	x, y = translateToCoordinates(row, col)
	updateKnownField(x, y, 'f')		

def checkWinCondition():
	flags = 0
	for x in range(0, 8):
		for y in range(0, 8):
			
			if knownField[x][y] == '*': # Player has remaining uncleared fields
				return False

			if knownField[x][y] == '⚑':
				flags += 1

	if flags == BOMBS:
		return True

# Build field
field = []
knownField = []

for x in range(8):
	field.append(['*','*','*','*','*','*','*','*'])
	knownField.append(['*','*','*','*','*','*','*','*'])

# Setup
plantBombs()
calculateFieldNumbers()

# Print game instructions
print("Welcome to Minesweeper!\nType \'q\' to quit the game.\n"
	  "Enter row number and column letter to sweep (eg \'1A\').\n"
	  "Add an \'m\' to flag that field (eg 1Am).")

# Start main game loop
printField(knownField)

while True:
	userInput = input('>') 

	if userInput == 'q':
		print('K thx bye')
		exit()

	else:
		row = userInput[0:1]
		col = userInput[1:2]

		if 'm' in userInput:
			flag(row, col)

		else: 
			outcome = sweep(row, col)

			if outcome == 'death':
				print('Kabooom!\nGame over!')
				printField(field)
				exit()

		printField(knownField)

		if checkWinCondition():
			print('You won!')
			exit()