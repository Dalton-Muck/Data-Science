# Dalton Muck
# CS4150 Activity #10
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

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

# interactive heat map of the normalized linkage values
def plot_normalized_linkage_heatmap(normal_linkage, hist1_window_data):
    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Create a heatmap using the normalized linkage values
    heatmap = ax.imshow(normal_linkage, cmap="hot", interpolation="nearest")

    # Add a colorbar to the heatmap
    cbar = plt.colorbar(heatmap)
    cbar.set_label("Normalized Linkage Value")  # Label for the colorbar

    # Set the title and axis labels for the heatmap
    plt.title("Normalized Linkage Hist1 Region")
    plt.xlabel("Window")
    plt.ylabel("Window")

    # Set ticks to increment every 10 for both rows and columns
    num_windows = len(hist1_window_data)  # Total number of windows
    plt.xticks(ticks=range(0, num_windows, 10), labels=range(0, num_windows, 10))  # X-axis ticks
    plt.yticks(ticks=range(0, num_windows, 10), labels=range(0, num_windows, 10))  # Y-axis ticks

    # Create an annotation object to display value and coordinates on hover
    annot = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)  # Initially hide the annotation

    # Function to update the annotation with the hovered cell's information
    def update_annot(event):
        if event.inaxes == ax:  # Check if the event occurred within the heatmap axes
            x, y = int(event.xdata + 0.5), int(event.ydata + 0.5)  # Get the cell coordinates
            if 0 <= x < num_windows and 0 <= y < num_windows:  # Ensure coordinates are within bounds
                annot.xy = (x, y)  # Set the annotation position
                value = normal_linkage[y][x]  # Get the value at the hovered cell
                annot.set_text(f"X: {x}, Y: {y}\nValue: {value:.4f}")  # Set the annotation text
                annot.set_visible(True)  # Make the annotation visible
            else:
                annot.set_visible(False)  # Hide the annotation if out of bounds

    # Function to handle hover events and update the annotation
    def on_hover(event):
        update_annot(event)  # Update the annotation with the current hover event
        fig.canvas.draw_idle()  # Redraw the canvas to reflect changes

    # Connect the hover event to the on_hover function
    fig.canvas.mpl_connect("motion_notify_event", on_hover)

    # Display the heatmap
    plt.show()

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

plot_normalized_linkage_heatmap(normal_linkage, hist1_window_data)