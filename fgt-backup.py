import logging
import argparse
import utils.io as io
import utils.fortigate as fgt_util

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging')
args = parser.parse_args()

def main():
    io.create_folders()
    io.setup_logging()
    logging.getLogger().setLevel(logging.DEBUG if args.debug else logging.INFO)

    # Lists to store successful and failed backups
    fgt_ok = []
    fgt_failed = []

    logging.info('#####  Fortigate Backup Log  #####')
    fortigates = io.read_fortigates()

    logging.info('Starting backups...')
    for fgt in fortigates:
        fgt_util.process_fortigate(fgt, fgt_ok, fgt_failed)

    logging.info('Backup results:')
    logging.info(f'{len(fgt_ok)} OK: {fgt_ok}')
    logging.info(f'{len(fgt_failed)} Failed: {fgt_failed}')
    logging.shutdown()
    exit(0)

if __name__ == '__main__':
    main()
