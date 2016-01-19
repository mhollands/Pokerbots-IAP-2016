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
    for line in handsDict[hand]:
        split = line.split()

        if split[0] == "Dealt":
            handParse = parseHand(split[3:], 4)
            team = split[2]
            if team == team1: team1hole = handParse
            if team == team2: team2hole = handParse

        if split[1] == "folds":
            team = split[0]
            if team == team1:
                if team1act[roundNum] == False:
                    team1Action[roundNum]["fold"].append()
                    team1act[roundNum] == True
                    team1folds0.append(Pokerini.pokeriniLookup(team1hand, pokeriniDict))
            if team == team2: 
                team2Exits["round" + str(roundNum) + "fold"] += 1
                if roundNum == 0:
                    team2folds0.append(Pokerini.pokeriniLookup(team2hand, pokeriniDict))
            continue
        if split[1] == "wins":
            team = split[0]
            if team == team1: 
                team1Wins["wins"] += 1
                team1Wins["totalScore"] += int(split[4][1:-1])
                team1Wins["listWins"].append(int(split[4][1:-1]))
            if team == team2: 
                team2Wins["wins"] += 1
                team2Wins["totalScore"] += int(split[4][1:-1])
                team2Wins["listWins"].append(int(split[4][1:-1]))
            continue
        if split[1] == "shows":
            team = split[0]
            if team == team1: team1Exits["showdown"] += 1
            if team == team2: team2Exits["showdown"] += 1
            continue
        if split[1] == "FLOP":
            roundNum = 1
            continue
        if split[1] == "TURN":
            roundNum = 2
            continue
        if split[1] == "RIVER":
            roundNum = 3
            continue

        #Previous code that calculated win probabilities - will use again later
        """        
        if split[0] == "Dealt":
            handParse = parseHand(split[3:], 4)
            team = split[2]
            handInfo[hand][team]["round0"]["hand"] = handParse
            handInfo[hand][team]["round0"]["winProb"] = Pokerini.pokeriniLookup(handParse, pokeriniDict)
            continue
        if split[1] == "raises":
            team = split[0]
            handInfo[hand][team]["round" + str(roundNum)]["betSize"] = int(split[3])
            continue
        if split[1] == "bets":
            team = split[0]
            handInfo[hand][team]["round" + str(roundNum)]["betSize"] = int(split[2])
            continue
        if split[1] == "FLOP":
            roundNum = 1
            handParse = parseHand(split[4:], 3)
            team1Hand = PP.findBestHand(handInfo[hand][team1]["round0"]["hand"], handParse)
            handInfo[hand][team1]["round1"]["hand"] = team1Hand[1]
            handInfo[hand][team1]["round1"]["winProb"] = Simulation.simulateOld(handInfo[hand][team1]["round0"]["hand"], handParse, 3, 100)


            team2Hand = PP.findBestHand(handInfo[hand][team2]["round0"]["hand"], handParse)
            handInfo[hand][team2]["round1"]["hand"] = team2Hand[1]
            handInfo[hand][team2]["round1"]["winProb"] = Simulation.simulateOld(handInfo[hand][team2]["round0"]["hand"], handParse, 3, 100)
            continue
        if split[1] == "TURN":
            roundNum = 2
            handParse = parseHand(split[7], 1)
            handParse2 = parseHand(split[4:-1], 3)
            handParse = handParse + handParse2

            team1Hand = PP.findBestHand(handInfo[hand][team1]["round0"]["hand"], handParse)
            handInfo[hand][team1]["round2"]["hand"] = team1Hand[1]
            handInfo[hand][team1]["round2"]["winProb"] = Simulation.simulateOld(handInfo[hand][team1]["round0"]["hand"], handParse, 4, 100)


            team2Hand = PP.findBestHand(handInfo[hand][team2]["round0"]["hand"], handParse)
            handInfo[hand][team2]["round2"]["hand"] = team2Hand[1]
            handInfo[hand][team2]["round2"]["winProb"] = Simulation.simulateOld(handInfo[hand][team2]["round0"]["hand"], handParse, 4, 100)
            continue
        if split[1] == "RIVER":
            roundNum = 3
            handParse = parseHand(split[8], 1)
            handParse2 = parseHand(split[4:-1], 4)
            handParse = handParse + handParse2

            team1Hand = PP.findBestHand(handInfo[hand][team1]["round0"]["hand"], handParse)
            handInfo[hand][team1]["round3"]["hand"] = team1Hand[1]
            handInfo[hand][team1]["round3"]["winProb"] = Simulation.simulateOld(handInfo[hand][team1]["round0"]["hand"], handParse, 4, 100)

            team2Hand = PP.findBestHand(handInfo[hand][team2]["round0"]["hand"], handParse)
            handInfo[hand][team2]["round3"]["hand"] = team2Hand[1]
            handInfo[hand][team2]["round3"]["winProb"] = Simulation.simulateOld(handInfo[hand][team2]["round0"]["hand"], handParse, 4, 100)
            continue
        """