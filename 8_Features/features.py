# Dalton Muck
# CS4150 Activity #6
import matplotlib.pyplot as plt
import random
import numpy as np
# Have to reset class values before classifying each NP
def reset_class_values(Jaccard, hist1_np_data):
    # Reset class values
    for i in range(len(hist1_np_data)):
        for j in range(len(hist1_np_data)):
            Jaccard[i][j]["class"] = ""

# Find the largest Jaccard value for each NP and classify it into a class
def classify_jaccard_values(Jaccard, hist1_np_data, medoid_x, medoid_y, medoid_z):
    # Classify each Normalized Jaccard Value into a class x, y, or z
    for i in range(len(hist1_np_data)):  # each element in row
        max_sim = max(Jaccard[i][medoid_x]["value"], Jaccard[i][medoid_y]["value"], Jaccard[i][medoid_z]["value"])
        max_classes = []
        if max_sim == Jaccard[i][medoid_x]["value"]:
            max_classes.append("x")
        if max_sim == Jaccard[i][medoid_y]["value"]:
            max_classes.append("y")
        if max_sim == Jaccard[i][medoid_z]["value"]:
            max_classes.append("z")
        selected_class = random.choice(max_classes)
        if selected_class == "x":
            Jaccard[i][medoid_x]["class"] = "x"
        elif selected_class == "y":
            Jaccard[i][medoid_y]["class"] = "y"
        else:
            Jaccard[i][medoid_z]["class"] = "z"

# Find the NP that has the highest average similarity to all other NP's in the same class
def calculate_average_similarity(Jaccard, hist1_np_data, medoid_idx, class_label):
    for i in range(len(hist1_np_data)):  # iterate through each NP
        sum_similarity = 0
        count = 0

        for j in range(len(hist1_np_data)):
                if Jaccard[i][medoid_idx]["class"] == class_label:
                    if Jaccard[j][medoid_idx]["class"] == class_label and j != medoid_idx:
                        sum_similarity += Jaccard[i][j]["value"]
                        count += 1

        if count > 0:
                Jaccard[i][medoid_idx]["avg"] = sum_similarity / count
        else:
                Jaccard[i][medoid_idx]["avg"] = 0

#For each cluster, find the NP whose average dissimilarity to all the objects in the cluster is minimal
def find_medoid(Jaccard, hist1_np_data, medoid_idx, class_label):
    closest_idx = -1
    max_avg = -1

    for idx in range(len(hist1_np_data)):
        if Jaccard[idx][medoid_idx]["class"] == class_label and Jaccard[idx][medoid_idx]["avg"] > max_avg:
            max_avg = Jaccard[idx][medoid_idx]["avg"]
            closest_idx = idx

    return closest_idx

# Find difference between medoid in every NP in that cluster
def variation(medoid_idx):
    total_distance = 0
    cluster_size = 0
    for i in range(len(hist1_np_data)):
        if Jaccard[i][medoid_idx]["class"] == Jaccard[medoid_idx][medoid_idx]["class"]:
            total_distance += (Jaccard[medoid_idx][medoid_idx]["value"] - Jaccard[i][medoid_idx]["value"])
            cluster_size += 1
    if cluster_size == 0:
        return 0
    return round(total_distance / cluster_size, 5)

def correlation(hist1_features, hist1_data, list, windows, nps, feature):
    for i in range(nps):
        numerator = 0
        denominator = 0
        for j in range(windows):
            if hist1_data[j][i] == 1:
                denominator += 1
                if hist1_features[j][feature] >= 1:
                    numerator += 1
        list.append(numerator / denominator)

def create_boxplot(data, tick_labels, xlabel, ylabel, title, ax):
    ax.boxplot(data, tick_labels=tick_labels)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

def plot_correlation_boxplots(np_correlation_hist1, np_correlation_lad, hist1_np_data, Jaccard, medoid_x, medoid_y, medoid_z):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Data for boxplot for Hist1
    data_hist1 = [
        [np_correlation_hist1[i] for i in range(len(hist1_np_data)) if Jaccard[i][medoid_x]["class"] == "x"],
        [np_correlation_hist1[i] for i in range(len(hist1_np_data)) if Jaccard[i][medoid_y]["class"] == "y"],
        [np_correlation_hist1[i] for i in range(len(hist1_np_data)) if Jaccard[i][medoid_z]["class"] == "z"]
    ]

    # Create boxplot for Hist1
    create_boxplot(data_hist1, ['Cluster X', 'Cluster Y', 'Cluster Z'], 'Clusters', 'Percentage of windows in an NP that contain histone genes', 'Boxplot of Histone Gene Percentage by Cluster (Hist1)', ax1)

    # Data for boxplot for LAD
    data_lad = [
        [np_correlation_lad[i] for i in range(len(hist1_np_data)) if Jaccard[i][medoid_x]["class"] == "x"],
        [np_correlation_lad[i] for i in range(len(hist1_np_data)) if Jaccard[i][medoid_y]["class"] == "y"],
        [np_correlation_lad[i] for i in range(len(hist1_np_data)) if Jaccard[i][medoid_z]["class"] == "z"]
    ]

    # Create boxplot for LAD
    create_boxplot(data_lad, ['Cluster X', 'Cluster Y', 'Cluster Z'], 'Clusters', 'Percentage of windows in an NP that contain LAD genes', 'Boxplot of LAD Gene Percentage by Cluster (LAD)', ax2)

    # Show plot
    plt.tight_layout()
    plt.show()

