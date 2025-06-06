import logging
import requests
import utils.io as io

PING_TIMEOUT = 3                                            # Number of seconds to wait for a ping response
URI = '/api/v2/monitor/system/config/backup?scope=global'   # URI to backup the Fortigate

# Setup session for HTTPS requests
req = requests.session()

# Comment these two lines below to enable SSL certificate checks
requests.packages.urllib3.disable_warnings()
req.verify = False

def ping(ip):
    """Check if the Fortigate is online via a simple HTTPS request."""
    try:
        logging.debug(f'Pinging https://{ip}')
        req.get(f'https://{ip}', timeout=PING_TIMEOUT)
        return True
    except:
        return False

def backup(ip, apikey):
    """Perform a backup of the Fortigate."""
    # Perform the backup
    try:
        logging.debug(f'Backing up https://{ip}{URI}')
        logging.debug(f'Apikey: {apikey}')
        res = req.post(f'https://{ip}{URI}', headers={'Authorization' : f'Bearer {apikey}'})

        # Check if the backup was successful
        if res.status_code == 200 and res.text.startswith('#config'):
            logging.debug(f'Backup data received from https://{ip}{URI}')
            logging.debug(f'Backup data length: {len(res.text)} bytes')
            req.close()
            return True, res.text
    except Exception:
        logging.exception(f'Failed to backup https://{ip}{URI}', exc_info=True)
        return False, ''

def attempt_backup(ip, apikey, name):
    """Perform full backup routine: ping, backup and save file."""
    if ping(ip):
        logging.info(f'https://{ip} is online, performing backup...')
        bkp_success, bkp_data = backup(ip, apikey)
        if bkp_success:
            if io.save_backup_file(name, bkp_data):
                logging.info('Backup file saved successfully')
                return True
            else:
                logging.error('Failed to save backup file')
        else:
            logging.error(f'Failed to backup https://{ip})')
    else:
        logging.warning(f'https://{ip} is offline')
    return False
