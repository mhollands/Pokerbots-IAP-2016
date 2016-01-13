import PokerPhysics as PP
import Pokerini
import Simulation

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

f = open('process.txt', 'r')
x = f.readlines()

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

team1 = "oldBot"
team2 = "currentBot"

handInfo = {}
for hand in handsDict:
    handInfo[hand] = {}
    handInfo[hand][team1] = {"round0":{"hand":None,"betSize":0,"winProb":None}, "round1":{"hand":None,"betSize":0,"winProb":None}, "round2":{"hand":None,"betSize":0,"winProb":None}, "round3":{"hand":None,"betSize":0,"winProb":None}}
    handInfo[hand][team2] = {"round0":{"hand":None,"betSize":0,"winProb":None}, "round1":{"hand":None,"betSize":0,"winProb":None}, "round2":{"hand":None,"betSize":0,"winProb":None}, "round3":{"hand":None,"betSize":0,"winProb":None}}


for hand in handsDict:
    roundNum = 0
    for line in handsDict[hand]:
        split = line.split()
        #print split
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
            handInfo[hand][team1]["round1"]["winProb"] = Simulation.simulate(handInfo[hand][team1]["round0"]["hand"], handParse, 3, 50)


            team2Hand = PP.findBestHand(handInfo[hand][team2]["round0"]["hand"], handParse)
            handInfo[hand][team2]["round1"]["hand"] = team2Hand[1]
            handInfo[hand][team2]["round1"]["winProb"] = Simulation.simulate(handInfo[hand][team2]["round0"]["hand"], handParse, 3, 50)
            continue
        if split[1] == "TURN":
            roundNum = 2
            handParse = parseHand(split[7], 1)
            handParse2 = parseHand(split[4:-1], 3)
            handParse = handParse + handParse2

            team1Hand = PP.findBestHand(handInfo[hand][team1]["round0"]["hand"], handParse)
            handInfo[hand][team1]["round2"]["hand"] = team1Hand[1]
            handInfo[hand][team1]["round2"]["winProb"] = Simulation.simulate(handInfo[hand][team1]["round0"]["hand"], handParse, 4, 50)


            team2Hand = PP.findBestHand(handInfo[hand][team2]["round0"]["hand"], handParse)
            handInfo[hand][team2]["round2"]["hand"] = team2Hand[1]
            handInfo[hand][team2]["round2"]["winProb"] = Simulation.simulate(handInfo[hand][team2]["round0"]["hand"], handParse, 4, 50)
            continue
        if split[1] == "RIVER":
            roundNum = 3
            handParse = parseHand(split[8], 1)
            handParse2 = parseHand(split[4:-1], 4)
            handParse = handParse + handParse2

            team1Hand = PP.findBestHand(handInfo[hand][team1]["round0"]["hand"], handParse)
            handInfo[hand][team1]["round3"]["hand"] = team1Hand[1]
            handInfo[hand][team1]["round3"]["winProb"] = Simulation.simulate(handInfo[hand][team1]["round0"]["hand"], handParse, 4, 50)

            team2Hand = PP.findBestHand(handInfo[hand][team2]["round0"]["hand"], handParse)
            handInfo[hand][team2]["round3"]["hand"] = team2Hand[1]
            handInfo[hand][team2]["round3"]["winProb"] = Simulation.simulate(handInfo[hand][team2]["round0"]["hand"], handParse, 4, 50)
            continue

print handInfo[10]["currentBot"]

#Currently ignored - x calls, x checks, x shows, x wins, x folds
#Fix betsize and include calls?
#Generate a graph for each team, each round, winProb vs betSize

