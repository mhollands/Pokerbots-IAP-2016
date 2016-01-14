import os

numMatches = 8

def getResult():
	f = open("competitor/result.txt")
	result = int(f.readline())
	f.close()
	return result

def chooseParameters(number):
	f = open("Parameters/playParameters"+str(number)+".txt")
	w = open("Player/playParameters.txt", "w")

	for x in f:
		w.write(x)

	f.close()
	w.close()

log = open("battleLog.txt", "w") #open battle log to write

for match in range(0, numMatches):
	chooseParameters(match) #select the correct parameters
	os.system("start cmd /c startEngine.bat") #start engine
	#first round
	os.system("start cmd /c startCompetitor.bat") #start competitor
	os.system("start /wait cmd /c StartPlayer.Bat") #start player
	os.rename("Player/Logs/playerLog.txt", "Player/Logs/playerLog"+str(match)+"a.txt")#rename the log file
	result1 = getResult()
	#duplicate 
	os.system("start cmd /c startCompetitor.bat 3000") #start competitor
	os.system("start /wait cmd /c StartPlayer.bat") #start player
	os.rename("Player/Logs/playerLog.txt", "Player/Logs/playerLog"+str(match)+"b.txt")#rename the log file
	result2 = getResult()
	log.write(str(result1)+"+"+str(result2)+"="+str(result1 + result2)+"\n")

log.close()