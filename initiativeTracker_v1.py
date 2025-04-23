# Initiative Tracker
# Josh Mitchell
# Keep track of intiative in games such as D&D, keep track of amount of turns, and timers within the game.
# 4/22/2025

import random

initiativeList = []

turnClock = 0

# Add players to initiative list and sort by reverse order
def playerAdd(name, score):
    initiativeList.append(score + " " + name)
    
# Add monsters to initiative list randomly    
def monsterAdd(monsterTotal):
    # Calculate total amount of players and monsters
    total = monsterAmount + len(initiativeList)
    
    for i in range(monsterTotal):
        # Prompt for monster name
        monsterName = input("Enter monster name: ")
        # Generate random number between 0 and total number of players and monsters
        randNum = random.randint(0, (total + 1))
        # Insert monsters into the initiative list at random position
        initiativeList.insert(randNum, monsterName)
        
        #print("Monster added at position: " + str(randNum))

# Prompt for player amount
playerAmount = int(input("Enter amount of players: "))
    
# Loop through player amount and prompt for player name and score
    
for i in range(playerAmount):
    playerName = input("Enter player name: ")
    playerScore = input("Enter player score: ")
    # Add player to initiative list
    playerAdd(playerName, playerScore)
    
    
    #print(initiativeList)

# Prompt for monster amount
monsterAmount = int(input("Enter amount of monsters: "))

# Add monsters to initiative list
monsterAdd(monsterAmount)

# Print and sort initiative list
print(initiativeList)
initiativeList.sort(reverse=True)

turnProgress = input("Type y to progress to next turn: ")

if turnProgress == 'y':
    # Add on to turn clock
    turnClock += 1
    
    # Shift initiative list to the left
    initiativeList = initiativeList[1:] + initiativeList[:1]
    print(initiativeList)