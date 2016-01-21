import math

teamID = {'NeverGF': [0.0, 0.24, 0.11299999999999999, 0.068], 'ladyshark': [0.6105, 0.068, 0.03, 0.034], 'Batman': [0.6555, 0.05, 0.036000000000000004, 0.03], 'LeBluff': [0.0, 0.1915, 0.11399999999999999, 0.0875], 'Battlecode': [0.5640000000000001, 0.091, 0.0455, 0.034999999999999996], '0xE29883': [0.1945, 0.186, 0.08, 0.062], 'MADbot': [0.0005, 0.1585, 0.121, 0.088]}

def whoIsIt(round0, round1, round2, round3, handNumber):

	if handNumber == 0:
		return "Your guess is as good as mine."

	round0 = 1.0 * round0 / handNumber
	round1 = 1.0 * round1 / handNumber
	round2 = 1.0 * round2 / handNumber
	round3 = 1.0 * round3 / handNumber

	print "Euler distances: "
	minDist = 4
	name = "I don't have a fucking clue"
	for team in teamID:
		rounds = teamID[team]
		distance = math.pow(round0 - rounds[0], 2) + math.pow(round1 - rounds[1], 2) + math.pow(round2 - rounds[2], 2) + math.pow(round3 - rounds[3], 2)
		print team, str(distance)
		if(distance < minDist):
			minDist = distance
			name = team
	return name