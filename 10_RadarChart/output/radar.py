# Dalton Muck
# CS4150 Activity #10
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

def correlation(hist1_features, hist1_data, windows, nps, feature, cluster_idx, cluster_name):
    correlation_list = []
    # nuclear profiles
    for i in range(nps):
        numerator = 0
        denominator = 0
        # rows
        for j in range(windows):
            # check if feature is present in NP and is in cluster
            if hist1_data[j][i] == 1 and Jaccard[i][cluster_idx]["class"] == cluster_name:
                denominator += 1
                # check if feature is present in window
                if hist1_features[j][feature] >= 1:
                    numerator += 1
            # correct for division by zero
            if denominator != 0:
                correlation_list.append(numerator / denominator)
            else:
                correlation_list.append(0)
    # return correlation percentage 
    return sum(correlation_list) / len(correlation_list) if correlation_list else 0

def calculate_feature_correlation(hist1_features, hist1_data, hist1_np_data, feature_col, medoid_x, medoid_y, medoid_z):
    feature_x = []
    feature_y = []
    feature_z = []
    # get list of correlation values for each feature
    # do this 15 times for each cluster, 45 total
    for feature in feature_col:
        feature_x.append(correlation(hist1_features, hist1_data, len(hist1_data), len(hist1_np_data), feature, medoid_x, "x"))
        feature_y.append(correlation(hist1_features, hist1_data, len(hist1_data), len(hist1_np_data), feature, medoid_y, "y"))
        feature_z.append(correlation(hist1_features, hist1_data, len(hist1_data), len(hist1_np_data), feature, medoid_z, "z"))

    return feature_x, feature_y, feature_z

def plot_radar_chart(feature_x, feature_y, feature_z, feature_names):
    # Labels for each feature
    labels = feature_names
    # Number of variables/features
    num_vars = len(labels)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # The radar chart is a circle, so we need to "complete the loop"
    # and append the start value to the end.
    feature_x += feature_x[:1]
    feature_y += feature_y[:1]
    feature_z += feature_z[:1]
    angles += angles[:1]

    # Create a subplot with polar projection
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    # Fill the area for each cluster
    ax.fill(angles, feature_x, color='red', alpha=0.25, label='Cluster x')
    ax.fill(angles, feature_y, color='blue', alpha=0.25, label='Cluster y')
    ax.fill(angles, feature_z, color='green', alpha=0.25, label='Cluster z')

    # Draw the outline for each cluster
    ax.plot(angles, feature_x, color='red', linewidth=2)
    ax.plot(angles, feature_y, color='blue', linewidth=2)
    ax.plot(angles, feature_z, color='green', linewidth=2)

    # Draw one axis per variable and add labels
    max_value = max(max(feature_x), max(feature_y), max(feature_z))
    yticks = np.arange(0, max_value + 0.05, 0.05)
    yticklabels = [f'{tick:.2f}' for tick in yticks]
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # Add a legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    # Set the title of the plot
    plt.title('Feature Correlation for Clusters', pad=20)
    # Display the plot
    plt.show()

# Open the file for remmading
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
    # Read the first row for feature names
    feature_names = file.readline().strip().split(",")[1:]

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

# Get random medoids
for i in range(0, 100):
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


#Print medoids
print("medoid_x: ", medoid_x, "medoid_y: ", medoid_y, "medoid_z: ", medoid_z)

# The list of features to test
feature_names = [
    "CTCF-7BWU",
    "NANOG",
    "LAD",
    "RNAPII-S5P",
    "RNAPII-S7P",
    "h3k27me3",
    "Hist1",
    "Vmn",
    "H3K9me3",
    "pou5f1",
    "sox2",
    "H3K36me3",
    "RNAPII-S2P",
    "Enhancer",
    "H3K20me3",
]
feature_col = [3, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 22]

# Calculate feature correlations
# Each list will contain the average correlation for each feature for each cluster
# each list is of size 15
feature_x, feature_y, feature_z = calculate_feature_correlation(hist1_features, hist1_data, hist1_np_data, feature_col, medoid_x, medoid_y, medoid_z)

# Call the function to plot the radar chart
plot_radar_chart(feature_x, feature_y, feature_z, feature_names)


# Print the Jaccard Similarity Matrix with the values and classes for the 3 clusters
with open("/Users/tm033520/Documents/4150/Data-Science/10_RadarChart/output/Value&Class.txt", "w") as file:
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
with open("/Users/tm033520/Documents/4150/Data-Science/10_RadarChart/output/Class.txt", "w") as file:
    # Write header
    file.write("        " + "  ".join([hist1_np_data[idx]["name"] for idx in [medoid_x, medoid_y, medoid_z]]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for idx in [medoid_x, medoid_y, medoid_z]:
            file.write(str(Jaccard[i][idx]["class"] + "      "))
        file.write("\n")

# Print the Jaccard Similarity Matrix with only the values for the 3 clusters
with open("/Users/tm033520/Documents/4150/Data-Science/10_RadarChart/output/Value.txt", "w") as file:
    # Write header
    file.write("        " + "   ".join([hist1_np_data[idx]["name"] for idx in [medoid_x, medoid_y, medoid_z]]) + "\n")
    for i in range(len(Jaccard)):
        file.write(hist1_np_data[i]["name"] + "\t")
        for idx in [medoid_x, medoid_y, medoid_z]:
            # round to 5 digits
            formatted_value = f"{Jaccard[i][idx]['value']:.5f}"
            file.write(formatted_value + "\t")
        file.write("\n")