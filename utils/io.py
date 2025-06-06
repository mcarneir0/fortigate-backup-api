import logging
import csv
from pathlib import Path
from datetime import datetime

DATE = datetime.now().strftime('%Y-%m-%d')                          # Today's date in the format yyyy-mm-dd
DATETIME = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S")    # Today's date and time in the format yyyymmddTHHMMSS
CURRENT_DIR = Path(__file__).parent.resolve().parents[0]            # Path to the directory where the main file is located
BKP_FOLDER = Path.joinpath(CURRENT_DIR, 'backups', DATE)            # Path to the backups folder
LOGS_FOLDER = Path.joinpath(CURRENT_DIR, 'logs')                    # Path to the logs folder
FORTIGATES_FILE = Path.joinpath(CURRENT_DIR, 'fortigates.csv')      # Path to the fortigates.csv file
is_manual_backup = False

def create_folders():
    """Create the backups and logs folders if they don't exist."""
    try:
        # Create the backups and logs folders if they don't exist
        # parents=True creates the parent directories if they don't exist
        # exist_ok=True prevents the function from raising an exception if the folder already exists
        Path.mkdir(BKP_FOLDER, parents=True, exist_ok=True)
        Path.mkdir(LOGS_FOLDER, parents=True, exist_ok=True)

    except Exception as e:
        print(f'IO ERROR: Could not create folders: {e}')
        exit(1)

def setup_logging():
    """Setup Pythonlogger."""
    log_type = 'manual-bkp' if is_manual_backup else 'bkp'    
    logging.basicConfig(filename=f'logs/{log_type}-{DATETIME}.log',
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        encoding='utf-8')

def read_fortigates():
    """Read the fortigates.csv file and convert it to a list of dictionaries."""
    try:
        # Read the fortigates.csv file and convert it to a list of dictionaries
        with open(FORTIGATES_FILE, 'r') as csv_file:
            fortigates = list(csv.DictReader(csv_file, delimiter=','))

        # Check if the file is empty
        if not fortigates:
            print('File fortigates.csv is empty')
            logging.error('File fortigates.csv is empty')
            exit(1)
        
        logging.info('fortigates.csv file read successfully')
        logging.debug(f'Number of Fortigates: {len(fortigates)}')
        for i, fgt in enumerate(fortigates, 1):
            logging.debug(f'{i} - Name: {fgt["name"]}, IP_1: {fgt["ip_1"]}, IP_2: {fgt["ip_2"]}, Apikey: {fgt["apikey"]}')
        
        return fortigates
    
    except FileNotFoundError:
        print(f'IO ERROR: File fortigates.csv not found')
        logging.error(f'IO ERROR: File fortigates.csv not found')
        exit(1)
    except Exception as e:
        print(f'IO ERROR: Failed to read fortigates.csv file: {e}')
        logging.exception(f'IO ERROR: Failed to read fortigates.csv file')
        exit(1)

def save_backup_file(name, bkp_data):
    """Save the backup data to a file."""
    # Path to the backup file
    if is_manual_backup:
        bkp_path = Path.joinpath(BKP_FOLDER, f'{name}-manual-bkp-{DATETIME}.conf')
    else:
        bkp_path = Path.joinpath(BKP_FOLDER, f'{name}-bkp-{DATETIME}.conf')
    logging.debug(f'Backup file path: {bkp_path}')
    
    try:
        # Save the backup data to a file
        with open(bkp_path, 'w') as bkp_file:
            bkp_file.writelines(bkp_data)       
        return True
    
    except Exception:
        logging.exception(f'IO ERROR: Failed to save backup file')
        return False
