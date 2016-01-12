import PokerPhysics as PP
from itertools import combinations
from operator import itemgetter
import time

def createHandEval():

	#creates a list of all possible cards
	#allCards = [(2,"h"),(3,"s"),(4,"d"),(12,"c"),(1,"h")]
	allCards = []

	
	for num in xrange(2,15):
		for suit in ['h','c','d','s']:
			allCards.append((num, suit))

	#creates a generator of all possible 5 card hands
	allHands = combinations(allCards,5)

	handFile = open('allHands.txt', 'w')

	for hand in allHands:
		hand = sorted(hand, key= lambda x: (x[0], x[1]), reverse = True)
		handValue = PP.findHandValue(hand)
	
		line = ''
		for card in hand:
			card = convertRoyaltyTP(card)
			line += (str(card[0]) + card[1])
		for num in handValue:
			line += str(convertRoyaltyNum(num))
		#handFile.write((hand, handValue)
		line += '\n'
		handFile.write(line)
	

	handFile.close()

	#handFile.open('allHands.txt', 'r)
	#numLines = sum(1 for line in open('allHands.txt'))
	return 0

def convertRoyaltyNum(num):
	if num == 10:
		num = 'T'
	elif num == 11:
		num = 'J'
	elif num == 12:
		num = 'Q'
	elif num == 13:
		num = 'K'
	elif num == 14:
		num = "A"
	return num

def reverseRoyaltyConvert(num):
	if num == 'T':
		num = 10
	elif num == 'J':
		num = 11
	elif num == 'Q':
		num = 12
	elif num == 'K':
		num = 13
	elif num == 'A':
		num = 14
	return num


def convertRoyaltyTP(card):
	cardValue = convertRoyaltyNum(card[0])
	card = (cardValue, card[1])

	return card

def loadHandEval():
    handEvalDict = dict()
    with open('allHands.txt') as handFile:
        for line in handFile:
        	evaluation = line[10:-1]
        	handValue = []
        	for num in evaluation:
        		value = int(reverseRoyaltyConvert(num))
        		handValue.append(value)
        	keyString = line[0:10]
        	keyList = []
        	for i in xrange(5):
        		num = reverseRoyaltyConvert(keyString[2*i])
        		keyList.append((int(num), keyString[2*i +1] ))
			handEvalDict[tuple(keyList)] = handValue
    return handEvalDict

if __name__ == '__main__':
	#createHandEval()
	handEvalDict = loadHandEval()

	#print handEvalDict['2h2c2d2s3h']
	testHands = []
	for i in xrange(10000):
		testHand = PP.generateTestHand(5)
		testHands.append(testHand)
	start = time.time()
	for j in xrange(10000):
		testHands[j] = tuple(sorted(testHands[j], key= lambda x: (x[0], x[1]), reverse = True))
	end = time.time()
	print(end - start)
	start = time.time()
	for hand in testHands:
		handValue = handEvalDict[hand]
	end = time.time()
	print(end - start)
	start = time.time()
	for hand in testHands:
		handValue = PP.findHandValue(hand)
	end = time.time()
	print end -start

	#print testHand