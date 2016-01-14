import PokerPhysics as PP
from itertools import combinations
from operator import itemgetter
import random
import csv
import time
import string
import Simulation

def createEvalCSV():
	allCards = []
	for num in xrange(2,15):
		for suit in ['c','d','h','s']:
			allCards.append((num, suit))
	translationDict = loadTranslationDict()
	allHands = combinations(allCards,5)

	handFile = open('handFile.csv', 'wt')
	writer = csv.writer(handFile)
	for hand in allHands:
		hand = sorted(hand, key= lambda x: (x[0], x[1]), reverse = True)
		handValue = PP.findHandValue(hand)
		handString = ''
		for card in hand:
			'''
			handString += (str(card[0]) + card[1])
			'''
			key = str(card[0]) + card[1]
			handString += translationDict[key]
		handValueString = ''
		for num in handValue:
			handValueString += str(convertRoyaltyNum(num))
		writer.writerow((handString , handValueString))
	return 0


def generateCardList():
	allCards = []
	for num in xrange(2,15):
		for suit in ['c','d','h','s']:
			allCards.append(str(num) + suit)
	return allCards

def loadHandEval():
	handEvalDict = dict()
	with open('handFile.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			#print row[0]
			handValue = []
			for num in row[1]:
				handValue.append(int(reverseRoyaltyConvert(num)))
			keyString = row[0]
			handEvalDict[keyString]  = handValue
	return handEvalDict

def generateHandString(numCards,cardString):
	handString = ''
	for i in xrange(numCards):
		card = pickRandomCard(cardString)
		handString += card
		cardString += card
		#print cardString
		#print handString
	handString = ''.join(sorted(handString))
	return handString

def pickRandomCard(cardString):
	while True:
		num = random.randint(0,51)
		card = string.ascii_letters[num]
		#card = random.choice(string.ascii_letters)
		#card = random.choice('QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm')
		if card not in cardString:
			return card

def evaluateHand(hand):
	hand = ''.join(sorted(hand, reverse = True))
	#print hand
	handValue = handEvalDict[hand]
	#print handValue
	return handValue

def convertRoyaltyTP(card):
	cardValue = convertRoyaltyNum(card[0])
	card = (cardValue, card[1])
	return card

def loadTranslationDict():
	allCards = generateCardList()
	translationDict = dict(zip(allCards, string.ascii_uppercase + string.ascii_lowercase))
	return translationDict

def convertRoyaltyNum(num):
	if num == 10:
		return 'T'
	if num == 11:
		return 'J'
	if num == 12:
		return 'Q'
	if num == 13:
		return 'K'
	if num == 14:
		return "A"
	return num

def reverseRoyaltyConvert(num):
	if num == 'T':
		return 10
	if num == 'J':
		return 11
	if num == 'Q':
		return 12
	if num == 'K':
		return 13
	if num == 'A':
		return 14
	return num

def translateHand(hand):
	numCards = len(hand)/2
	handString = ''
	for i in range(numCards):
		key = str(reverseRoyaltyConvert(hand[2*i])) + hand[2*i + 1]
		handString += translationDict[key]
	return handString

def findBestHand(ourHand, tableHand):

	#Generate all appropriate length combinations from the tableHand and ourHand
	#ourHandString = translateHand(ourHand)
	#tableString = translateHand(tableHand)
	ourCardsList = list(combinations(ourHand, 2))
	tableCardsList = list(combinations(tableHand, 3))
	
	#Combine the combinations into all possible hands and determine their values
	possibleHands = []
	currentMax = 0
	for ourCombo in ourCardsList:
		for tableCombo in tableCardsList:
			hand = ourCombo + tableCombo
			handValue = evaluateHand(hand)
			if handValue[0] >= currentMax:
				currentMax = handValue[0]
				possibleHands.append((handValue,hand))

	#Cut the sortable list down to just maximum category hands
	sortHands = []
	for hand in possibleHands:
		if hand[0][0] == currentMax:
			sortHands.append(hand)

	#Sort the hands by value and then return the best
	sortedByValue = sorted(sortHands, key = lambda x: (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4], x[0][5]), reverse = True)
	#print sortedByValue[0]
	return sortedByValue[0]

def simulate2(myHand, boardCards, numBoardCards, numSimulations):
	wins = 0
	handString = ''
	boardString = ''
	for card in myHand: handString += (str(convertRoyaltyNum(card[0])) + card[1])
	for card in boardCards: boardString += (str(convertRoyaltyNum(card[0])) + card[1])
	handString = translateHand(handString)
	boardString = translateHand(boardString)
	for x in xrange(0,numSimulations): 
		#print handString + boardString
		newCards = generateHandString(9-numBoardCards, handString + boardString)
		'''
		newCardList = PP.generateHand(9-numBoardCards, set(myHand + boardCards))
		newCards = ''
		for card in newCardList:
			newCards +=translateHand((str(convertRoyaltyNum(card[0])) + card[1]))
		'''
		fakeBoard = boardString + newCards[0:5-numBoardCards]
		#print fakeBoard
		fakeOpponent = newCards[5-numBoardCards:]
		#print fakeOpponent
		myBest = findBestHand(handString, fakeBoard)
		opponentBest = findBestHand(fakeOpponent, fakeBoard)
		if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1

	winPercentage = 1.0*wins/numSimulations

	return winPercentage

'''
def simulate(myHand, boardCards, numBoardCards, numSimulations):
	wins = 0
	if(numBoardCards == 3):
		for x in xrange(0,numSimulations):
			cardSet = set(boardCards)
			for card in myHand: cardSet.add(card)
			newCards = PP.generateHand(6, cardSet)
			fakeBoard = boardCards + newCards[0:2]
			fakeOpponent = newCards[2:]
			myBest = PP.findBestHand(myHand, fakeBoard)
			opponentBest = PP.findBestHand(fakeOpponent, fakeBoard)
			if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
		winPercentage = 1.0*wins/numSimulations
		return winPercentage

	if(numBoardCards == 4):
		for x in xrange(0,numSimulations):
			cardSet = set(boardCards)
			for card in myHand: cardSet.add(card)
			newCards = PP.generateHand(5, cardSet)
			fakeBoard = boardCards + newCards[0:1]
			fakeOpponent = newCards[1:]
			myBest = PP.findBestHand(myHand, fakeBoard)
			opponentBest = PP.findBestHand(fakeOpponent, fakeBoard)
			if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
		winPercentage = 1.0*wins/numSimulations
		return winPercentage

	if(numBoardCards == 5):
		myBest = PP.findBestHand(myHand, boardCards)
		print myBest
		for x in xrange(0,numSimulations):
			cardSet = set(boardCards)
			for card in myHand: cardSet.add(card)
			fakeOpponent = PP.generateHand(4, cardSet)
			opponentBest = PP.findBestHand(fakeOpponent, boardCards)
			if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
		winPercentage = 1.0*wins/numSimulations
		return winPercentage
'''
if __name__ == '__main__':
	print string.ascii_letters
	translationDict = loadTranslationDict()
	#createEvalCSV()
	start =time.time()
	handEvalDict = loadHandEval()
	end =time.time()
	print end -start
	hand = [(3,"h"),(3,"s"),(4,"d"),(8,"c")]
	board = [(14,"d"),(14,"s"),(12,"d")]
	start =time.time()
	print Simulation.simulate(hand, board,3,1000)
	end =time.time()
	print end - start
	start =time.time()
	print simulate2(hand, board,3,1000)
	end =time.time()
	print end - start
	'''
	start =time.time()
	print simulate([(2,"h"),(3,"s"),(4,"d"),(14,"c")],[(2,"d"),(7,"d"),(12,"h"),(11,"d")],4,1)
	end =time.time()
	print end -start
	start =time.time()
	print simulate2([(2,"h"),(3,"s"),(4,"d"),(14,"c")],[(2,"d"),(7,"d"),(12,"h"),(11,"d")],4,1)
	end =time.time()
	print end -start
	'''
	for i in range(100):
		myHand = [(2,"h"),(12,"s"),(4,"s"),(14,"c")]
		boardCards = PP.generateHand(5,set(myHand))
		handString = ''
		boardString = ''
		for card in myHand: handString += (str(convertRoyaltyNum(card[0])) + card[1])
		for card in boardCards: boardString += (str(convertRoyaltyNum(card[0])) + card[1])
		handString = translateHand(handString)
		boardString = translateHand(boardString)
		sim2 = findBestHand(handString, boardString)[0]
		sim1 = PP.findBestHand(myHand, boardCards)[0]
		if sim1 != sim2:
			print boardCards
			print sim1
			print sim2

	print 'done'
	'''
	start =time.time()
	print simulate([(2,"h"),(3,"s"),(4,"d"),(14,"c")],[(2,"d"),(7,"d"),(12,"h"),(11,"d"),(10,"s")],5,10)
	end =time.time()
	start =time.time()
	print simulate2([(2,"h"),(3,"s"),(4,"d"),(14,"c")],[(2,"d"),(7,"d"),(12,"h"),(11,"d"),(10,"s")],5,10)
	end =time.time()
	print end -start
	'''