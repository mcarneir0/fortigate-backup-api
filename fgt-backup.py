import os
import csv
import sys
import requests
from datetime import datetime

# The req object is used to make https requests
req = requests.session()

# Uncomment these two lines below to disable SSL certificate warnings
# requests.packages.urllib3.disable_warnings()
# req.verify = False

# Global variables
DATE = datetime.now().strftime('%m-%d-%Y')      # Today's date in the format mm-dd-yyyy
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))   # Path to the directory where this script is located
BKP_FOLDER = os.path.join(CURRENT_DIR, 'backups', DATE)     # Path to the backups folder
LOGS_FOLDER = os.path.join(CURRENT_DIR, 'logs')     # Path to the logs folder

def main():

    # Read the fortigates.csv file
    fortigates = read_fortigates()
    
    # Create folders for backups and logs if they don't exist
    create_folders()

    # Create log file
    log = create_log()
    log.write(f'Backup log - {DATE}\n')

    # Backup each Fortigate
    for fgt in fortigates:
        print('\n========================================')
        print(f'Fortigate: {fgt["name"]}')
        
        # Call the main backup function
        bkp_ok = backup(fgt)

        log.write('\nBackup successful!\n') if bkp_ok else log.write('\nBackup failed!\n')
        log.write('========================================\n')
        log.write(f'Fortigate: {fgt["name"]}\n')
        log.write(f'Date: {DATE}\n')
        log.write('========================================\n')
    
    log.close()
    print('Backup finished!')
    input('Press ENTER to exit...')
    sys.exit()

def read_fortigates():

    try:
        # Read the fortigates.csv file and convert it to a list of dictionaries
        with open(os.path.join(CURRENT_DIR, 'fortigates.csv'), 'r') as file:
            fortigates = list(csv.DictReader(file, delimiter=','))
    except FileNotFoundError as e:
        print(f'File fortigates.csv not found: {e}')
        sys.exit()
    except Exception as e:
        print(f'Error reading fortigates.csv file: {e}')
        sys.exit()

    return fortigates

def create_folders():

    try:
        # Create the backups and logs folders if they don't exist
        # exist_ok=True prevents the function from raising an exception if the folder already exists
        os.makedirs(BKP_FOLDER, exist_ok=True)
        os.makedirs(LOGS_FOLDER, exist_ok=True)
    except Exception as e:
        print(f'Error creating folders: {e}')
        sys.exit()

def create_log():
    
    try:
        # Create log file and remain it open to write
        return open(os.path.join(LOGS_FOLDER, f'bkp-{DATE}.log'), 'a')
    except Exception as e:
        print(f'Error creating the log file: {e}')
        sys.exit()

def backup(fgt):

    # Mount the backup URL
    url = mount_url(fgt)
    if not url:
        print('Fortigate offline!')
        print('========================================\n')
        return False

    # Perform the backup
    print('Fortigate online, backing up...')
    try:
        bkp_data = req.get(url)
    except Exception as e:
        print(f'Backup failed: {e}')
        print('========================================\n')
        return False

    # Save and check the backup file
    file_ok = save_and_check_file(fgt['name'], bkp_data)
    
    print('Backup successful!') if file_ok else print('Backup failed!')
    print('========================================\n')
    return file_ok

def ping(ip):

    # Do a simple request to the Fortigate to check if it is online
    try:
        req.get(f'https://{ip}', timeout=3)
        return True
    except:
        return False

def check_online_ip(fgt):

    # Check if the Fortigate is online on primary IP
    if ping(fgt['ip_1']):
        return fgt["ip_1"]
    
    # If not, check if the Fortigate has a secondary IP and if it is online
    elif fgt['ip_2'] != '' and ping(fgt['ip_2']):
        return fgt["ip_2"]
    
    # If the Fortigate is not available on any IP, return False
    return False

def mount_url(fgt):

    # URI to backup the Fortigate
    URI = '/api/v2/monitor/system/config/backup?scope=global&access_token='

    # Check if the Fortigate is online on both IPs
    is_online = check_online_ip(fgt)
    if is_online:
        # If it is online, mount the URL to backup the Fortigate
        return f'https://{is_online}{URI}{fgt["token"]}'
    else:
        return False
    
def save_and_check_file(name, data):

    # Path to the backup file
    file_path = os.path.join(BKP_FOLDER, f'{name}-bkp-{DATE}.conf')
    
    try:
        # Save the backup data to a file
        with open(file_path, 'wb') as file:
            for line in data:
                file.write(line)

        # Check if the file is a valid Fortigate configuration file
        with open(file_path, 'r') as file:
            first_line = file.readline()
            return first_line.startswith('#config')
    
    except Exception as e:
        print(f'Error saving backup file: {e}')
        return False
        
if __name__ == '__main__':
    main()
