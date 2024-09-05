import os
from datetime import datetime
import django
import logging as log
from time import sleep
from alive_progress import alive_bar  # Import alive-progress for the progress bar

log.basicConfig(level=log.DEBUG)
# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SysOpsSuite.settings")
django.setup()

from parse import parse_switch_config  # noqa: E402
from Backups.models import Backup  # noqa: E402

# Directory containing the backups
BACKUP_DIR = "/Users/jvaught/Documents/python/projects/SYSOPSSUITE/Backups/DummyData/"


def save_config_to_db(
    switch_name, device_type, backup_date, config_data, backup_status
):
    if Backup.objects.filter(switch_name=switch_name, backup_date=backup_date).exists():
        log.debug(
            f"{switch_name} backup for {backup_date} already exists in the database....Skipping"
        )
        return f"{switch_name} backup for {backup_date} already exists in the database....Skipping"
    else:
        Backup.objects.create(
            switch_name=switch_name,
            device_type=device_type,
            backup_date=backup_date,
            config_data=config_data,
            backup_status=backup_status,
        )


def extract_metadata_from_path(root, file):
    backup_date_str = os.path.basename(root)  # Example: "08-21-2024_10-35-58"

    try:
        # Attempt to parse the directory name as a date
        backup_date = datetime.strptime(backup_date_str, "%m-%d-%Y_%H-%M-%S")
    except ValueError:
        # If parsing fails, print an error and return None
        print(
            f"Skipping directory '{root}': does not match date format '%m-%d-%Y_%H-%M-%S'"
        )
        return None, None, None

    # Extracting switch name from the file name
    switch_name = file.split("_")[0]  # Example: "EAV-SW18-MDF2"

    # Assuming device type could be part of switch name or determined otherwise, set default for now
    device_type = "Unknown"

    return switch_name, device_type, backup_date


def process_backup_files(progress_callback=None):
    # First, count the total number of backup files to process
    total_files = sum(
        1
        for root, dirs, files in os.walk(BACKUP_DIR)
        for file in files
        if file.endswith(".txt")
    )

    processed_files = 0

    with alive_bar(total_files, title="Processing Backups") as bar:
        for root, dirs, files in os.walk(BACKUP_DIR):
            for file in files:
                if file.endswith(".txt"):
                    # Extract metadata from the file and directory structure
                    switch_name, device_type, backup_date = extract_metadata_from_path(
                        root, file
                    )

                    # If metadata extraction fails, skip this file
                    if not all([switch_name, device_type, backup_date]):
                        bar()  # Increment the progress bar even if skipping
                        continue

                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        config_text = f.read()
                        try:
                            # Parse the switch configuration
                            parsed_config = parse_switch_config(config_text)
                            backup_status = "Success"
                        except Exception as e:
                            print(f"Failed to parse {file_path}: {e}")
                            parsed_config = {}
                            backup_status = "Failed"

                        # Save to database
                        save_config_to_db(
                            switch_name,
                            device_type,
                            backup_date,
                            parsed_config,
                            backup_status,
                        )

                    # Sleep to simulate delay and show progress more clearly
                    sleep(1)

                    # Increment the progress bar
                    bar()

                    # Update the processed files and calculate the percentage
                    processed_files += 1
                    progress = (processed_files / total_files) * 100
                    if progress_callback:
                        progress_callback(progress)
