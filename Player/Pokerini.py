import PokerPhysics as PP

def pokeriniInitialise():
    d = dict()
    with open('omahavs1randomhand.txt') as f:
        for x in f:
            d[x[0:8]] = float(x[8:-1])
    return d

def pokeriniLookup(cards):
    numSuits = len(set((cards[0][1],cards[1][1],cards[2][1],cards[3][1])))

    suit1 = list()
    suit2 = list()
    suit3 = list()
    suit4 = list()

    for card in cards:
        if(card[1] == 's'):
            suit1.append(card)
            next
        if(card[1] == 'h'):
            suit2.append(card)
            next
        if(card[1] == 'd'):
            suit3.append(card)
            next
        if(card[1] == 'c'):
            suit4.append(card)
            next

    suits = sorted([sorted(suit1, reverse = True), sorted(suit2, reverse = True), sorted(suit3, reverse = True), sorted(suit4, reverse = True)], reverse = True)

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

d = pokeriniInitialise()
print pokeriniLookup([(4, 's'), (5, 'c'), (3, 'd'), (8, 'c')])
