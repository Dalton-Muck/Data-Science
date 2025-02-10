# Dalton Muck
# CS4150 Activity #6

import random

# Open the file for reading
filename = "/Users/tm033520/Documents/4150/Data-Science/data.txt"
# 2D list to hold the data
data = []
# names of each window and total number of NP's in window
window_data = []
# names of each NP and total number of windows in NP
np_data = []
# names of each window in Hist1 and total number of NP's in window
hist1_data = []
# names of each NP in Hist1 and total number of windows in NP
hist1_np_data = []
# names of each window in Hist1 and total number of NP's in window
hist1_window_data = []

# Load data into structures and data array
with open(filename, "r") as file:
    # Read the first row for NP names
    first_row = file.readline().strip().split()
    np_data = [{"name": name, "total": 0} for name in first_row[3:]]
    hist1_np_data = [{"name": name, "total": 0} for name in first_row[3:]]

    for line in file:
        row = line.strip().split()
        start_pos = int(row[1])
        end_pos = int(row[2])

        values = [int(value) for value in row[3:]]
        data.append(values)
        window_data.append({"name": row[0], "total": sum(values)})

        for i in range(len(values)):
            if values[i] != 0:
                np_data[i]["total"] += 1

        if (21700000 <= start_pos <= 24100000 or 21700000 <= end_pos <= 24100000) and row[0] == "chr13":
            hist1_data.append(values)
            hist1_window_data.append({"name": row[0], "total": sum(values)})
            for i in range(len(values)):
                if values[i] != 0:
                    hist1_np_data[i]["total"] += 1

# Remove columns (and corresponding NP_data) where all values are 0
columns_to_keep = [col_idx for col_idx in range(len(np_data)) if any(row[col_idx] != 0 for row in hist1_data)]
# Filter out unneeded data from column
hist1_data = [[row[col_idx] for col_idx in columns_to_keep] for row in hist1_data]
# Filter np_data to remove unwanted columns
hist1_np_data = [hist1_np_data[col_idx] for col_idx in columns_to_keep]
# Filter window_data update totals since some columns were removed
hist1_window_data = [{"name": hist1_window_data[i]["name"], "total": sum(hist1_data[i])} for i in range(len(hist1_data))]

# Matrix to hold the Jaccard similarity values
Jaccard = [[{"value": 0, "class": ""} for _ in range(len(hist1_np_data))] for _ in range(len(hist1_np_data))]

# Get the first NP column to be compared
for i in range(len(hist1_np_data)):  # rows
    # Get the second NP column to be compared
    for j in range(len(hist1_np_data)):  # columns
        # Reset values
        M11 = 0
        M10 = 0
        M01 = 0
        M00 = 0
        # Compare outerloop NP to all other NP's including itself
        for k in range(len(hist1_data)):  # each element in column
            if hist1_data[k][i] == 1 and hist1_data[k][j] == 1:
                M11 += 1
            elif hist1_data[k][i] == 1 and hist1_data[k][j] == 0:
                M10 += 1
            elif hist1_data[k][i] == 0 and hist1_data[k][j] == 1:
                M01 += 1
            else:
                M00 += 1
        # used to find min number of 1's in either column
        total_i = M11 + M10
        total_j = M11 + M01

        least_windows = min(total_i, total_j)

        # handle dividing by zero
        if M11 == 0:
            Jaccard[i][j]["value"] = 0
        elif least_windows == 0:
            Jaccard[i][j]["value"] = 1
        else:
            # Calculate Normalized Jaccard Similarity Index
            Jaccard[i][j]["value"] = M11 / least_windows
random.seed(4000)
# Get random indices for centroid of classes
medoid_x = random.randint(0, len(Jaccard) - 1)
medoid_y = random.randint(0, len(Jaccard) - 1)
while medoid_y == medoid_x:
    medoid_y = random.randint(0, len(Jaccard) - 1)
medoid_z = random.randint(0, len(Jaccard) - 1)
while medoid_z == medoid_x or medoid_z == medoid_y:
    medoid_z = random.randint(0, len(Jaccard) - 1)



