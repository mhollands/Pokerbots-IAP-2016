import PokerPhysics as PP

def pokeriniInitialise():
    d = dict()
    with open('omahavs1randomhand.txt') as f:
        for x in f:
            d[x[0:8]] = float(x[8:-1])
    return d

def pokeriniLookup(cards, pokeriniDictionary):
    suitOrder = ['s', 'h', 'd', 'c']
    translateDict = dict()
    for x1 in suitOrder: #go through every value for suit1
        for x2 in suitOrder: #go through every value for suit2
            if(x2 == x1):
                continue
            for x3 in suitOrder: #go through every value for suit3
                if(x3 == x2 or x3 == x1):
                    continue
                for x4 in suitOrder: #go through every value of suit4
                    if(x4 == x3 or x4 == x2 or x4 == x1):
                        continue
                    #create dictionary to say which suits translate to which
                    translateDict['s'] = x1
                    translateDict['h'] = x2
                    translateDict['d'] = x3
                    translateDict['c'] = x4

                    #translate cards to new hand
                    pokeriniCards = list()
                    for card in cards:
                        pokeriniCards.append((card[0], translateDict[card[1]]))
                    #sort cards
                    pokeriniCards = sorted(pokeriniCards, key=lambda x: (x[0], x[1]), reverse = True)
                    #convert to string
                    searchString = ''
                    for card in pokeriniCards:
                        number = str(card[0])
                        if(card[0] == 10):
                            number = 'T'
                        if(card[0] == 11):
                            number = 'J'
                        if(card[0] == 12):
                            number = 'Q'
                        if(card[0] == 13):
                            number = 'K'
                        if(card[0] == 14):
                            number = 'A'
                        searchString = searchString + number + card[1]
                    result = pokeriniDictionary.get(searchString)
                    if(result != None):
                        return result
    
'''
def pokeriniLookup(cards):
    numSuits = len(set((cards[0][1],cards[1][1],cards[2][1],cards[3][1])))

    suit1 = list()
    suit2 = list()
    suit3 = list()
    suit4 = list()

    for card in cards:
        if(card[1] == 's'):
            suit1.append((card[0], 'x'))
            next
        if(card[1] == 'h'):
            suit2.append((card[0], 'x'))
            next
        if(card[1] == 'd'):
            suit3.append((card[0], 'x'))
            next
        if(card[1] == 'c'):
            suit4.append((card[0], 'x'))
            next

    suits = sorted([sorted(suit1, reverse = True), sorted(suit2, reverse = True), sorted(suit3, reverse = True), sorted(suit4, reverse = True)], key=lambda x: (len(x), x[0]), reverse = True)
    print suits
    suitOrder = ['s', 'h', 'd', 'c']
    pokeriniCards = list()
    for suit in range(0, 4):
        for card in suits[suit]:
            pokeriniCards.append((card[0], suitOrder[suit]))

    pokeriniCards = sorted(pokeriniCards, reverse = True)
    searchString = ''
    for card in pokeriniCards:
        number = str(card[0])
        if(card[0] == 10):
            number = 'T'
        if(card[0] == 11):
            number = 'J'
        if(card[0] == 12):
            number = 'Q'
        if(card[0] == 13):
            number = 'K'
        if(card[0] == 14):
            number = 'A'
        searchString = searchString + number + card[1]
                     
    return d[searchString]
'''
