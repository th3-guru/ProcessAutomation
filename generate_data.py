#!/usr/bin/env python
# coding: utf-8

import os
import random
import string
import pycountry
from datetime import datetime


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

# Generate a random dataset for the current date
def generate_dataset(num_entries):
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


num_entries = 300000  # Adjust this based on the number of streams for the day

dataset = generate_dataset(num_entries)


current_date = datetime.now()
file_name = f"listen-{current_date.strftime('%Y%m%d')}.log"
file_path = os.path.join("in", file_name)
write_dataset_to_file(dataset, file_path)

