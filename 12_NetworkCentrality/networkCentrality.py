# Dalton Muck
# CS4150 Activity #12
import networkx as nx
import matplotlib.pyplot as plt

# Calculates Cosegregation between all windows
def calculate_cosegregation(hist1_data, hist1_window_data, hist1_np_data):
    cosegregation = [[0 for _ in range(len(hist1_window_data))] for _ in range(len(hist1_window_data))]

    for window1 in range(len(hist1_window_data)):
        for window2 in range(len(hist1_window_data)):
            total_windows = 0
            for np1 in range(len(hist1_np_data)):
                if hist1_data[window1][np1] == 1 and hist1_data[window2][np1] == 1:
                    total_windows += 1
            cosegregation[window1][window2] = total_windows / len(hist1_np_data)
    
    return cosegregation

# Calculates the linkage between all windows
# this is the coseg value of windows minus product of detection freq of windows
def calculate_linkage(cosegregation, detection_freq, hist1_window_data):
    linkage = [[0 for _ in range(len(hist1_window_data))] for _ in range(len(hist1_window_data))]
    for window1 in range(len(hist1_window_data)):
        for window2 in range(len(hist1_window_data)):
            linkage[window1][window2] = cosegregation[window1][window2] - (detection_freq[window1] * detection_freq[window2])
    return linkage

# Calculates the Normal Linakge between all windows
# this is the linkage value of windows divided by the maximum linkage value
def calculate_normalized_linkage(linkage, detection_freq, hist1_window_data):
    normal_linkage = [[0 for _ in range(len(hist1_window_data))] for _ in range(len(hist1_window_data))]
    for window1 in range(len(hist1_window_data)):
        for window2 in range(len(hist1_window_data)):
            if linkage[window1][window2] < 0:
                denominator = min(
                    (1 - detection_freq[window1]) * (1 - detection_freq[window2]),
                    detection_freq[window1] * detection_freq[window2]
                )
            else:
                denominator = min(
                    detection_freq[window1] * (1 - detection_freq[window2]),
                    (1 - detection_freq[window1]) * detection_freq[window2]
                )
            if denominator != 0:
                normal_linkage[window1][window2] = linkage[window1][window2] / denominator
            else:
                normal_linkage[window1][window2] = 0
    return normal_linkage

# Open the file for remmading
datafile = "/Users/tm033520/Documents/4150/Data-Science/data.txt"
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
# Holds Hist1 feature data
hist1_features = []

# Load data into structures and data array
with open(datafile, "r") as file:
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

# Preprocessing
# Remove columns (and corresponding NP_data) where all values are 0
columns_to_keep = [col_idx for col_idx in range(len(np_data)) if any(row[col_idx] != 0 for row in hist1_data)]
# Filter out unneeded data from column
hist1_data = [[row[col_idx] for col_idx in columns_to_keep] for row in hist1_data]
# Filter np_data to remove unwanted columns
hist1_np_data = [hist1_np_data[col_idx] for col_idx in columns_to_keep]
# Filter window_data update totals since some columns were removed
hist1_window_data = [{"name": hist1_window_data[i]["name"], "total": sum(hist1_data[i])} for i in range(len(hist1_data))]


# Detection frequency of each widnow in Hist1
# this is the total number of NP's present in the window divided by the total number of NP's in Hist1 (163)
detection_freq = [window["total"] / len(hist1_np_data) for window in hist1_window_data]

cosegregation = calculate_cosegregation(hist1_data, hist1_window_data, hist1_np_data)

linkage = calculate_linkage(cosegregation, detection_freq, hist1_window_data)

normal_linkage = calculate_normalized_linkage(linkage, detection_freq, hist1_window_data)

# flatten the normal_linkage matrix
flattened_normal_linkage = []
for i in range(len(normal_linkage)):
    for j in range(len(normal_linkage[i])):
        if i != j:
            flattened_normal_linkage.append(normal_linkage[i][j])

# sort the flattened list
sorted_normal_linkage = sorted(flattened_normal_linkage, reverse=False)
# find the 75th percentile
threshold = sorted_normal_linkage[int(len(sorted_normal_linkage) * 0.75)]
print("Threshold:", threshold)
# evaluate if every value in  the normal_linkage matrix is greater than the threshold
# if it is greater than the threshold, set it to 1, else set it to 0
binary_normal_linkage = [[1 if normal_linkage[i][j] > threshold else 0 for j in range(len(normal_linkage[i]))] for i in range(len(normal_linkage))]

# sum the rows of the binary_normal_linkage matrix
sum_rows = [sum(row) for row in binary_normal_linkage]
# Divide the sums by the number of NP's
degree_centrality_list = [row_sum / (len(hist1_window_data)- 1) for row_sum in sum_rows]

#sort the degree_centrality_list in ascending order
degree_centrality_list = sorted(degree_centrality_list)
# print the min max and average of the degree_centrality_list
print("Degree Centrality List:")
print("Min:", degree_centrality_list[0])
print("Max:", degree_centrality_list[-1])
print("Average:", sum(degree_centrality_list) / len(degree_centrality_list))
# print the degree_centrality_list
print("Degree Centrality Values:")
with open("degree_centrality_list.txt", "w") as file:
    for i in range(1, len(degree_centrality_list) + 1):
        file.write(f"window {i} {degree_centrality_list[i - 1]}\n")



# use network x to create a graph
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# Create a graph
G = nx.Graph()
# Add nodes with attributes
for i in range(len(hist1_window_data)):
    G.add_node(i, name=hist1_window_data[i]["name"], degree_centrality=degree_centrality_list[i])
# Add edges based on the binary_normal_linkage matrix
for i in range(len(binary_normal_linkage)):
    for j in range(len(binary_normal_linkage[i])):
        if binary_normal_linkage[i][j] == 1:
            G.add_edge(i, j)
nx.draw(G, with_labels=True)
# Show the graph
plt.axis('off')
plt.show()

