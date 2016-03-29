import string
import matplotlib.pyplot as plt
import os

def calcDifference(fileName, newThreshold):
	placeholder = 0

def calcDifferencePreFlop(fileName, newThreshold):
	logFile = open(fileName, 'r')
	logString = logFile.read()
	#print logString
	responseIndex = 0
	overallGain = 0
	winnings = 0
	while True:
		prevWinnings = winnings
		pokeriniIndex = string.find(logString, 'Pokerini Rank: ', responseIndex)
		if pokeriniIndex == -1:
			break
		pokeriniRank = logString[pokeriniIndex + 15: pokeriniIndex + 20]
		pokeriniRank = float(string.split(pokeriniRank)[0])

		myBetIndex = string.find(logString, 'My Bet: ', pokeriniIndex)
		myBet = logString[myBetIndex + 9: myBetIndex + 12]
		myBet = int(string.split(myBet)[0])

		responseIndex = string.find(logString, 'Response: ' , myBetIndex)
		response = logString[responseIndex + 10: responseIndex + 14]

		winningsIndex = string.find(logString, 'HANDOVER', responseIndex)
		winnings = logString[winningsIndex+9:winningsIndex + 13]
		winnings = int(string.split(winnings)[0])

		#print 'pokeriniRank: ', pokeriniRank
		#print 'My Bet: ', myBet
		#print 'response: ', response
		#print 'winnings: ', winningsresponse

		if (response != 'FOLD') and (response != 'CHEC') and pokeriniRank < newThreshold:
			winLoss = winnings - prevWinnings
			#print 'winLoss: ', winLoss
			overallGain -= winLoss
			if winLoss < 0:
				overallGain -= myBet
			#print 'overallGain: ', overallGain

	logFile.close()

	return overallGain

def analyseDayResults(day, newThreshold):
	gain = 0
	directory = 'casino_logs\day ' + str(day) + '\Player Dumps'
	for fileName in os.listdir(directory):
		gain += calcDifferencePreFlop(directory + '\\' + fileName, newThreshold)

	return gain

def graphThresholds(day):
	thresholdValues = []
	for i in range(65):
		thresholdValues.append(0.1 + i * 0.01)

	gains = []
	for value in thresholdValues:
		gains.append(analyseDayResults(day, value))

	plt.plot(thresholdValues, gains)
	plt.xlabel('Fold Threshold')
	plt.ylabel('Gain')
	plt.show()

if __name__ == '__main__':
	graphThresholds(3)
	print calcDifferencePreFlop('casino_logs\Day 7\Player Dumps\Batman_vs_StraightOuttaCam_StraightOuttaCam', 0.60)
