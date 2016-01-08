from itertools import combinations

#Chooses the optimal hand given the hold cards and the cards on the table
def findBestHand(ourHand, tableHand):

	#Generate all appropriate length combinations from the tableHand and ourHand
	our2Cards = combinations(ourHand, 2)
	table3Cards = combinations(tableHand, 3)

	#Combinations object is a generator so can only be iterated over once - converting to list
	ourCardsList = list(our2Cards)
	tableCardsList = list(table3Cards)
	
	#Combine the combinations into all possible hands
	possibleHands = []
	for ourCombo in ourCardsList:
		for tableCombo in tableCardsList:
			possibleHands.append(ourCombo + tableCombo)

	#Assosciate hands with their values (this could be combined with the previous step to save time if needed)
	handsTuples = []
	for hand in possibleHands:
		handValue = findHandValue(hand)
		handsTuples.append((handValue,hand))

	#Sort the hands by value and then return the best
	sortedByValue = sorted(handsTuples, key = lambda x: (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4], x[0][5]), reverse = True)
	return sortedByValue[0][1]