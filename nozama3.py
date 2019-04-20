def totalScore(blocks, n):
    """Function to return total score given a list of scores:
        integer = current score
        X = current score is 2x last score
        + = current score is sum of last two scores
        Z = remove most recent score from list
    """
    # use a stack/list to hold the most recent scores
    stack = []
    total = 0
    if len(blocks) != n:
        print ("Error in input! Number of scores does not match input")
        return 0
    for block in blocks:
        if block == 'Z' and len(stack) > 0:
            num = stack.pop()
            total -= num
        else:
            if block == 'X':
                if len(stack) > 0:
                    num = 2 * stack[-1]
                else:
                    num = 0
            elif block == '+':
                num = sum_last_two(stack)
            else:
                try:
                    num = int(block)
                except ValueError:
                    print ("Error in input!")
                    print ("Enter a digit or 'X', 'Z', '+'")
                    num = 0
            total += num
            stack.append(num)

    return total

def sum_last_two(stack):
    if len(stack) == 0:
        return 0
    elif len(stack) == 1:
        return stack[0]
    else:
        return stack[-1] + stack[-2]


'''blocks = [5, -2, 4, 'Z', 'X', 9, '+', '+']
n = 8
print (totalScore(blocks, n))
blocks = [1, 2, '+', 'Z']
n = 4
print (totalScore(blocks, n))
blocks = ['+', 'Z', 1, 2, '+']
n = 5
print (totalScore(blocks, n))
blocks = [1, 2, 3, 1e10, 11, 'Z']
n = 6
print (totalScore(blocks, n))'''


def matchLunches(lunchMenuPairs, teamCuisinePreference):
    """ Function to match lunch menus with team eating preference"""
    # Dict to hold map from cuisine type to lunch item
    lunchMenuTable = {}
    for pair in lunchMenuPairs:
        if len(pair) != 2:
            print ("Invalid input for lunch menu ", pair)
            continue
        elif pair[1] in lunchMenuTable:
            lunchMenuTable[pair[1]].append(pair[0])
        else:
            lunchMenuTable[pair[1]] = [pair[0]]

    teamCuisineList = []
    for cuisine in lunchMenuTable:
        for teamMember in teamCuisinePreference:
            if len(teamMember) != 2:
                print ("Invalid input for team member ", teamMember)
                continue
            elif teamMember[1] == '*' or teamMember[1] == cuisine:
                for menuitem in lunchMenuTable[cuisine]:
                    teamCuisineList.append([teamMember[0], menuitem])
    return teamCuisineList



'''lunchMenuPairs = [['Pizza', 'Italian'],
                    ['Curry', 'Indian'],
                    ['Masala', 'Indian']]

teamCuisinePreference = [['Jose', 'Italian'], ['John', 'Indian'],
                            ['Sarah', 'Thai'], ['Mary', '*']]

lunchMenuPairs = [['pizza', 'italian'], ['lasagna', 'italian']]
teamCuisinePreference = [['ian', '*']]

lunchMenuPairs = [['taco', 'mexican'], ['torta', 'mexican']]
teamCuisinePreference = [['ian', 'mexican']]

lunchMenuPairs = [['lasagna']]
teamCuisinePreference = [['ian']]

print (matchLunches(lunchMenuPairs, teamCuisinePreference))'''

def lazyBartender(setList):
    returnSet = set()
    possibleSet = []
    for nextSet in setList:
        if not any([nextSet & pset for pset in possibleSet]):
            possibleSet.append(nextSet)
        else:
            removeSets = []
            for pset in possibleSet:
                if not nextSet.isdisjoint(pset):
                    returnSet |= nextSet & pset
                    removeSets.append(pset)
            for rset in removeSets:
                possibleSet.remove(rset)
    return returnSet


'''setList = [{3,7,5,2,9}]
setList.append({5})
setList.append({2,3})
setList.append({4})
setList.append({3,4,5,7})
print (lazyBartender(setList))'''

def generateDistMap(ATMLocs, myLoc):
    atmMap = {}
    for atm in ATMLocs:
        atmMap[atm] = getDist(atm, myLoc)
    return atmMap

def closestATM(ATMdist, n):
    closest ATMs
