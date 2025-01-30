#Dalton Muck
# CS 4150 Activity #4
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
# Iterate over hist1_data to calculate totals
for row in hist1_data:
    for i in range(len(row)):
        if row[i] != 0:  # Only count non-zero values
            hist1_np_data[i]["total"] += 1


# Matrix to hold the Jaccard similarity values
# It is a NP by NP matrix where each cell holds the Jaccard similarity value
# https://en.wikipedia.org/wiki/Jaccard_index#Similarity_of_asymmetric_binary_attributes (Jaccard Similarity)
Jaccard = []


# Get the first NP column to be compared
for i in range(len(hist1_np_data)): #rows
    # Get the second NP column to be compared
    for j in range(len(hist1_np_data)): #columns
        # Reset values
        # value on left is outer loop, value on right is inner loop
        M11 = 0
        M10 = 0
        M01 = 0
        M00 = 0
        # Compare outerloop NP to all other NP's including itself
        for k in range(len(hist1_data)): #each element in column
            if(hist1_data[k][i] == 1 and hist1_data[k][j] == 1):
                M11 += 1
            elif(hist1_data[k][i] == 1 and hist1_data[k][j] == 0):
                M10 += 1
            elif(hist1_data[k][i] == 0 and hist1_data[k][j] == 1):
                M01 += 1
            else:
                M00 += 1
        # Calculate the Jaccard Similarity
        # handle dividing by zero
        if(M11 == 0):
            Jaccard.append(0)
        elif(M11+M10+M01 == 0):
            Jaccard.append(1)
        else:
            # Calculate Jaccard Similarity Index
            Jaccard.append(M11 / (M11 + M10 + M01))

# Print the Jaccard Similarity Matrix
with open("/Users/tm033520/Documents/4150/Data-Science/4_NP_Similairity/jaccard_similarity.txt", "w") as output_file:
    size = len(hist1_np_data)
    for i in range(size):
        row = Jaccard[i * size:(i + 1) * size]
        # round to 5 digits
        formatted_row = [f"{value:.5f}" for value in row]
        # label rows
        output_file.write(f"NP{i+1}: " + " ".join(formatted_row) + "\n")

