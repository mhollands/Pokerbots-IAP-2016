from operator import itemgetter

def findHandValue(hand):
	'''
	This function takes an input of one hand in the following format:
	hand = [(2,"h"),(3,"s"),(4,"d"),(14,"c"),(1,"h")]
	and returns the hand value in the following format:
	return [handType,most_important_card_number,..,..,..,least_important_car_number]
	handType: 8 = straight flush, 7 = 4 of a kind, 6 = full house, 5 = flush, 4 = straight
	3 = 3 of a kind, 2 = 2 pair, 1 = pair, 0 = high card
	'''

	sortedHand = sorted(hand, key=itemgetter(0), reverse = True)
	sortedNum = [card[0] for card in sortedHand]

	#check straight flush
	suit = hand[0][1]
	flush = False
	if suit == hand[1][1] and suit == hand[2][1] and suit == hand[3][1] and suit == hand[4][1]:
		flush = True
		if sortedNum[0] - sortedNum[4] == 4:
			return [8] + sortedNum
		if sortedNum[0] == 14 and sortedNum[1] == 5:
			return [8, 5, 4, 3, 2, 1]
		
	#check 4 of a kind	
	if sortedNum[0] == sortedNum[1] and sortedNum[0] == sortedNum[2] and sortedNum[0] == sortedNum[3]:
		return [7, sortedNum[0], sortedNum[4], 0, 0, 0]
	elif sortedNum[1] == sortedNum[2] and sortedNum[1] == sortedNum[3] and sortedNum[1] == sortedNum[4]:
		return [7, sortedNum[1], sortedNum[0], 0, 0, 0]
		
	#check full house
	if sortedNum[0] == sortedNum[1] and sortedNum[0] == sortedNum[2] and sortedNum[3] == sortedNum[4]:
		return [6, sortedNum[0], sortedNum[4], 0, 0, 0]
	elif sortedNum[2] == sortedNum[3] and sortedNum[3] == sortedNum[4] and sortedNum[0] == sortedNum[1]:
		return [6, sortedNum[4], sortedNum[0], 0, 0, 0]
	
	#check flush
	if flush:
		return [5] + sortedNum
		
	#check straight
	if sortedNum[0] == 14 and sortedNum[1] == 5 and sortedNum[2] == 4 and sortedNum[3] == 3 and sortedNum[4] == 2:
		return [4, 5, 4, 3, 2, 1]
	straight = True
	for i in range(3):
		if not sortedNum[i] == sortedNum[i+1] + 1:
			straight = False
			break
	if straight:
		return [4] + sortedNum
	
	#check 3 of a kind
	if sortedNum[0] == sortedNum[1] and sortedNum[0] == sortedNum[2]:
		return [3, sortedNum[0], sortedNum[3], sortedNum[4], 0, 0]
	elif sortedNum[1] == sortedNum[2] and sortedNum[1] == sortedNum[3]:
		return [3, sortedNum[1], sortedNum[0], sortedNum[4], 0, 0]
	elif sortedNum[2] == sortedNum[3] and sortedNum[2] == sortedNum[4]:
		return [3, sortedNum[2], sortedNum[0], sortedNum[1], 0, 0]
	
	#check 2 pair
	if sortedNum[0] == sortedNum[1] and sortedNum[2] == sortedNum[3]:
		return [2, sortedNum[0], sortedNum[2], sortedNum[4], 0, 0]
	elif sortedNum[0] == sortedNum[1] and sortedNum[3] == sortedNum[4]:
		return [2, sortedNum[0], sortedNum[3], sortedNum[2], 0, 0]
	elif sortedNum[1] == sortedNum[2] and sortedNum[3] == sortedNum[4]:
		return [2, sortedNum[1], sortedNum[3], sortedNum[0], 0, 0]
	
	#check pair
	for i in range(4):
		if sortedNum[i] == sortedNum[i+1]:
			handType = [1, sortedNum[i]]
			for j in range(4):
				if not (j == i) or (j==i+1):
					handType.append(sortedNum[j])
			handType.append(0)
			return handType
	
	
	#check high card
	return [0] + sortedNum




def isBetterHand(handType1,handType2):
	'''
	This function takes an input of two hands in an array of tuples
	and returns 1 if hand 1 is better is better 0 if equal and
	-1 if hand 2 is better
	
	e.g handType1 = [hand_type,most_important_card_number,..,..,..,least_important_car_number]
	
	'''
	for i in xrange(6):
		if handType1[i] > handType2[i]:
			return 1
		elif handType2[i] > handType1[i]:
			return -1
	
	return 0
	
if __name__ == '__main__':
	print findHandValue([(14,"h"),(3,"h"),(8,"h"),(5,"c"),(2,"h")])