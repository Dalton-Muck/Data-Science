# Dalton Muck
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
            hist1_data.append({"values": values, "total": sum(values)})
            hist1_window_data.append({"name": row[0], "total": sum(values)})
            for i in range(len(values)):
                if values[i] != 0:
                    hist1_np_data[i]["total"] += 1

# Remove columns (and corresponding NP_data) where all values are 0
# keep columns where at least one value is not 0
columns_to_keep = [index for index, np in enumerate(hist1_np_data) if np["total"] != 0]
# Filter out unneeded data from column
hist1_data = [[row["values"][col_idx] for col_idx in columns_to_keep] for row in hist1_data]
# Filter np_data to only include relevant columns
hist1_np_data = [hist1_np_data[col_idx] for col_idx in columns_to_keep]
hist1_window_data= [{"name": hist1_window_data[i]["name"], "total": sum(hist1_data[i])} for i in range(len(hist1_data))]

# 1. Number of genomic windows
print("1. Windows:", len(hist1_data))

# 2. Number of NPs
print("2. NP:", len(hist1_np_data))

# 3. On average, how many windows(rows) are present in an NP(column)?
total_windows = sum(np["total"] for np in hist1_np_data)
average = total_windows / len(hist1_np_data)
print("3. Average Windows in NP:", average)

# 4. Smallest and largest number of windows(rows) present in any NP(column)
window_count = [np["total"] for np in hist1_np_data]
print("4. Min windows in NP:", min(window_count))
print("4. Max windows in NP:", max(window_count))

# 5. Average, smallest, and largest number of NPs in which a window is detected
NP_count = [np["total"] for np in hist1_window_data]
total = sum(NP_count)
print("5. Average NP's in window:", total / len(hist1_data))
print("5. Min NP in window:", min(NP_count))
print("5. Max NP in window:", max(NP_count))

# 6. Estimate radial position
# Get number of NPs in each window
np_data.sort(key=lambda np: np["total"])
min_total = np_data[0]["total"]
max_total = np_data[-1]["total"]
range_total = max_total - min_total
#assign each NP to a range
np_ratios = [np["total"] / range_total for np in hist1_np_data]
average_ratio = sum(np_ratios) / len(np_ratios)
print("The average radial ratio is:", average_ratio)
ranges = [0, 0, 0, 0, 0]
for ratio in np_ratios:
    if 0 <= ratio < 0.2:
        ranges[0] += 1
    elif 0.2 <= ratio < 0.4:
        ranges[1] += 1
    elif 0.4 <= ratio < 0.6:
        ranges[2] += 1
    elif 0.6 <= ratio < 0.8:
        ranges[3] += 1
    elif 0.8 <= ratio <= 1:
        ranges[4] += 1
#find the most common range
most_common_range_index = ranges.index(max(ranges))
range_labels = ["1", "2", "3", "4", "5"]
print("The most common radial position range is:", range_labels[most_common_range_index])

# 7. Estimate compaction
# Get number of NPs in each window
window_data = [{"name": row[0], "total": sum(row)} for row in data]
window_data.sort(key=lambda window: window["total"])
min_total = window_data[0]["total"]
max_total = window_data[-1]["total"]
range_total = max_total - min_total


#assign each window to a range
window_ratios = [sum(row) / range_total for row in hist1_data]
average_compaction = sum(window_ratios) / len(window_ratios)
print("The average compaction ratio is:", average_compaction)
ranges = [0] * 10
for ratio in window_ratios:
    index = int(ratio * 10)
    if index == 10:
        index = 9
    ranges[index] += 1

#find the most common range
most_common_range_index = ranges.index(max(ranges))
range_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
print("The most common compaction range is:", range_labels[most_common_range_index])
