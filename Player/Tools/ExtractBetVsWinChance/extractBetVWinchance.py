import Pokerini 
import PokerPhysics as PP
import Simulation

myName = ''
opponentName = ''
myBet = 0
opponentBet = 0 
myPot = 0
opponentPot = 0
iAgreeWithBet = False
opponentAgreesWithBet = False
numBoardCards = 0
boardCards = []

opponentRound0Folds = 0
opponentRound1Folds = 0
opponentRound2Folds = 0
opponentRound3Folds = 0

preflopBets = []
postflopBets = []
turnBets = []
riverBets = []

d = Pokerini.pokeriniInitialise()

    #If both players agree on bet, moves bet to pot
def updatePot():
    global iAgreeWithBet, opponentAgreesWithBet, myPot, myBet, opponentPot, opponentBet
    if(iAgreeWithBet and opponentAgreesWithBet):
        myPot = myPot + myBet
        myBet = 0
        opponentPot = opponentPot + opponentBet
        opponentBet = 0
        iAgreeWithBet = False
        opponentAgreesWithBet = False

#handles actions performed between GetAction packets
def parsePerformedAction(performedAction):
    words = performedAction.split(':')
    if(words[0] == "POST"):
        handlePerformedActionPost(words)
        return
    if(words[0] == "CALL"):
        handlePerformedActionCall(words)
        return
    if(words[0] == "RAISE"):
        handlePerformedActionRaise(words)
        return
    if(words[0] == "BET"):
        handlePerformedActionBet(words)
        return
    if(words[0] == "CHECK"):
        handlePerformedActionCheck(words)
        return
    if(words[0] == "DEAL"):
        handlePerformedActionDeal(words)
        return
    if(words[0] == "FOLD"):
        handlePerformedActionFold(words)
        return
    if(words[0] == "SHOW"):
        handlePerformedActionShow(words)
        return

def handlePerformedActionShow(words):
    global opponentName
    global numBoardCards
    global preflopBets
    global postflopBets
    global turnBets
    global riverBets
    global boardCards
    global d

    if(words[5] == opponentName):
        opponentHand = []
        for card in words[1:5]:
            opponentHand.append(parseCard(card))
        preflopRating = Pokerini.pokeriniLookup(opponentHand, d)
        print str(preflopRating)+","+','.join(preflopBets)
        if(numBoardCards >= 3):
            postflopRanking = Simulation.simulateOld(opponentHand, boardCards[0:3], 3, 100)
            print str(postflopRanking)+","+','.join(postflopBets)
        if(numBoardCards >= 4):
            turnRanking = Simulation.simulateOld(opponentHand, boardCards[0:4], 4, 100)
            print str(turnRanking)+","+','.join(turnBets)
        if(numBoardCards == 5):
            riverRanking = Simulation.simulateOld(opponentHand, boardCards[0:5], 5, 100)
            print str(riverRanking)+","+','.join(riverBets)

def handlePerformedActionFold( words):
    global numBoardCards, opponentName, opponentRound0Folds, opponentRound1Folds, opponentRound2Folds, opponentRound3Folds
    if(words[1] == opponentName):
        if(numBoardCards == 0):
            opponentRound0Folds += 1
        if(numBoardCards == 3):
            opponentRound1Folds += 1
        if(numBoardCards == 4):
            opponentRound2Folds += 1
        if(numBoardCards == 5):
            opponentRound3Folds += 1

def handlePerformedActionDeal( words):
    global numBoardCards
    if(numBoardCards == 0):
        numBoardCards = 3
        return
    numBoardCards += 1

def handlePerformedActionCheck( words):
    global myName, iAgreeWithBet, opponentAgreesWithBet
    if(words[1] == myName):
        iAgreeWithBet = True
        return
    opponentAgreesWithBet = True

#updates myBet or opponentBet
def handlePerformedActionBet( words):
    global myName, iAgreeWithBet, opponentAgreesWithBet, opponentBet, myBet 
    if(words[2] == myName):
        myBet = int(words[1])
        iAgreeWithBet = True
        opponentAgreesWithBet = False
        return
    logBet(int(words[1]))
    opponentBet = int(words[1])
    iAgreeWithBet = False
    opponentAgreesWithBet = True

    #updates myBet or opponentBet
def handlePerformedActionRaise(words):
    global myName, opponentBet, myBet, iAgreeWithBet, opponentAgreesWithBet
    if(words[2] == myName):
        myBet = int(words[1])
        iAgreeWithBet = True
        opponentAgreesWithBet = False
        return
    logBet(int(words[1])) # remember that they betted this ammount
    opponentBet = int(words[1])
    iAgreeWithBet = False
    opponentAgreesWithBet = True

