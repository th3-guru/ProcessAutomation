#!/usr/bin/env python
# coding: utf-8


import os
import pandas as pd
from collections import defaultdict
import pycountry
from datetime import datetime, timedelta


# Read and Parse Log Files
def parse_log_files(log_folder, start_date, end_date):
    aggregated_streams = defaultdict(lambda: defaultdict(int))
    for file_name in os.listdir(log_folder):
        if file_name.startswith("listen-") and file_name.endswith(".log"):
            file_date_str = file_name[7:15]  # Extract the date portion from the file name
            try:
                file_date = datetime.strptime(file_date_str, "%Y%m%d")
            except ValueError:
                continue  # Skip files with invalid date format
            if start_date <= file_date <= end_date:
                file_path = os.path.join(log_folder, file_name)
                with open(file_path, "r") as file:
                    for line in file:
                        try:
                            sng_id, user_id, country = line.strip().split("|")
                            aggregated_streams[country][sng_id] += 1
                            aggregated_streams[user_id][sng_id] += 1  # Personal top songs per user
                        except ValueError:
                            continue  # Skip corrupted rows
    return aggregated_streams


# Calculate Top 50 Songs per Country
def calculate_top_songs_per_country(aggregated_streams):
    top_songs_per_country = {}
    for country, streams in aggregated_streams.items():
        if country.isalpha(): 
            top_songs = sorted(streams.items(), key=lambda x: x[1], reverse=True)[:50]
            top_songs_formatted = ",".join(f"{sng_id}:{count}" for sng_id, count in top_songs)
            top_songs_per_country[country] = top_songs_formatted
    return top_songs_per_country


# Calculate Top 50 Songs per User
def calculate_top_songs_per_user(aggregated_streams):
    top_songs_per_user = {}
    for user_id, streams in aggregated_streams.items():
        if user_id.isnumeric():
            top_songs = sorted(streams.items(), key=lambda x: x[1], reverse=True)[:50]
            top_songs_formatted = ",".join(f"{sng_id}:{count}" for sng_id, count in top_songs)
            top_songs_per_user[user_id] = top_songs_formatted
    return top_songs_per_user



def is_valid_country(country_code):
    try:
        pycountry.countries.get(alpha_2=country_code)
        return True
    except LookupError:
        return False



# Main Function
def main():
    current_directory = os.getcwd()
    log_folder = os.path.join(current_directory, "in")
    output_folder = os.path.join(current_directory, "out")

    # Get date range for the last 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)

    # Read and Parse Log Files
    aggregated_streams = parse_log_files(log_folder, start_date, end_date)

    # Calculate Top 50 Songs per Country
    top_songs_per_country = calculate_top_songs_per_country(aggregated_streams)

    # Calculate Top 50 Songs per User
    top_songs_per_user = calculate_top_songs_per_user(aggregated_streams)

    # Create DataFrame from top songs per country
    df_country = pd.DataFrame.from_dict(top_songs_per_country, orient='index')
    df_country.reset_index(inplace=True)
    df_country.columns = ['Country', 'Top Songs']

    # Create DataFrame from top songs per user
    df_user = pd.DataFrame.from_dict(top_songs_per_user, orient='index')
    df_user.reset_index(inplace=True)
    df_user.columns = ['User', 'Top Songs']

    # Check the validity of country codes
    valid_country_codes = []
    for code in df_country['Country']:
        if len(code) == 2 and is_valid_country(code):
            valid_country_codes.append(code)

    df_country = df_country[df_country['Country'].isin(valid_country_codes)]

    # Split Top Songs column into separate columns
    df_country[['Song_' + str(i) for i in range(1, 51)]] = df_country['Top Songs'].str.split(',', expand=True)

    # Remove the 'Top Songs' column
    df_country.drop('Top Songs', axis=1, inplace=True)

    # Save the resulting DataFrames to output files
    output_file_country = os.path.join(output_folder, f"country_top50_{end_date.strftime('%Y%m%d')}.txt")
    output_file_user = os.path.join(output_folder, f"user_top50_{end_date.strftime('%Y%m%d')}.txt")

    df_country.to_csv(output_file_country, index=False, sep='|', header=False)
    df_user.to_csv(output_file_user, index=False, sep='|', header=False)

    print("Country Top 50 Songs:")
    print(df_country)
    print("User Top 50 Songs:")
    print(df_user)


if __name__ == "__main__":
    main()

