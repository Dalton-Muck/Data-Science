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

# Get random indices for centroid of classes
random_x = Jaccard[random.randint(0, len(Jaccard) - 1)][random.randint(0, len(Jaccard) - 1)]["value"]
random_y = Jaccard[random.randint(0, len(Jaccard) - 1)][random.randint(0, len(Jaccard) - 1)]["value"]
random_z = Jaccard[random.randint(0, len(Jaccard) - 1)][random.randint(0, len(Jaccard) - 1)]["value"]

# Classify each Normalized Jaccard Value into a class x, y, or z
for i in range(len(hist1_np_data)):  # columns
    for j in range(len(hist1_data)):  # each element in column
        # Calculate the distance from the random centroid
        distance_x = random_x - Jaccard[i][j]["value"]
        distance_y = random_y - Jaccard[i][j]["value"]
        distance_z = random_z - Jaccard[i][j]["value"]
        # Assign the class
        if abs(distance_x) < abs(distance_y) and abs(distance_x) < abs(distance_z):
            Jaccard[i][j]["class"] = "X"
        elif abs(distance_y) < abs(distance_z):
            Jaccard[i][j]["class"] = "Y"
        else:
            Jaccard[i][j]["class"] = "Z"

# Print the Jaccard Similarity Matrix with values and classes next to each other
with open("/Users/tm033520/Documents/4150/Data-Science/6_Clustering/output/Value&Class.txt", "w") as file:
    # Write header
    file.write("        " + "        ".join([np["name"] for np in hist1_np_data]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for j in range(len(Jaccard)):
            # round to 5 digits
            formatted_value = f"{Jaccard[i][j]['value']:.5f}"
            file.write(formatted_value + Jaccard[i][j]["class"] + "     ")
        file.write("\n")

# Print the Jaccard Similarity Matrix with only the classes
with open("/Users/tm033520/Documents/4150/Data-Science/6_Clustering/output/Class.txt", "w") as file:
    # Write header
    file.write("        " + "  ".join([np["name"] for np in hist1_np_data]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for j in range(len(Jaccard)):
            file.write(str(Jaccard[i][j]["class"] + "      "))
        file.write("\n")

# Print the Jaccard Similarity Matrix with only the values
with open("/Users/tm033520/Documents/4150/Data-Science/6_Clustering/output/Value.txt", "w") as file:
    # Write header
    file.write("        " + "   ".join([np["name"] for np in hist1_np_data]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for j in range(len(Jaccard[i])):
            # round to 5 digits
            formatted_value = f"{Jaccard[i][j]['value']:.5f}"
            file.write(formatted_value + "\t")
        file.write("\n")