# Open the file for reading
datafile = "/Users/tm033520/Documents/4150/Data-Science/data.txt"
# Open file with features
features = "/Users/tm033520/Documents/4150/Data-Science/Hist1_region_features.csv"
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

with open(features, "r") as file:
    # Skip the first row for feature names
    file.readline()

    for line in file:
        row = line.strip().split(",")
        hist1_features.append([int(value) for value in row[1:]])  # Skip the first column

# LAD is the 9th column or index 8
# Hist1 is the 13th column or index 12

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


# Initialize variance variables
variance_x = 1
variance_y = 1
variance_z = 1



# Get random medoids
for i in range(0, 1000):
    # Get random indices for centroid of classes
    medoid_x = random.randint(0, len(Jaccard) - 1)
    medoid_y = random.randint(0, len(Jaccard) - 1)
    while medoid_y == medoid_x:
        medoid_y = random.randint(0, len(Jaccard) - 1)
    medoid_z = random.randint(0, len(Jaccard) - 1)
    while medoid_z == medoid_x or medoid_z == medoid_y:
        medoid_z = random.randint(0, len(Jaccard) - 1)

    # Number of times we find a new set of medoids
    iterations = 0

    while (True):

        # Save previous medoids
        prev_medoids = (medoid_x, medoid_y, medoid_z)

        reset_class_values(Jaccard, hist1_np_data)

        classify_jaccard_values(Jaccard, hist1_np_data, medoid_x, medoid_y, medoid_z)

        calculate_average_similarity(Jaccard, hist1_np_data, medoid_x, "x")
        calculate_average_similarity(Jaccard, hist1_np_data, medoid_y, "y")
        calculate_average_similarity(Jaccard, hist1_np_data, medoid_z, "z")

        x_closest = find_medoid(Jaccard, hist1_np_data, medoid_x, "x")
        y_closest = find_medoid(Jaccard, hist1_np_data, medoid_y, "y")
        z_closest = find_medoid(Jaccard, hist1_np_data, medoid_z, "z")

        #print("Iteration: ", iterations)
        #print("medoid_x: ", medoid_x, "medoid_y: ", medoid_y, "medoid_z: ", medoid_z)

        if prev_medoids == (x_closest, y_closest, z_closest):
            #print("Centroids are the closest to the average in their class after", iterations, "iterations.")
            break
        # Update medoids to the NP with the highest average similarity in each class
        medoid_x = x_closest
        medoid_y = y_closest
        medoid_z = z_closest
        iterations += 1

    # Calculate within-cluster variance and update if the new variance is better (lower) than the previous variance
    if variation(medoid_x) + variation(medoid_y) + variation(medoid_z) < (variance_x + variance_y + variance_z):
        variance_x = variation(medoid_x)
        variance_y = variation(medoid_y)
        variance_z = variation(medoid_z)


#Print medoids
print("medoid_x: ", medoid_x, "medoid_y: ", medoid_y, "medoid_z: ", medoid_z)

# Print the variance for each cluster and the total variance
print("Variance for cluster x:", variance_x)
print("Variance for cluster y:", variance_y)
print("Variance for cluster z:", variance_z)
print("Total variance:", (variance_x+variance_y+variance_z) / 3)

np_correlation_hist1 = []
np_correlation_lad = []
hist1_col = 8
lad_col = 12
# Call correlation function
correlation(hist1_features, hist1_data, np_correlation_hist1, len(hist1_window_data), len(hist1_np_data), hist1_col)
correlation(hist1_features, hist1_data, np_correlation_lad, len(hist1_window_data), len(hist1_np_data), lad_col)
# Call the function to plot the boxplots
plot_correlation_boxplots(np_correlation_hist1, np_correlation_lad, hist1_np_data, Jaccard, medoid_x, medoid_y, medoid_z)

# Print the Jaccard Similarity Matrix with the values and classes for the 3 clusters
with open("/Users/tm033520/Documents/4150/Data-Science/8_Features/output/Value&Class.txt", "w") as file:
    # Write header
    file.write("        " + "        ".join([hist1_np_data[idx]["name"] for idx in [medoid_x, medoid_y, medoid_z]]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for idx in [medoid_x, medoid_y, medoid_z]:
            # round to 5 digits
            formatted_value = f"{Jaccard[i][idx]['value']:.5f}"
            file.write(formatted_value + Jaccard[i][idx]["class"] + "     ")
        file.write("\n")

# Print the Jaccard Similarity Matrix with only the classes for the 3 clusters
with open("/Users/tm033520/Documents/4150/Data-Science/8_Features/output/Class.txt", "w") as file:
    # Write header
    file.write("        " + "  ".join([hist1_np_data[idx]["name"] for idx in [medoid_x, medoid_y, medoid_z]]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for idx in [medoid_x, medoid_y, medoid_z]:
            file.write(str(Jaccard[i][idx]["class"] + "      "))
        file.write("\n")

# Print the Jaccard Similarity Matrix with only the values for the 3 clusters
with open("/Users/tm033520/Documents/4150/Data-Science/8_Features/output/Value.txt", "w") as file:
    # Write header
    file.write("        " + "   ".join([hist1_np_data[idx]["name"] for idx in [medoid_x, medoid_y, medoid_z]]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for idx in [medoid_x, medoid_y, medoid_z]:
            # round to 5 digits
            formatted_value = f"{Jaccard[i][idx]['value']:.5f}"
            file.write(formatted_value + "\t")
        file.write("\n")