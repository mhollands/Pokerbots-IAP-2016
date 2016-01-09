import Simulation
import PokerPhysics as PP
import time

'''
f = open('data.csv', 'w')

for x in range(0, 2000):
	myHand = PP.generateTestHand(4)
	boardCards = PP.generateTestHand(3)
	bestHandRank = PP.findBestHand(myHand, boardCards)
	simulationRank = Simulation.simulate(myHand, boardCards, 3, 100)
	print "BestHandRank: ",bestHandRank[0][0]," SimulationRank: ",simulationRank
	f.write(str(bestHandRank[0][0]*10 + (bestHandRank[0][1]/1.4))+","+str(simulationRank)+"\n")

f.close()

'''
myHand = list()
boardCards = list()
for x in range(0, 1000):
	myHand.append(PP.generateTestHand(4))
	boardCards.append(PP.generateTestHand(3))

startTime = time.time()
print startTime

for x in range(0,1000):
	bestHandRank = PP.findBestHand(myHand[x], boardCards[x])
	#simulationRank = Simulation.simulate(myHand[x], boardCards[x], 3, 100)
endTime = time.time()

print endTime
print endTime - startTime
