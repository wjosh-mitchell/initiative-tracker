# Josh Mitchell
# Initiative Tracker
# This program is a simple initiative tracker for tabletop role-playing games. It allows users to add players and monsters, manage their initiative scores, and track turns and timers.
# 5.7.2025

import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Global variables
initiativeList = []  # Stores players and monsters with their details
turnClock = 0  # Tracks the number of full turns completed
turnsTaken = 0  # Tracks the number of turns taken in the current round

def addPlayer():
    # Add a player to the initiative list
    
    # Prompt for player name and score
    playerName = simpledialog.askstring("Player Name", "Enter player name:")
    playerScore = simpledialog.askinteger("Player Score", "Enter player score:")  
    if playerName and playerScore is not None:
        # Add player to the initiative list with a turn counter initialized to 0 and an empty timer 
        initiativeList.append({"name": playerName, "score": playerScore, "turns": 0, "timers": [], "concentration": tk.BooleanVar()})
        updateListbox()

def addMonsters():
    # Add monsters to the initiative list with random scores
    
    # Prompt for the number of monsters to add
    monsterCount = simpledialog.askinteger("Monster Count", "Enter number of monsters:")
    if monsterCount is not None:
        for i in range(monsterCount):
            monsterName = simpledialog.askstring("Monster Name", "Enter monster name:")
            if monsterName:
                # Generate a random score between 0 and 26
                randScore = random.randint(0, 100) % 27 
                # Add monster to the initiative list with a turn counter initialized to 0 and an empty timer list
                initiativeList.append({"name": monsterName, "score": randScore, "turns": 0, "timers": [], "concentration": tk.BooleanVar()})
        updateListbox()

def sortInitiative():
    # Sort the initiative list in descending order based on the score
    
    initiativeList.sort(key=lambda x: x["score"], reverse=True)
    updateListbox()

def nextTurn():
    # Progress to the next turn in the initiative list
    
    global turnClock, turnsTaken
    if initiativeList:
        # Increment the turn counter for the current entry
        initiativeList[0]["turns"] += 1  
        # Increment the global turns taken counter
        turnsTaken += 1
        # Decrement all timers for the current entry
        for i, timer in enumerate(initiativeList[0]["timers"]):
            initiativeList[0]["timers"][i] -= 1
        # Remove timers that have reached 0 and alert the user
        finishedTimers = [timer for timer in initiativeList[0]["timers"] if timer <= 0]
        initiativeList[0]["timers"] = [timer for timer in initiativeList[0]["timers"] if timer > 0]
        for _ in finishedTimers:
            messagebox.showinfo("Timer Finished", f"{initiativeList[0]['name']}'s Timer has Finished!")
        # Move the current entry to the end of the list
        initiativeList.append(initiativeList.pop(0))
        updateListbox()
        # Check if every object has had a turn
        if turnsTaken >= len(initiativeList):
            # Increments the turn clock
            turnClock += 1 
            # Reset the turns taken counter
            turnsTaken = 0
            messagebox.showinfo("Turn Complete", f"{turnClock} full turn(s) has passed!")
    else:
        #Warn if the initiative list is empty
        
        messagebox.showwarning("Warning", "Initiative list is empty!")

def updateListbox():
    # Clear the listbox and update it with the current initiative list
    
    listbox.delete(0, tk.END)  
    for entry in initiativeList:
        # Show "C" if concentration is active and empty if not
        concentrationStatus = "C" if entry["concentration"].get() else "" 
         # Show timers if they exist
        timerDisplay = f" - Timers: {', '.join(map(str, entry['timers']))}" if entry["timers"] else "" 
        listbox.insert(tk.END, f"{entry['turns']} - {entry['name']} ({entry['score']}) {concentrationStatus} {timerDisplay}")

def toggleConcentration():
    # Toggle the concentration status of the selected object in the initiative list
    
    selectedIndex = listbox.curselection()
    if selectedIndex:
        index = selectedIndex[0]
        # Toggle the concentration status of the selected entry
        initiativeList[index]["concentration"].set(not initiativeList[index]["concentration"].get())
        updateListbox()
    else:
        # Warn if no entry is selected
        
        messagebox.showwarning("Warning", "No Entry Selected!")

def addTimer():
    # Add a timer to the selected object in the initiative list
    
    selectedIndex = listbox.curselection()
    if selectedIndex:
        index = selectedIndex[0]
        # Prompt for timer
        newTimer = simpledialog.askinteger("Add Timer", f"Enter timer for {initiativeList[index]['name']} (in turns):")
        if newTimer is not None:
            # Add the new timer to the list
            initiativeList[index]["timers"].append(newTimer)
            updateListbox()
    else:
        # Warn if no entry is selected
        
        messagebox.showwarning("Warning", "No entry selected!")

