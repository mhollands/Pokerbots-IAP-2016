from itertools import combinations
from operator import itemgetter
import random
import csv
import time
import string
import PokerPhysics as PP

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
			key = str(card[0]) + card[1]
			handString += translationDict[key]
		handValueString = ''
		for num in handValue:
			if num < 10: addHand = "0" + str(num)
			else: addHand = str(num)
			handValueString += addHand
		writer.writerow((handString , handValueString))
	return 0

def generateCardList():
	allCards = []
	for num in xrange(2,15):
		for suit in ['c','d','h','s']:
			allCards.append(str(num) + suit)
	return allCards

def pickRandomCard(cardString):
	while True:
		card = random.choice(string.ascii_letters)
		if card not in cardString:
			return card

def loadHandEval():
	handEvalDict = dict()
	with open('handFile.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			handEvalDict[row[0]] = int(row[1])
			"""handValue = []
			for num in row[1]:
				handValue.append(int(reverseRoyaltyConvert(num)))
			keyString = row[0]
			handEvalDict[keyString]  = handValue"""
	return handEvalDict

def generateHandString(numCards,cardString):
	handString = ''
	for i in xrange(numCards):
		card = pickRandomCard(cardString)
		handString += card
		cardString += card
	return handString

def evaluateHand(hand, handEvalDict):
	hand = ''.join(sorted(hand, reverse = True))
	handValue = handEvalDict[hand]
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

def translateHand(hand, translationDict):
	numCards = len(hand)/2
	handString = ''
	for i in range(numCards):
		key = str(reverseRoyaltyConvert(hand[2*i])) + hand[2*i + 1]
		handString += translationDict[key]

	return handString

def translateHandToStringType(hand, translationDict):
	numCards = len(hand)
	handString = ''
	for i in range(numCards):
		key = str(reverseRoyaltyConvert(hand[i][0])) + hand[i][1]
		handString += translationDict[key]

	return handString
