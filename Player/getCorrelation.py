import PokerPhysics as PP
import Pokerini
import Simulation
import os

def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    else:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

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

def parseHand(words, length):
    if length == 1:
        return [parseCard(words[1:-1])]
    hand = []
    for x in range(0,length):
        if x == 0:
            hand.append(parseCard(words[x][1:]))
            continue
        if x == length-1:
            hand.append(parseCard(words[x][:-1]))
            continue
        hand.append(parseCard(words[x]))
    return hand

pokeriniDict = Pokerini.pokeriniInitialise()

#Pokerini initialised

#Open and process the file
#f = open('process.txt', 'r')
f = open("hands/" + fn, 'r')
x = f.readlines()

#Split the lines into each hand
start = 0
end = 0
hand = 1
handsDict = {}
lineNum = len(x)
for i in range(0,lineNum):
    line = x[i]
    if line == '\n':
        end = i
        handsDict[hand] = x[start:end]
        start = i+1
        hand += 1

#Rip team names from line 1
team1 = x[0].split()[4]
team2 = x[0].split()[6]

team1Action = {0:{"fold": [], "check": [], "raise": [], "call": []}, 1:{"fold": [], "check": [], "raise": [], "call": []}, 2:{"fold": [], "check": [], "raise": [], "call": []}, 3{"fold": [], "check": [], "raise": [], "call": []}}
team2Action = {0:{"fold": [], "check": [], "raise": [], "call": []}, 1:{"fold": [], "check": [], "raise": [], "call": []}, 2:{"fold": [], "check": [], "raise": [], "call": []}, 3{"fold": [], "check": [], "raise": [], "call": []}}


#Parse the data from hands into a useful format
for hand in handsDict:
    roundNum = 0
    team1act = [False, False, False, False]
    team2act = [False, False, False, False]
    team1hole = []
    team2hole = []
    tableCards = []
    potSize = 0
    for line in handsDict[hand]:
        split = line.split()

        if split[0] == "Dealt":
            handParse = parseHand(split[3:], 4)
            team = split[2]
            if team == team1: team1hole = handParse
            if team == team2: team2hole = handParse
        if split[1] == "FLOP":
            roundNum = 1
            tableCards = parseHand(split[4:], 3)
            continue
        if split[1] == "TURN":
            roundNum = 2
            tableCards = parseHand(split[7], 1) + parseHand(split[4:-1], 3)
            continue
        if split[1] == "RIVER":
            roundNum = 3
            tableCards = parseHand(split[8], 1) + parseHand(split[4:-1], 4)
            continue
        if split[1] == "raises":
            team = split[0]
            handInfo[hand][team]["round" + str(roundNum)]["betSize"] = int(split[3])
            continue
        if split[1] == "bets":
            team = split[0]
            handInfo[hand][team]["round" + str(roundNum)]["betSize"] = int(split[2])
            continue