def modifyScore():
    # Allows the user to modify the initiative score of a selected object.
    
    selectedIndex = listbox.curselection()
    if selectedIndex:
        index = selectedIndex[0]
        currentScore = initiativeList[index]["score"]
        modifyAmount = simpledialog.askinteger(
            "Modify Score",
            f"Current score for {initiativeList[index]['name']} is {currentScore}. Enter the amount to add or subtract:",
        )
        if modifyAmount is not None:
            # Modify the score by specified amount
            
            initiativeList[index]["score"] += modifyAmount
            updateListbox()
    else:
        # Warn if no entry is selected
        
        messagebox.showwarning("Warning", "No entry selected!")  

def resetList():
#   Clears the initiative list and updates the listbox.

    global initiativeList, turnClock, turnsTaken
    initiativeList = []  # Clear the initiative list
    turnClock = 0  # Reset the turn clock
    turnsTaken = 0  # Reset the turns taken counter
    updateListbox()  # Update the listbox
    messagebox.showinfo("Reset", "The initiative list has been reset!")  # Notify the user

def removeSelected():
    # Removes the selected object from the initiative list
    
    selectedIndex = listbox.curselection()
    if selectedIndex:
        index = selectedIndex[0]
        # Get the name of the removed object
        removedName = initiativeList[index]["name"] 
        # Remove the selected object from the list
        del initiativeList[index] 
        # Update the list
        updateListbox()
         # Notify the user of the removal
        messagebox.showinfo("Removed", f"{removedName} has been removed from the list.")
    else:
         # Warn if no entry is selected
        
        messagebox.showwarning("Warning", "No entry selected!")

# ---  GUI Setup --- #

root = tk.Tk()
root.title("Initiative Tracker")

topFrame = tk.Frame(root)  # Create a frame for the top buttons
topFrame.pack(pady=5, fill="x")  # Fill the frame horizontally

btnReset = tk.Button(topFrame, text="Reset", command=resetList)  # Button to reset the initiative list
btnReset.pack(side=tk.LEFT, padx=5)  # Place the Reset button on the left

btnNextTurn = tk.Button(topFrame, text="Next Turn", command=nextTurn)  # Button to progress to the next turn
btnNextTurn.pack(side=tk.RIGHT, padx=5)  # Place the Next Turn button on the right

frame = tk.Frame(root)
frame.pack(pady=10)

listbox = tk.Listbox(frame, width=70, height=15)  # Create a listbox to display the initiative list
listbox.pack(side=tk.LEFT, padx=10)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)  # Add a scrollbar to the listbox
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

buttonFrame = tk.Frame(root)  # Create a frame for the buttons
buttonFrame.pack(pady=5)

btnAddPlayer = tk.Button(buttonFrame, text="Add Player", command=addPlayer)  # Button to add players
btnAddPlayer.pack(side=tk.LEFT, padx=5)

btnAddMonsters = tk.Button(buttonFrame, text="Add Monsters", command=addMonsters)  # Button to add monsters
btnAddMonsters.pack(side=tk.LEFT, padx=5)

btnConcentrationTimerFrame = tk.Frame(root)  # Create a frame for concentration and timer buttons
btnConcentrationTimerFrame.pack(pady=5)

btnToggleConcentration = tk.Button(btnConcentrationTimerFrame, text="Toggle Concentration", command=toggleConcentration)  # Button to toggle concentration
btnToggleConcentration.pack(side=tk.LEFT, padx=5)

btnAddTimer = tk.Button(btnConcentrationTimerFrame, text="Add Timer", command=addTimer)  # Button to add a timer
btnAddTimer.pack(side=tk.LEFT, padx=5)

btnModifyRemoveFrame = tk.Frame(root)  # Create a frame for Modify Score and Remove buttons
btnModifyRemoveFrame.pack(pady=5)

btnModifyScore = tk.Button(btnModifyRemoveFrame, text="Modify Score", command=modifyScore)  # Button to modify the score
btnModifyScore.pack(side=tk.LEFT, padx=5)

btnRemove = tk.Button(btnModifyRemoveFrame, text="Remove", command=removeSelected)  # Button to remove the selected object
btnRemove.pack(side=tk.LEFT, padx=5)

btnSortModifyFrame = tk.Frame(root)  # Create a frame for Sort Initiative button
btnSortModifyFrame.pack(pady=5)

btnSort = tk.Button(btnSortModifyFrame, text="Sort Initiative", command=sortInitiative)  # Button to sort the initiative list
btnSort.pack(side=tk.LEFT, padx=5)

root.mainloop()  # Run the GUI event loop