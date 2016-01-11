import PokerPhysics as PP

#Picks random cards to fill out the table and runs multiple simulations to find an approximation for the win probability
def simulate(myHand, boardCards, numBoardCards, numSimulations):
    wins = 0
    if(numBoardCards == 3):
        for x in range(0,numSimulations):
            cardSet = set(boardCards)
            for card in myHand: cardSet.add(card)
            newCards = generateHand(6, cardSet)
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
            newCards = generateHand(5, cardSet)
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
            fakeOpponent = generateHand(4, cardSet)
            opponentBest = PP.findBestHand(fakeOpponent, boardCards)
            if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage