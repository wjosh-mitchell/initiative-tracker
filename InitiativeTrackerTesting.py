import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Global variables
initiativeList = []  # Stores players and monsters with their details
turnClock = 0  # Tracks the number of full turns completed
turnsTaken = 0  # Tracks the number of turns taken in the current round

def addPlayer():
    playerName = simpledialog.askstring("Player Name", "Enter player name:")  # Prompt for player name
    playerScore = simpledialog.askinteger("Player Score", "Enter player score:")  # Prompt for player score
    if playerName and playerScore is not None:
        # Add player to the initiative list with a turn counter initialized to 0 and an empty timer list
        initiativeList.append({"name": playerName, "score": playerScore, "turns": 0, "timers": [], "concentration": tk.BooleanVar()})
        updateListbox()

def addMonsters():
    monsterCount = simpledialog.askinteger("Monster Count", "Enter number of monsters:")  # Prompt for number of monsters
    if monsterCount is not None:
        for _ in range(monsterCount):
            monsterName = simpledialog.askstring("Monster Name", "Enter monster name:")  # Prompt for monster name
            if monsterName:
                randScore = random.randint(0, 100) % 29  # Generate a random score between 0 and 28
                # Add monster to the initiative list with a turn counter initialized to 0 and an empty timer list
                initiativeList.append({"name": monsterName, "score": randScore, "turns": 0, "timers": [], "concentration": tk.BooleanVar()})
        updateListbox()

def sortInitiative():
    # Sort the initiative list in descending order based on the score
    initiativeList.sort(key=lambda x: x["score"], reverse=True)
    updateListbox()

def nextTurn():
    global turnClock, turnsTaken
    if initiativeList:
        initiativeList[0]["turns"] += 1  # Increment the turn counter for the current entry
        turnsTaken += 1  # Increment the global turns taken counter
        # Decrement all timers for the current entry
        for i, timer in enumerate(initiativeList[0]["timers"]):
            initiativeList[0]["timers"][i] -= 1
        # Remove timers that have reached 0 and alert the user
        finishedTimers = [timer for timer in initiativeList[0]["timers"] if timer <= 0]
        initiativeList[0]["timers"] = [timer for timer in initiativeList[0]["timers"] if timer > 0]
        for _ in finishedTimers:
            messagebox.showinfo("Timer Finished", f"{initiativeList[0]['name']}'s Timer has Finished!")
        initiativeList.append(initiativeList.pop(0))  # Move the current entry to the end of the list
        updateListbox()
        if turnsTaken >= len(initiativeList):  # Check if everyone has had a turn
            turnClock += 1  # Increment the turn clock
            turnsTaken = 0  # Reset the turns taken counter
            messagebox.showinfo("Turn Complete", f"{turnClock} full turn(s) has passed!")
    else:
        messagebox.showwarning("Warning", "Initiative list is empty!")  # Warn if the list is empty

def updateListbox():
    listbox.delete(0, tk.END)  # Clear the listbox
    for entry in initiativeList:
        concentrationStatus = "C" if entry["concentration"].get() else ""  # Show "C" if concentration is active
        timerDisplay = f" - Timers: {', '.join(map(str, entry['timers']))}" if entry["timers"] else ""  # Show timers if they exist
        listbox.insert(tk.END, f"{entry['turns']} - {entry['name']} ({entry['score']}) {concentrationStatus} {timerDisplay}")

def toggleConcentration():
    selectedIndex = listbox.curselection()
    if selectedIndex:
        index = selectedIndex[0]
        initiativeList[index]["concentration"].set(not initiativeList[index]["concentration"].get())  # Toggle concentration
        updateListbox()
    else:
        messagebox.showwarning("Warning", "No Entry Selected!")  # Warn if no entry is selected

def addTimer():
    selectedIndex = listbox.curselection()
    if selectedIndex:
        index = selectedIndex[0]
        newTimer = simpledialog.askinteger("Add Timer", f"Enter timer for {initiativeList[index]['name']} (in turns):")  # Prompt for timer
        if newTimer is not None:
            initiativeList[index]["timers"].append(newTimer)  # Add the new timer to the list
            updateListbox()
    else:
        messagebox.showwarning("Warning", "No entry selected!")  # Warn if no entry is selected

root = tk.Tk()
root.title("Initiative Tracker")

topFrame = tk.Frame(root)  # Create a frame for the top buttons
topFrame.pack(pady=5, anchor="e")

btnNextTurn = tk.Button(topFrame, text="Next Turn", command=nextTurn)  # Button to progress to the next turn
btnNextTurn.pack(side=tk.RIGHT, padx=5)

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

btnSort = tk.Button(root, text="Sort Initiative", command=sortInitiative)  # Button to sort the initiative list
btnSort.pack(pady=5)

root.mainloop()  # Run the GUI event loop