import json
import pandas as pd

# Variable Initialization
output_folder = ""

# Load the JSON file into a list of dictionary
with open('all_parts.json') as data_file:
    json_data = data_file.read()

parts = json.loads(json_data)

total_parts = len(parts)

# Sort the parts so that we have one list of dictionary per part_type
sorted_parts = {}
for part in parts:
    part_type = part['part_type']
    if part_type not in sorted_parts:
        sorted_parts[part_type] = []
    sorted_parts[part_type].append(part)

# Write these parts into different .csv
# and
# Create a summary of the dataset to output at the command line
print("Total Number of Parts Scraped : " + str(total_parts) + "parts")
for part_type in sorted_parts.keys():
    filepath = output_folder + part_type + ".csv"

    # Creating the dataframe
    parts = sorted_parts[part_type]
    part_df = pd.DataFrame(parts) 
    part_df.to_csv(filepath,index=False)

    print(part_type + " : " + str(len(parts)) + " parts")




