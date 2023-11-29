import json
import os
import re
import shutil
import sys

def process_file(file_path):
    # Read the data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Filter out any dictionaries containing "0.00" or empty strings
    filtered_data = [item for item in data if not any(value == "0.00" or value == "" for value in item.values())]

    return filtered_data

def save_processed_data(original_file_path, processed_data):
    # Check if processed data is empty
    if not processed_data:
        print(f"No data to save for {original_file_path}, all fields were '0.00' or empty")
        return None

    # Extract the integer from the original filename
    match = re.search(r"_truncated_(\d+)", original_file_path)
    if match:
        int_part = match.group(1)
        new_file_name = re.sub(r"_truncated_\d+", f"_prepared_{int_part}", original_file_path)
    else:
        print(f"Could not find integer pattern in {original_file_path}")
        return None

    # Save the processed data to the new file
    with open(new_file_name, 'w') as file:
        json.dump(processed_data, file, indent=4)

    return new_file_name

def move_to_cache(file_path, cache_directory):
    # Move the file to the cache directory
    shutil.move(file_path, os.path.join(cache_directory, os.path.basename(file_path)))

def get_processed_files(cache_directory):
    processed_files = set()

    # Add files from the cache directory
    if os.path.exists(cache_directory):
        for filename in os.listdir(cache_directory):
            if filename.endswith('.txt'):
                processed_files.add(filename)

    return processed_files

def process_directory():
    # Get the directory of the script
    directory_path = os.path.dirname(os.path.realpath(__file__))
    cache_directory = os.path.join(directory_path, "truncated_cache")

    # Get a set of all processed files from the cache directory
    processed_files = get_processed_files(cache_directory)

    # Pattern to match files ending with _truncated_[int].txt
    pattern = re.compile(r"_truncated_\d+\.txt$")

    # Process each matching file in the directory
    for filename in os.listdir(directory_path):
        if pattern.search(filename) and filename not in processed_files:
            file_path = os.path.join(directory_path, filename)
            processed_data = process_file(file_path)
            new_file_name = save_processed_data(file_path, processed_data)
            if new_file_name:
                print(f"Processed {filename}, saved to {new_file_name}")
                # Move the original file to the cache
                move_to_cache(file_path, cache_directory)
                # Add filename to the set of processed files
                processed_files.add(filename)

# Run the processing function
process_directory()
