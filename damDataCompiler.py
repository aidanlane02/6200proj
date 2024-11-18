import pandas as pd
import os

folder_start = 'Data\TrainingData'
loc = '\MonumentalDown' #change for each location
folder_path = folder_start+loc

# List all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Combine all CSV files into a single DataFrame
combined_data = pd.concat([
    pd.read_csv(os.path.join(folder_path, file)).iloc[:-14]  # Exclude last 14 rows
    for file in csv_files
])

# Save the combined data to a new CSV file
output_start = 'Data\TrainingData'
output_end = 'Training.csv'
output_path = output_start+loc+output_end
combined_data.to_csv(output_path, index=False)