def logBet(opponentBet):
    global preflopBets, postflopBets, turnBets, riverBets, numBoardCards
    maxBet = calculateMaxOpponentBet()
    minBet = calculateMinOpponentBet(maxBet)
    if(minBet == maxBet):
        percentage = -1.0
    else:
        percentage = 1.0 * (opponentBet - minBet) / (maxBet - minBet)
    if(numBoardCards == 0):
        preflopBets.append(str(percentage))
    if(numBoardCards == 3):
        postflopBets.append(str(percentage))
    if(numBoardCards == 4):
        turnBets.append(str(percentage))
    if(numBoardCards == 5):
        riverBets.append(str(percentage))

def calculateMaxOpponentBet():
    global myBet, opponentBet, myPot, opponentPot
    pot = myBet + opponentBet + myPot + opponentPot
    maxRaise = myBet*2 - opponentBet + pot;
    if(maxRaise > 400 - opponentPot):
        maxRaise = 400 - opponentPot
    return maxRaise

def calculateMinOpponentBet(maxRaise):
    global myBet, opponentBet, myPot, opponentPot
    delta = myBet - opponentBet
    if(delta < 2):
        delta = 2
    minRaise = myBet + delta
    if(minRaise > maxRaise):
        minRaise = maxRaise
    return minRaise

#updates myBet or opponentBet - but doesn't agree with documentation
def handlePerformedActionCall(words):
    global myBet
    global opponentBet
    global opponentAgreesWithBet
    global iAgreeWithBet
    global MyName
    if(words[1] == myName):
        myBet = opponentBet
        iAgreeWithBet = True
        return
    opponentBet = myBet
    opponentAgreesWithBet = True

#updates either myBet or opponentBet based on the blinds
def handlePerformedActionPost(words):
    global myBet
    global opponentBet
    if(words[2] == myName):
        myBet = int(words[1])
        iAgreeWithBet = False
        return
    opponentBet = int(words[1])
    opponentAgreesWithBet = False

def handlePacketGetAction(words):  
    global boardCards
    numBoardCardsListed = int(words[2])
    del boardCards[:] #clear board cards list
    for word in range(3,3 + numBoardCardsListed): #add board cards to list
        boardCards.append(parseCard(words[word]))

    numPerformedActions = int(words[3 + numBoardCardsListed]) #get the number of actions performed since my last `
    for word in range(4 + numBoardCardsListed, 4 + numBoardCardsListed + numPerformedActions): #parse every performed action
        parsePerformedAction(words[word]) #update variables depending on performedActions
        updatePot() #update the pot 

#takes string such as "Qs" and returns tuple of (11,s)
def parseCard(cardString):
    number = cardString[0]
    if(number == "T"):
        number = 10
    if(number == "J"):
        number = 11
    if(number == "Q"):
        number = 12
    if(number == "K"):
        number = 13
    if(number == "A"):
        number = 14
    return (int(number), cardString[1])

#updates myName, opponentName, myStackSize, bigBlind, totalNumHands
def handlePacketNewGame( words):
    global myName
    global opponentName
    global iAgreeWithBet
    global opponentAgreesWithBet
    myName = words[1]
    opponentName = words[2]
    iAgreeWithBet = False
    opponentAgreesWithBet = False

#updates handId, myHand, myStack, opponentStack, myBet
def handlePacketNewHand( words):
    global myBet, opponentBet, myPot, opponentPot, boardCards, iAgreeWithBet, opponentAgreesWithBet, preflopBets, postflopBets, turnBets, riverBets, numBoardCards
    myBet = 0 #reset myBet
    opponentBet = 0 #reset opponentBet
    myPot = 0 #reset myPot
    opponentPot = 0 #reset opponentPot
    del boardCards[:] #reset boardCards
    numBoardCards = 0 
    iAgreeWithBet = False
    opponentAgreesWithBet = False
    del preflopBets[:]
    del postflopBets[:]
    del turnBets[:]
    del riverBets[:]

def handlePacketHandOver( words):
    numBoardCardsListed = int(words[3])
    del boardCards[:] #clear board cards list
    for word in range(4,4 + numBoardCardsListed): #add board cards to list
        boardCards.append(parseCard(words[word]))
    numPerformedActions = int(words[4 + numBoardCardsListed]) #get the number of actions performed since my last action
    for word in range(5 + numBoardCardsListed, 5 + numBoardCardsListed + numPerformedActions): #parse every performed action
        parsePerformedAction(words[word]) #update variables depending on performedActions
        updatePot() #update the pot

#acts on given packet
def parsePacket( data):
    if(len(data) == 0):
        return
    words = data.split() #split packet string at each space to produce array of words
    if(len(words) == 0):
        return
    packetType = words[0] #the first word represents the type of packet
    if(packetType == "GETACTION"):
        handlePacketGetAction(words)
        return
    if(packetType == "NEWGAME"):
        handlePacketNewGame(words)
        return
    if(packetType == "NEWHAND"):
        handlePacketNewHand(words)
        return
    if(packetType == "HANDOVER"):
        handlePacketHandOver(words)
        return

f = open("betsvswinchanceinput.txt")

for x in f:
    parsePacket(x)

f.close()