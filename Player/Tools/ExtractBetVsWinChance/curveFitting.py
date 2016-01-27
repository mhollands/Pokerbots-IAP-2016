import string
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import extractBetVWinchance as extractData
import os

#reads in the data from fileName and returns lists of the winPercentage and respective bet percentage for a specified round of betting
def readBetVWinChanceFile(fileName, roundNumber):
	f = open(fileName, 'r')
	betPercentages = []
	winPercentages = []
	lineNum = 0
	for line in f:
		if (lineNum % 4) == roundNumber:
			lineLength = len(line)
			if line[lineLength - 2] == ',':
				finalIndex = -2
			else:
				finalIndex = -1
			numList = string.split(line[:finalIndex], ',')
			listLength = len(numList)
			if listLength > 1:
				winPercentage = float(numList[0])
				for i in xrange(1, listLength):
					betPercentage = float(numList[i])
					if betPercentage >= 0 and betPercentage <= 1.0:
						betPercentages.append(betPercentage)
						winPercentages.append(winPercentage)
		lineNum += 1
	return betPercentages, winPercentages

def line(x,a,b,c,d):
	return a*x**3 +b*x**2 + c*x + d

#fits a curve in the format specified by the parameters
def fitCurve(betPercentages, winPercentages):
	return curve_fit(line , winPercentages, betPercentages)

def plotPoints(betPercentages, winPercentages, fileLocation): 
	plt.scatter(winPercentages, betPercentages)
	plt.xlabel('Win Percentage')
	plt.ylabel('Bet Percentage')
	plt.savefig(fileLocation)
	plt.clf()
	#plt.show()

def analyseFile(fileLocation, roundNumber):
	print 'hi'
	betPercentages, winPercentages = readBetVWinChanceFile(fileLocation, roundNumber)
	parameters, covar = fitCurve(betPercentages, winPercentages)
	print 'betPercentage = ' + str(parameters[0]) + '* winPercentage + ' + str(parameters[1])
	print parameters
	plotPoints(betPercentages, winPercentages)
	return parameters

def processMiniTournament(directory):
	for fileName in os.listdir(directory):
	
		extractData.createFile(directory + '\\' + fileName)
		for i in range(4):
			betPercentages, winPercentages = readBetVWinChanceFile('output.txt', i)
			plotPoints(betPercentages, winPercentages, 'miniTournament\Betting Graphs\\' + fileName + 'round' + str(i) + '.png')

	return 0

if __name__ == '__main__':
	#analyseFile('extractBetVWinChanceOutput.txt', 0)
	processMiniTournament('miniTournament\logs')