# Dalton Muck
# CS 4150 Activity #2

# Open the file for reading
filename = "/Users/tm033520/Documents/4150/Data-Science/data.txt"
data = []
# will hold name of window and total number of NP's in window 
window_data = [{"name": [], "total": 0}]

#will hold name of np and total number of windows in np
np_data = [{"name": [], "total": 0}]



# load data into strcutures and data array
with open(filename, "r") as file:

    # Read the first row for NP names
    first_row = file.readline().strip().split()
    
    # Store names starting from the 4th element in np
    np_data = [{"name": name, "total": 0} for name in first_row[3:]]


    for line in file:
        # Split the line into a list of values
        row = line.strip().split()

        # Add a window structure for the current row
        window_data.append({"name": row[0], "total": 0})
        # Skip the first three elements and convert the rest to integers
        row = [int(value) for value in row[3:]]
        # Append the processed row to the 2D list
        data.append(row)

#1. Estimate radial posisition


#number of windows (rows) in a NP(column)
for row in data:
    for index in range(len(data[0])):
        if row[index] == 1:
            np_data[index]["total"] += 1
# built in sort functoin to sort the list by total number of windows
np_data.sort(key=lambda np: np["total"])


size = len(np_data)
# cateogrize the NP's into 5 groups
for index in range(len(np_data)):
    num = 0
    if(index < size / 5):
        num = 1
    elif(index < size / 4):
        num = 2
    elif(index < size / 3):
        num = 3
    elif(index < size / 2):
        num = 4
    else:
        num = 5
    print(np_data[index]["name"], "has", np_data[index]["total"], "windows", "and is in group", num)

#2. Estimate compaction

# get number of NP's in each window
# Get number of NPs in each window
for index in range(len(data)):
    total = 0
    for value in data[index]:
        total += value
    window_data[index]["total"] = total

# built in sort functoin to sort the list by total number of windows
window_data.sort(key=lambda window: window["total"])

size = len(window_data)
# cateogrize the windows into 10 groups
for index in range(len(window_data)):
    num = 0
    if(index < size / 10):
        num = 1
    elif(index < size / 9):
        num = 2
    elif(index < size / 8):
        num = 3
    elif(index < size / 7):
        num = 4
    elif(index < size / 6): 
        num = 5
    elif(index < size / 5):
        num = 6 
    elif(index < size / 4): 
        num = 7 
    elif(index < size / 3):
        num = 8
    elif(index < size / 2):
        num = 9
    else:
        num = 10
    #print(window_data[index]["name"], "has", window_data[index]["total"], "NP's", "and is in group", num)
