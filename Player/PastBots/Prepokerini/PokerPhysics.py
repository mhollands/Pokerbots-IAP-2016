from itertools import combinations
from operator import itemgetter

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

	#Associate hands with their values (this could be combined with the previous step to save time if needed)
	handsTuples = []
	for hand in possibleHands:
		handValue = findHandValue(hand)
		handsTuples.append((handValue,hand))

	#Sort the hands by value and then return the best
	sortedByValue = sorted(handsTuples, key = lambda x: (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4], x[0][5]), reverse = True)
	return sortedByValue[0]

def findHandValue(hand):
	'''
	This function takes an input of one hand in the following format:
	
	hand = [(2,"h"),(3,"s"),(4,"d"),(14,"c"),(1,"h")]
	
	and returns the hand value in the following format:
	
	return [handType,most_important_card_number,..,..,..,least_important_car_number]
	
	handType: 8 = straight flush, 7 = 4 of a kind, 6 = full house, 5 = flush, 4 = straight
	3 = 3 of a kind, 2 = 2 pair, 1 = pair, 0 = high card
	'''
	#Sorts the hand into descending numeric order and creates a list of just the numbers numbers 
	sortedHand = sorted(hand, key=itemgetter(0), reverse = True)
	sortedNum = [card[0] for card in sortedHand]

	#Checks if there is a straight flush by first checking if there is a flush and storing that for later use and then checking if straight
	suit = hand[0][1]
	flush = False
	if suit == hand[1][1] and suit == hand[2][1] and suit == hand[3][1] and suit == hand[4][1]:
		flush = True
		if sortedNum[0] - sortedNum[4] == 4:
			return [8] + sortedNum
		if sortedNum[0] == 14 and sortedNum[1] == 5:
			return [8, 5, 4, 3, 2, 1]
		
	#Checks if there is a four of a kind
	if sortedNum[0] == sortedNum[1] and sortedNum[0] == sortedNum[2] and sortedNum[0] == sortedNum[3]:
		return [7, sortedNum[0], sortedNum[4], 0, 0, 0]
	elif sortedNum[1] == sortedNum[2] and sortedNum[1] == sortedNum[3] and sortedNum[1] == sortedNum[4]:
		return [7, sortedNum[1], sortedNum[0], 0, 0, 0]
		
	#Checks if there is a full house
	if sortedNum[0] == sortedNum[1] and sortedNum[0] == sortedNum[2] and sortedNum[3] == sortedNum[4]:
		return [6, sortedNum[0], sortedNum[4], 0, 0, 0]
	elif sortedNum[2] == sortedNum[3] and sortedNum[3] == sortedNum[4] and sortedNum[0] == sortedNum[1]:
		return [6, sortedNum[4], sortedNum[0], 0, 0, 0]
	
	#Checks if there is a flush using earlier result
	if flush:
		return [5] + sortedNum
		
	#Checks if there is a straight with a low Ace (Ace, 2,3,4,5)
	if sortedNum[0] == 14 and sortedNum[1] == 5 and sortedNum[2] == 4 and sortedNum[3] == 3 and sortedNum[4] == 2:
		return [4, 5, 4, 3, 2, 1]
	#Checks for any other straight
	straight = True
	for i in range(4):
		if not sortedNum[i] == sortedNum[i+1] + 1:
			straight = False
			break
	if straight:
		return [4] + sortedNum
	
	#Checks for 3 of a kind
	if sortedNum[0] == sortedNum[1] and sortedNum[0] == sortedNum[2]:
		return [3, sortedNum[0], sortedNum[3], sortedNum[4], 0, 0]
	elif sortedNum[1] == sortedNum[2] and sortedNum[1] == sortedNum[3]:
		return [3, sortedNum[1], sortedNum[0], sortedNum[4], 0, 0]
	elif sortedNum[2] == sortedNum[3] and sortedNum[2] == sortedNum[4]:
		return [3, sortedNum[2], sortedNum[0], sortedNum[1], 0, 0]
	
	#Checks for 2 pair
	if sortedNum[0] == sortedNum[1] and sortedNum[2] == sortedNum[3]:
		return [2, sortedNum[0], sortedNum[2], sortedNum[4], 0, 0]
	elif sortedNum[0] == sortedNum[1] and sortedNum[3] == sortedNum[4]:
		return [2, sortedNum[0], sortedNum[3], sortedNum[2], 0, 0]
	elif sortedNum[1] == sortedNum[2] and sortedNum[3] == sortedNum[4]:
		return [2, sortedNum[1], sortedNum[3], sortedNum[0], 0, 0]
	
	#Checks for a pair
	for i in range(4):
		if sortedNum[i] == sortedNum[i+1]:
			handType = [1, sortedNum[i]]
			for j in xrange(5):
				if not ((j == i) or (j == i+1)):
					handType.append(sortedNum[j])
			handType.append(0)
			handType.append(0)
			return handType
	
	
	#Returns the cards in descending order along with the information that there is only a high card
	return [0] + sortedNum

#isBetterHand is currently not used
def isBetterHand(handType1,handType2):
	'''
	This function takes an input of two hands in an array of tuples and 
	returns 1 if hand 1 is better is better 0 if equal and -1 if hand 2 is better
	
	e.g handType1 = [hand_type,most_important_card_number,..,..,..,least_important_car_number]
	
	'''
	for i in xrange(6):
		if handType1[i] > handType2[i]:
			return 1
		elif handType2[i] > handType1[i]:
			return -1
	
	return 0