# Dalton Muck
# CS 4150 Activity #1 
# 

# Open the file for reading
filename = "/Users/tm033520/Documents/4150/Data-Science/data.txt"
data = []
names = []
# r means you are reading the file
with open(filename, "r") as file:
    # Skip the first row
    next(file)

    for line in file:
        # Split the line into a list of values
        row = line.strip().split()
        # Skip the first three elements and convert the rest to integers
        row = [int(value) for value in row[3:]]
        # Append the processed row to the 2D list
        data.append(row)


#1. Number of genomic windows
# rows

print ("1. Windows:", len(data))


#2. Number of NPs
# columns

print ("2. NP:", len(data[0]))


# 3. On average, how many windows(rows) are present in an NP(column)?

# count total number of windows
windows = 0
for row in data:
    for value in row:
        if value == 1:
            windows += 1

# divide by the total number of windows present by the number of NP's
average = windows / len(data[0])

print ("3. Average Windows in NP:", average)


# 4. What is the smallest number of windows(rows) present in any NP(column)? The largest?
# store the number of windows in each NP in this array then use min max built in function
#array the size of the number of NPs set to 0
window_count = [0] * len(data[0])

for row in data:
    for index in range(len(data[0])):
        if row[index] == 1:
            window_count[index] += 1

#smallest amount of 1's in a column
print("4. Min windows in NP: ",min(window_count))
#largest amount of 1's in a column
print("4. Max windows in NP: ",max(window_count))


# 5. On average, what is the number of NPs in which a window is detected? The smallest? The largest?

# array size of the number of windows set to 0
NP_count = [0] * len(data)

# get number of NP's in each window
for row in data:
    for index in range(len(row)):
        if row[index] == 1:
            NP_count[index] += 1

# get total number of 1's in the data
total = 0
for row in data:
    for index in range(len(row)):
        if row[index] == 1:
            total += 1

print("5. Average NP's in window: ",total / len(data))
print("5. Min NP in window: ",min(NP_count))
print("5. Max NP in window: ", len(data[0]))