iterations = 0
while (True):
    # Reset class values
    for i in range(len(hist1_np_data)):
        for j in range(len(hist1_np_data)):
            Jaccard[i][j]["class"] = ""

    # Classify each Normalized Jaccard Value into a class x, y, or z
    for i in range(len(hist1_np_data)):  # each element in row
        max_sim = max(Jaccard[i][medoid_x]["value"], Jaccard[i][medoid_y]["value"], Jaccard[i][medoid_z]["value"])
        if max_sim == Jaccard[i][medoid_x]["value"]:
            Jaccard[i][medoid_x]["class"] = "x"
        elif max_sim == Jaccard[i][medoid_y]["value"]:
            Jaccard[i][medoid_y]["class"] = "y"
        else:
            Jaccard[i][medoid_z]["class"] = "z"

    # Calculate the average similarity of each NP compared to every other NP in its class
    for i in range(len(hist1_np_data)): #iterate through each NP
        sum = 0
        count = 0
        cluster = ""

        if(Jaccard[i][medoid_x]["class"] == "x"):
            cluster = "x"
        elif(Jaccard[i][medoid_y]["class"] == "y"):
            cluster = "y"
        else:
            cluster = "z"

        for j in range(len(hist1_np_data)):
                if cluster == "x":
                    if Jaccard[j][medoid_x]["class"] == "x":
                        if j != medoid_x:
                            sum += Jaccard[i][j]["value"]
                            count += 1
                elif cluster == "y":
                    if Jaccard[j][medoid_y]["class"] == "y":
                        if j != medoid_y:
                            sum += Jaccard[i][j]["value"]
                            count += 1
                elif cluster == "z":
                    if Jaccard[j][medoid_z]["class"] == "z":
                     if j != medoid_z:
                        sum += Jaccard[i][j]["value"]
                        count += 1
        if cluster == "x":
            Jaccard[i][medoid_x]["avg"] = sum / count
        elif cluster == "y":
            Jaccard[i][medoid_y]["avg"] = sum / count
        else:
            Jaccard[i][medoid_z]["avg"] = sum / count


    # Find the NP with the highest average similarity in each class
    x_closest = max(range(len(hist1_np_data)), key=lambda idx: Jaccard[idx][medoid_x]["avg"] if Jaccard[idx][medoid_x]["class"] == "x" else -1)
    y_closest = max(range(len(hist1_np_data)), key=lambda idx: Jaccard[idx][medoid_y]["avg"] if Jaccard[idx][medoid_y]["class"] == "y" else -1)
    z_closest = max(range(len(hist1_np_data)), key=lambda idx: Jaccard[idx][medoid_z]["avg"] if Jaccard[idx][medoid_z]["class"] == "z" else -1)

    print("Max avg for x: ", Jaccard[x_closest][medoid_x]["avg"])
    print("Max avg for y: ", Jaccard[y_closest][medoid_y]["avg"])
    print("Max avg for z: ", Jaccard[z_closest][medoid_z]["avg"])
                


    print("Iteration: ", iterations)
    # Print all the x_closest, y_closest, z_closest & medoid_x, medoid_y, medoid_z
    print("x_closest: ", x_closest, "y_closest: ", y_closest, "z_closest: ", z_closest)
    print("medoid_x: ", medoid_x, "medoid_y: ", medoid_y, "medoid_z: ", medoid_z)
    prev_medoids = (medoid_x, medoid_y, medoid_z)
    if prev_medoids == (x_closest, y_closest, z_closest):
        print("Centroids are the closest to the average in their class after", iterations, "iterations.")
        break
    iterations += 1
    medoid_x = x_closest
    medoid_y = y_closest
    medoid_z = z_closest

with open("/Users/tm033520/Documents/4150/Data-Science/6_Clustering/output/Value&Class.txt", "w") as file:
    # Write header
    file.write("        " + "        ".join([hist1_np_data[idx]["name"] for idx in [medoid_x, medoid_y, medoid_z]]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for idx in [medoid_x, medoid_y, medoid_z]:
            # round to 5 digits
            formatted_value = f"{Jaccard[i][idx]['value']:.5f}"
            file.write(formatted_value + Jaccard[i][idx]["class"] + "     ")
        file.write("\n")


# Print the Jaccard Similarity Matrix with only the classes for the 3 random columns
with open("/Users/tm033520/Documents/4150/Data-Science/6_Clustering/output/Class.txt", "w") as file:
    # Write header
    file.write("        " + "  ".join([hist1_np_data[idx]["name"] for idx in [medoid_x, medoid_y, medoid_z]]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for idx in [medoid_x, medoid_y, medoid_z]:
            file.write(str(Jaccard[i][idx]["class"] + "      "))
        file.write("\n")

# Print the Jaccard Similarity Matrix with only the values for the 3 random columns
with open("/Users/tm033520/Documents/4150/Data-Science/6_Clustering/output/Value.txt", "w") as file:
    # Write header
    file.write("        " + "   ".join([hist1_np_data[idx]["name"] for idx in [medoid_x, medoid_y, medoid_z]]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for idx in [medoid_x, medoid_y, medoid_z]:
            # round to 5 digits
            formatted_value = f"{Jaccard[i][idx]['value']:.5f}"
            file.write(formatted_value + "\t")
        file.write("\n")