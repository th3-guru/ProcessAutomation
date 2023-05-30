import os
import random
import string
import pycountry
from datetime import datetime, timedelta

# Generate a random song ID
def generate_song_id():
    return random.randint(1, 80000000)

# Generate a random user ID
def generate_user_id():
    return random.randint(1, 1000000)

# Generate a random country code
def generate_country_code():
    country_codes = [country.alpha_2 for country in pycountry.countries]
    return random.choice(country_codes)

# Generate a random log entry
def generate_log_entry():
    song_id = generate_song_id()
    user_id = generate_user_id()
    country = generate_country_code()
    return f"{song_id}|{user_id}|{country}"

# Generate a random dataset for a given date
def generate_dataset_for_date(date, num_entries):
    dataset = []
    for _ in range(num_entries):
        log_entry = generate_log_entry()
        dataset.append(log_entry)
    return dataset

# Write the dataset to a file
def write_dataset_to_file(dataset, file_path):
    with open(file_path, 'w') as file:
        for log_entry in dataset:
            file.write(f"{log_entry}\n")

# Check if a log file exists for a specific date
def log_file_exists(date):
    file_name = f"listen-{date.strftime('%Y%m%d')}.log"
    file_path = os.path.join("in", file_name)
    return os.path.isfile(file_path)

def main():
    current_directory = os.getcwd()
    log_folder = os.path.join(current_directory, "in")
    output_folder = os.path.join(current_directory, "out")

    # Get the date range for the last 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)

    # Check if log files exist for each day within the date range and generate dataset and write to a new log file for the missing date
    for i in range(7):
        date = start_date + timedelta(days=i)
        if not log_file_exists(date):
            dataset = generate_dataset_for_date(date, num_entries)
            file_name = f"listen-{date.strftime('%Y%m%d')}.log"
            file_path = os.path.join(log_folder, file_name)
            write_dataset_to_file(dataset, file_path)

    # Generate dataset for the current date and write to a log file
    if not log_file_exists(end_date):
        dataset = generate_dataset_for_date(end_date, num_entries)
        file_name = f"listen-{end_date.strftime('%Y%m%d')}.log"
        file_path = os.path.join(log_folder, file_name)
        write_dataset_to_file(dataset, file_path)

if __name__ == "__main__":
    num_entries = 300000  # Adjust this based on required number of streams per day
    main()
