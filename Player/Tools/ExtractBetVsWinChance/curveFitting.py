import string
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

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
					print 'String: ', numList[i]
					betPercentage = float(numList[i])
					print 'betPercentage: ', betPercentage
					if betPercentage >= 0 and betPercentage <= 1.0:
						betPercentages.append(betPercentage)
						winPercentages.append(winPercentage)
		lineNum += 1
	return betPercentages, winPercentages

def line(x,a,b):
	return a*x +b

def fitCurve(betPercentages, winPercentages):
	return curve_fit(line , winPercentages, betPercentages)

def plotPoints(betPercentages, winPercentages):
	plt.scatter(winPercentages, betPercentages)
	plt.xlabel('Win Percentage')
	plt.ylabel('Bet Percentage')
	plt.show()

def analyseFile(fileLocation, roundNumber):
	betPercentages, winPercentages = readBetVWinChanceFile(fileLocation, roundNumber)
	parameters, covar = fitCurve(betPercentages, winPercentages)
	print 'betPercentage = ' + str(parameters[0]) + '* winPercentage + ' + str(parameters[1])
	plotPoints(betPercentages, winPercentages)
	return parameters

if __name__ == '__main__':
	analyseFile('extractBetVWinChanceOutput.txt', 1)
