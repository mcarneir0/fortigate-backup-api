import logging
import utils.io as io
import utils.fortigate as fgt_util

def main():
    io.is_manual_backup = True
    io.create_folders()
    io.setup_logging()
    logging.getLogger().setLevel(logging.INFO)

    # Lists to store successful and failed backups
    fgt_ok = []
    fgt_failed = []

    logging.info('#####  Fortigate Manual Backup Log  #####')
    fortigates = io.read_fortigates()

    print('====== Fortigates Manual Backup ======\n'.rjust(50))

    # List the Fortigates
    for i in range(0, len(fortigates), 2):
        fgt1 = f'{i:3} - {fortigates[i]["name"]:<40}'
        if i + 1 < len(fortigates):
            fgt2 = f'{i+1:2} - {fortigates[i+1]["name"]}'
            print(f'{fgt1} {fgt2}')
        else:
            print(fgt1)   
    print(f'all - {"All Fortigates":<38} exit - Close the program')
    logging.info('Prompt user to select Fortigates for backup')
    selected_fortigates = fgt_util.select_fortigates(fortigates)
    backups = [fortigates[i] for i in selected_fortigates]
    
    logging.info('Starting backups...')
    print('\nStarting backups...')
    for fgt in backups:
        print(f'Backing up {fgt["name"]}...'.ljust(40), 'OK' if fgt_util.process_fortigate(fgt, fgt_ok, fgt_failed) else 'FAILED')

    logging.info('Backup results:')
    logging.info(f'{len(fgt_ok)} OK: {fgt_ok}')
    logging.info(f'{len(fgt_failed)} Failed: {fgt_failed}')
    logging.shutdown()
    
    print('\nBackup results:')
    print(f'{len(fgt_ok)} OK: {fgt_ok}')
    print(f'{len(fgt_failed)} Failed: {fgt_failed}')
    
    print(f'\nFor more details check the log file {logging.getLogger().handlers[0].baseFilename}')
    exit(0)

if __name__ == '__main__':
    main()
