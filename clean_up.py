import os
from datetime import datetime, timedelta

def cleanup_log_files(log_folder, end_date):
    for file_name in os.listdir(log_folder):
        if file_name.startswith("listen-") and file_name.endswith(".log"):
            file_date_str = file_name[7:15]
            try:
                file_date = datetime.strptime(file_date_str, "%Y%m%d")
            except ValueError:
                continue 
            if file_date < (end_date - timedelta(days=7)):
                file_path = os.path.join(log_folder, file_name)
                os.remove(file_path)

def main():
    current_directory = os.getcwd()
    log_folder = os.path.join(current_directory, "in")

    # Get the end date for the cleanup process
    end_date = datetime.now()

    # Clean up processed log files
    cleanup_log_files(log_folder, end_date)

if __name__ == "__main__":
    main()
