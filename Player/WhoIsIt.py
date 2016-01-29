import math

teamID = {'NeverGF': [0.0, 0.2175, 0.0445, 0.020999999999999998], 'ladyshark': [0.0, 0.0, 0.0, 0.0], 'Batman': [0.642, 0.027000000000000003, 0.003, 0.0005], 'LeBluff': [0.0, 0.2705, 0.066, 0.0495], 'HalstonTaylor': [0.0035, 0.008, 0.0, 0.0], 'Battlecode': [0.492, 0.0595, 0.0165, 0.0095], '0xE29883': [0.1915, 0.195, 0.039, 0.027999999999999997], 'MADbot': [0.0, 0.184, 0.1135, 0.053]}
def whoIsIt(round0, round1, round2, round3, handNumber):

	if handNumber == 0:
		return "Your guess is as good as mine."

	round0 = 1.0 * round0 / handNumber
	round1 = 1.0 * round1 / handNumber
	round2 = 1.0 * round2 / handNumber
	round3 = 1.0 * round3 / handNumber

	print "Euler distances: "
	minDist = 4
	name = "I don't know"
	for team in teamID:
		rounds = teamID[team]
		distance = math.pow(round0 - rounds[0], 2) + math.pow(round1 - rounds[1], 2) + math.pow(round2 - rounds[2], 2) + math.pow(round3 - rounds[3], 2)
		print team, str(distance)
		if(distance < minDist):
			minDist = distance
			name = team
	return name