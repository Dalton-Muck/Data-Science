# Dalton Muck
# CS 4150 Activity #3

# Open the file for reading
filename = "/Users/tm033520/Documents/4150/Data-Science/data.txt"
data = []
window_data = []
np_data = []

# Load data into structures and data array
with open(filename, "r") as file:
    # Read the first row for NP names
    first_row = file.readline().strip().split()
    np_data = [{"name": name, "total": 0} for name in first_row[3:]]

    for line in file:
        row = line.strip().split()
        start_pos = int(row[1])
        end_pos = int(row[2])

        if (21700000 <= start_pos <= 24100000 or 21700000 <= end_pos <= 24100000) and row[0] == "chr13":
            window_data.append({"name": row[0], "total": 0})
            values = [int(value) for value in row[3:]]
            data.append(values)
            for i in range(len(values)):
                if values[i] != 0:
                    np_data[i]["total"] += 1

# Remove columns (and corresponding NP_data) where all values are 0
# keep columns where at least one value is not 0
columns_to_keep = [col_idx for col_idx in range(len(np_data)) if any(row[col_idx] != 0 for row in data)]
# Filter data
filtered_data = [[row[col_idx] for col_idx in columns_to_keep] for row in data]
# Filter np_data
filtered_np_data = [np_data[col_idx] for col_idx in columns_to_keep]

# 1. Number of genomic windows
print("1. Windows:", len(filtered_data))

# 2. Number of NPs
print("2. NP:", len(filtered_np_data))

# 3. On average, how many windows(rows) are present in an NP(column)?
windows = sum(value == 1 for row in filtered_data for value in row)
average = windows / len(filtered_np_data)
print("3. Average Windows in NP:", average)

# 4. Smallest and largest number of windows(rows) present in any NP(column)
window_count = [sum(row[index] == 1 for row in filtered_data) for index in range(len(filtered_np_data))]
print("4. Min windows in NP:", min(window_count))
print("4. Max windows in NP:", max(window_count))

# 5. Average, smallest, and largest number of NPs in which a window is detected
NP_count = [sum(row[index] == 1 for row in filtered_data) for index in range(len(filtered_data[0]))]
total = sum(sum(row) for row in filtered_data)
print("5. Average NP's in window:", total / len(filtered_data))
print("5. Min NP in window:", min(NP_count))
print("5. Max NP in window:", max(NP_count))

# 6. Estimate radial position
# Get number of NPs in each window
np_data.sort(key=lambda np: np["total"])
if np_data:
    min_total = np_data[0]["total"]
    max_total = np_data[-1]["total"]
    range_total = max_total - min_total
#assign each NP to a range
np_ratios = [sum(row) / range_total for row in filtered_data]
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
window_data = [{"name": row[0], "total": sum(row)} for row in filtered_data]
window_data.sort(key=lambda window: window["total"])
if window_data:
    min_total = window_data[0]["total"]
    max_total = window_data[-1]["total"]
    range_total = max_total - min_total

#assign each window to a range
window_ratios = [sum(row) / range_total for row in filtered_data]
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
