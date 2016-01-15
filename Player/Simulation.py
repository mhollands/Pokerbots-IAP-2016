import PokerPhysics as PP
import handEvalTable as evalTable
from itertools import combinations

#Picks random cards to fill out the table and runs multiple simulations to find an approximation for the win probability
'''
def simulate(myHand, boardCards, numBoardCards, numSimulations):
    wins = 0
    if (numBoardCards == 3 or numBoardCards == 4):
        for x in xrange(numSimulations):
            cardSet = set(boardCards)
            for card in myHand: cardSet.add(card)
            newCards = PP.generateHand(9-numBoardCards, cardSet)
            slicePoint = 5 - numBoardCards
            fakeBoard = boardCards + newCards[0:slicePoint]
            fakeOpponent = newCards[slicePoint:]
            myBest = PP.findBestHand(myHand, fakeBoard)
            opponentBest = PP.findBestHand(fakeOpponent, fakeBoard)
            if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage

    if(numBoardCards == 5):
        myBest = PP.findBestHand(myHand, boardCards)
        for x in xrange(0,numSimulations):
            cardSet = set(boardCards)
            for card in myHand: cardSet.add(card)
            fakeOpponent = PP.generateHand(4, cardSet)
            opponentBest = PP.findBestHand(fakeOpponent, boardCards)
            if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage
'''
#Picks random cards to fill out the table and runs multiple simulations to find an approximation for the win probability using eval table
def simulate(myHand, boardCards, numBoardCards, numSimulations, handEvalTable, translationDict):
    wins = 0
    handString = ''
    boardString = ''
    for card in myHand: handString += (str(evalTable.convertRoyaltyNum(card[0])) + card[1])
    for card in boardCards: boardString += (str(evalTable.convertRoyaltyNum(card[0])) + card[1])
    handString = evalTable.translateHand(handString)
    boardString = evalTable.translateHand(boardString)
    if (numBoardCards == 3 or numBoardCards == 4):
        for x in xrange(0,numSimulations): 
            newCards = generateHandString(9-numBoardCards, handString + boardString)
            fakeBoard = boardString + newCards[0:5-numBoardCards]
            fakeOpponent = newCards[5-numBoardCards:]
            myBest = findBestHand(handString, fakeBoard)
            opponentBest = findBestHand(fakeOpponent, fakeBoard)
            #if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
            if myBest[0] > opponentBest[0]: wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage
    
    if numBoardCards == 5:
        myBest = findBestHand(handString, boardString)
        for x in xrange(0,numSimulations): 
            fakeOpponent = generateHandString(4, handString + boardString)
            opponentBest = findBestHand(fakeOpponent, boardString, handEvalTable)
            #if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
            if myBest[0] > opponentBest[0]: wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage

def findBestHand(ourHand, tableHand, handEvalTable):
    #Generate all appropriate length combinations from the tableHand and ourHand
    #ourHandString = translateHand(ourHand)
    #tableString = translateHand(tableHand)
    ourCardsList = list(combinations(ourHand, 2))
    tableCardsList = list(combinations(tableHand, 3))
    
    #Combine the combinations into all possible hands and determine their values
    possibleHands = []
    for ourCombo in ourCardsList:
        for tableCombo in tableCardsList:
            hand = ourCombo + tableCombo
            handValue = evalTable.evaluateHand(hand)
            possibleHands.append((handValue,hand))

    bestVal = max(possibleHands, key = lambda x: x[0])

    #Sort the hands by value and then return the best
    #sortedByValue = sorted(sortHands, key = lambda x: (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4], x[0][5]), reverse = True)
    #print sortedByValue[0]
    return bestVal