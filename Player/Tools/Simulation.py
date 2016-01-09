import PokerPhysics as PP

#Picks random cards to fill out the table and runs multiple simulations to find an approximation for the win probability
def simulate(myHand, boardCards, numBoardCards, numSimulations):
    if(numBoardCards == 3):
        wins = 0
        for x in range(0,numSimulations):
            cardSet = set(boardCards)
            for card in myHand: cardSet.add(card)
            newCards = []
            for i in range(0,6):
                card = PP.pickRandomCard(cardSet)
                cardSet.add(card)
                newCards.append(card)
            fakeBoard = boardCards + newCards[0:2]
            fakeOpponent = newCards[2:]
            myBest = PP.findBestHand(myHand, fakeBoard)
            opponentBest = PP.findBestHand(fakeOpponent, fakeBoard)
            if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage

    if(numBoardCards == 4):
        wins = 0
        for x in range(0,numSimulations):
            cardSet = set(boardCards)
            for card in myHand: cardSet.add(card)
            newCards = []
            for i in range(0,5):
                card = PP.pickRandomCard(cardSet)
                cardSet.add(card)
                newCards.append(card)
            fakeBoard = boardCards + newCards[0:1]
            fakeOpponent = newCards[1:]
            myBest = PP.findBestHand(myHand, fakeBoard)
            opponentBest = PP.findBestHand(fakeOpponent, fakeBoard)
            if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage

    if(numBoardCards == 5):
        wins = 0
        myBest = PP.findBestHand(myHand, boardCards)
        for x in range(0,numSimulations):
            cardSet = set(boardCards)
            for card in myHand: cardSet.add(card)
            fakeOpponent = []
            for i in range(0,4):
                card = PP.pickRandomCard(cardSet)
                cardSet.add(card)
                fakeOpponent.append(card)
            opponentBest = PP.findBestHand(fakeOpponent, boardCards)
            if PP.isBetterHand(myBest[0], opponentBest[0]) == 1 : wins+=1
        winPercentage = 1.0*wins/numSimulations
        return winPercentage