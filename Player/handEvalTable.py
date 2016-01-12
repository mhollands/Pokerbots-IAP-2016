import PokerPhysics as PP
from itertools import combinations
from operator import itemgetter
import csv
import time

def createEvalCSV():
	allCards = []

	for num in xrange(2,15):
		for suit in ['h','c','d','s']:
			allCards.append((num, suit))


	allHands = combinations(allCards,5)

	handFile = open('handFile.csv', 'wt')
	writer = csv.writer(handFile)
	for hand in allHands:
		hand = sorted(hand, key= lambda x: (x[0], x[1]), reverse = True)
		handValue = PP.findHandValue(hand)
		handString = ''
		for card in hand:
			card = convertRoyaltyTP(card)
			handString += (str(card[0]) + card[1])
		handValueString = ''
		for num in handValue:
			handValueString += str(convertRoyaltyNum(num))

		writer.writerow((handString , handValueString))

	return 0

def loadHandEval():
	handEvalDict = dict()
	with open('handFile.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			#print row[0]
			handEvalDict[row[0]]  = row[1]
	return handEvalDict

def generateHandString(hand):
	hand = sorted(hand, key= lambda x: (x[0], x[1]), reverse = True)
	handString = ''
	for card in hand:
		card = convertRoyaltyTP(card)
		num = str(card[0])
		handString += (num + card[1])
	return handString

def evaluateHand(hand):
	handString = generateHandString(hand)
	handValue = handEvalDict[handString]
	return handValue


def convertRoyaltyTP(card):
	cardValue = convertRoyaltyNum(card[0])
	card = (cardValue, card[1])
	return card


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


def simulate(myHand, boardCards, numBoardCards, numSimulations):
    wins = 0
    if(numBoardCards == 3):
        for x in range(0,numSimulations):
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
        for x in range(0,numSimulations):
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
        for x in range(0,numSimulations):
            cardSet = set(boardCards)
            for card in myHand: cardSet.add(card)
            fakeOpponent = PP.generateHand(4, cardSet)
            opponentBest = PP.findBestHand(fakeOpponent, boardCards)
            if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage

def simulate2(myHand, boardCards, numBoardCards, numSimulations):
    wins = 0
    if(numBoardCards == 3):
        for x in range(0,numSimulations):
            cardSet = set(boardCards)
            for card in myHand: cardSet.add(card)
            newCards = PP.generateHand(6, cardSet)
            fakeBoard = boardCards + newCards[0:2]
            fakeOpponent = newCards[2:]
            myBest = findBestHand(myHand, fakeBoard)
            opponentBest = findBestHand(fakeOpponent, fakeBoard)
            if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage

    if(numBoardCards == 4):
        for x in range(0,numSimulations):
            cardSet = set(boardCards)
            for card in myHand: cardSet.add(card)
            newCards = PP.generateHand(5, cardSet)
            fakeBoard = boardCards + newCards[0:1]
            fakeOpponent = newCards[1:]
            myBest = findBestHand(myHand, fakeBoard)
            opponentBest = findBestHand(fakeOpponent, fakeBoard)
            if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage

    if(numBoardCards == 5):
        myBest = PP.findBestHand(myHand, boardCards)
        for x in range(0,numSimulations):
            cardSet = set(boardCards)
            for card in myHand: cardSet.add(card)
            fakeOpponent = PP.generateHand(4, cardSet)
            opponentBest = findBestHand(fakeOpponent, boardCards)
            if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage

def findBestHand(ourHand, tableHand):

	#Generate all appropriate length combinations from the tableHand and ourHand
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
	return sortedByValue[0]


if __name__ == '__main__':
	#createEvalCSV()
	start =time.time()
	handEvalDict = loadHandEval()
	end =time.time()
	print end -start
	start =time.time()
	simulate([(2,"h"),(3,"s"),(4,"d"),(14,"c")],[(2,"d"),(7,"d"),(12,"h")],3,1000)
	end =time.time()
	print end -start
	start =time.time()
	simulate2([(2,"h"),(3,"s"),(4,"d"),(14,"c")],[(2,"d"),(7,"d"),(12,"h")],3,1000)
	end =time.time()
	print end -start
