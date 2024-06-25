#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import os
from tabulate import tabulate

# Function to read CSV files and return data as a dictionary
def read_csv(filename, key_column):
    data = {}
    with open(filename, 'r', encoding='latin1') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row.pop(key_column)  # Use the specified key column
            data[key] = row
    return data

# Function to search for a column value in all CSV files
def search_csv_files(csv_files, user_data, key_column):
    all_results = {}
    for filename in csv_files:
        results = {}
        data = read_csv(filename, key_column)
        for user_key, user_value in user_data.items():
            if user_key in data:
                results[user_key] = data[user_key]
        if results:
            all_results[filename] = results
    return all_results

# Path where the user CSV file is located
user_csv_file_path = input("Enter the path of your CSV file: ")

# Check if the entered file path is valid
if not os.path.exists(user_csv_file_path):
    print("The specified file path does not exist.")
    exit()

# Ask user for the column name to be used as key for comparison
key_column = input("Enter the column name to use as key for comparison: ")

# Read CSV file entered by user
user_data = read_csv(user_csv_file_path, key_column)

# Path where other CSV files are located
csv_directory = input("Enter the path of the directory containing the CSV files to search: ")

# Change directory to the location of other CSV files
if not os.path.exists(csv_directory):
    print("The specified directory path does not exist.")
    exit()
os.chdir(csv_directory)

# Automatically detect CSV files in the specified directory
csv_files = [file for file in os.listdir() if file.endswith('.csv')]

# Search for the value in all detected CSV files
results = search_csv_files(csv_files, user_data, key_column)

# Ask user for the path to save the result CSV files
save_directory = input("Enter the path of the directory to save the result CSV files: ")

# Check if the save directory path is valid
if not os.path.exists(save_directory):
    print("The specified save directory path does not exist.")
    exit()

# Print the results in table form and save to CSV file
if results:
    for filename, data in results.items():
        print(f"Results from {filename}:")
        table_data = [[key] + list(value.values()) for key, value in data.items()]
        headers = [key_column] + list(data[next(iter(data))].keys())
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        # Save to CSV file
        csv_filename = os.path.join(save_directory, f"{filename}_results.csv")
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(table_data)
        print(f"Results saved to '{csv_filename}'\n")
else:
    print("No matching results found.")

