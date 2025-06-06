import logging
import utils.networker as net

def validate_fortigate(fgt):
    """Check if the Fortigate entry has at least one IP and an apikey."""
    logging.debug(f'Validating {fgt["name"]}')
    if not fgt['ip_1'] and not fgt['ip_2']:
        logging.warning('No IP found, check the fortigates.csv file and try again. Skipping...')
        return False
    if not fgt['apikey']:
        logging.warning('No apikey found, check the fortigates.csv file and try again. Skipping...')
        return False
    return True

def process_fortigate(fgt, fgt_ok, fgt_failed):
    """Initiate backup process for a single Fortigate."""
    logging.info('========================================')
    logging.info(f'Fortigate: {fgt["name"]}')

    if not validate_fortigate(fgt):
        fgt_failed.append(fgt['name'])
        logging.info('========================================')
        return False

    if (fgt['ip_1'] and net.attempt_backup(fgt['ip_1'], fgt['apikey'], fgt['name'])) or (
        fgt['ip_2'] and net.attempt_backup(fgt['ip_2'], fgt['apikey'], fgt['name'])):
        fgt_ok.append(fgt['name'])
        logging.info('========================================')
        return True
    else:
        fgt_failed.append(fgt['name'])
        logging.error('Backup failed on all available IPs')
        logging.info('========================================')
        return False

def select_fortigates(fortigates):
    """
    Prompt user to select Fortigates for backup.

    Accepts:
        - 'all' to select all Fortigates
        - 'exit' to quit
        - comma-separated indexes (e.g., 0,2,3)

    Returns:
        List of selected Fortigate indexes
    """
    fgt_count = len(fortigates)

    while True:
        
        selected = input('\nSelect the Fortigates to backup (separated by commas): ').strip().lower()
        logging.debug(f'User input: {selected}')

        # Check if the user typed 'all' to backup all Fortigates
        if selected == 'all':
            logging.info('Selected all Fortigates')
            return list(range(fgt_count))

        # Check if the user typed 'exit' to exit the script
        if selected == 'exit':
            logging.info('User chose to exit')
            exit(0)

        # Check if the user typed nothing
        if not selected:
            logging.error('No input provided')
            print(f'\nNo input provided. Please enter valid indexes between 0 and {len(fortigates) - 1}, separated by commas.')
            print('Or type "all" to backup all Fortigates or "exit" to quit.')
            continue

        # Split the string into a list of numbers
        try:
            indexes = [int(i) for i in selected.split(',')]
            # Check if the numbers are on the range of the Fortigates list
            if all(0 <= int(i) < len(fortigates) for i in indexes):
                logging.info('Selected Fortigates:')
                for i in indexes:
                    logging.info(f'{i}: {fortigates[i]["name"]}')
                return indexes
            else:
                raise ValueError

        except ValueError:
            logging.error(f'Invalid input: {selected}')
            print(f'\nInvalid input. Please enter valid indexes between 0 and {len(fortigates) - 1}, separated by commas.')
            print('Or type "all" to backup all Fortigates or "exit" to quit.')
