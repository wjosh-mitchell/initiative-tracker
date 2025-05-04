# Initiative Tracker
# Josh Mitchell
# Keep track of intiative in games such as D&D, keep track of amount of turns, and timers within the game.
# 5/4/2025

import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Global variables
initiativeList = []
turnClock = 0
turnsTaken = 0

# Add players to initiative list
def addPlayer():
    # Prompt user for player name and score
    
    playerName = simpledialog.askstring("Player Name", "Enter player name:")
    playerScore = simpledialog.askinteger("Player Score", "Enter player score:")
    
    # Check if user provided a valid name and score
    if playerName and playerScore is not None:
        initiativeList.append({"name": playerName, "score": playerScore, "turns": 0})
        updateListbox()

# Add monsters to initiative list
def addMonsters():
    # Prompt user for number of monsters
    monsterCount = simpledialog.askinteger("Monster Count", "Enter number of monsters:")
    
    # Check if user provided a valid input
    if monsterCount is not None:
        # Generate random scores and insert the monsters into the initiative list
        for _ in range(monsterCount):
            monsterName = simpledialog.askstring("Monster Name", "Enter monster name:")
            if monsterName:
                # Generate a random score force it to be between 0 and 28
                randScore = random.randint(0, 100) % 29
                # Insert the monseter into the initiative list
                initiativeList.insert(0, {"name": monsterName, "score": randScore, "turns": 0})
        updateListbox()

# Sort initiative list by score
def sortInitiative():
    initiativeList.sort(key=lambda x: x["score"], reverse=True)
    updateListbox()

# Progress to the next turn
def nextTurn():
    global turnClock, turnsTaken
    
    if initiativeList:
        # Update the turn counter for the current entry
        initiativeList[0]["turns"] += 1
        turnsTaken += 1

        # Cycle the list
        initiativeList.append(initiativeList.pop(0))
        updateListbox()

        # Check if everyone has had a turn
        if turnsTaken >= len(initiativeList):
            turnClock += 1
            turnsTaken = 0
            messagebox.showinfo("Turn Complete", f"{turnClock} full turn(s) has passed!")
    else:
        messagebox.showwarning("Warning", "Initiative list is empty!")

# Update the listbox with the current initiative list
def updateListbox():
    listbox.delete(0, tk.END)
    
    for entry in initiativeList:
        listbox.insert(tk.END, f"{entry['name']} ({entry['score']}) - {entry['turns']}")

# Create the main GUI window
root = tk.Tk()
root.title("Initiative Tracker")

# Create and place widgets
frame = tk.Frame(root)
frame.pack(pady=10)

listbox = tk.Listbox(frame, width=50, height=15)
listbox.pack(side=tk.LEFT, padx=10)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# Create a frame for the buttons
buttonFrame = tk.Frame(root)
buttonFrame.pack(pady=5)

# Button to add players to the list
btnAddPlayer = tk.Button(buttonFrame, text="Add Player", command=addPlayer)
btnAddPlayer.pack(side=tk.LEFT, padx=5)

# Button to add monsters to the list
btnAddMonsters = tk.Button(buttonFrame, text="Add Monsters", command=addMonsters)
btnAddMonsters.pack(side=tk.LEFT, padx=5)

# Button to sort the initiative list
btnSort = tk.Button(root, text="Sort Initiative", command=sortInitiative)
btnSort.pack(pady=5)

# Button to progress to the next turn
btnNextTurn = tk.Button(root, text="Next Turn", command=nextTurn)
btnNextTurn.pack(pady=5)

# Run the GUI event loop
root.mainloop()