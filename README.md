<div align="center"><img src="https://raw.githubusercontent.com/mcarneir0/fortigate-backup-api/refs/heads/assets/logo.png" alt="Logo" style="display:block;float:none;margin-left:auto;margin-right:auto;width:60%"></div>

# Fortigate Config Backup Tool

This simple script makes it easy to perform backups of several Fortigate firewalls. It reads a list of Fortigates from a CSV file, performs a backup of each one and saves the backup file in a local directory.

## Summary

- [Installation](#installation)
- [Usage](#usage)
  - [Debug mode](#debug-mode)
- [Configuration](#configuration)
  - [CSV file](#csv-file-format)
  - [SSL certificate](#ssl-certificate-warnings)
  - [Project structure](#project-structure)
- [Generating API key](#generating-the-api-key)
  1. [Access the firewall](#1-access-the-firewall)
  2. [Create REST API user](#2-create-a-new-rest-api-admin)
  3. [_Super_admin_ permission](#3-grant-super_admin-permissions-to-the-user)
- [Support for](#support-for)
- [References](#references)
- [License](#license)


## Installation

#### Requirements

- [Python 3.8](https://www.python.org/downloads/) or newer
- [Requests](https://pypi.org/project/requests/) module

Clone the project

```bash
git clone https://github.com/mcarneir0/fortigate-backup-api.git
```

Go to project folder.

```bash
cd fortigate-backup-api
```

Install dependencies.

```bash
pip install -r requirements.txt
```

## Usage

Add the details of each Fortigate to backup in the `fortigates.csv` file and then you can perform the backup in two ways:

1. Run the `fgt-backup.py` file to perform a backup of all Fortigates without user input. Useful for use with cron job or scheduled tasks.
    ```bash
    python fgt-backup.py
    ```
2. Run the `manual-backup.py` file to display a list of all Fortigates and then select which Fortigates will be backed up.
    ```bash
    python manual-backup.py
    ```

### Debug mode

Additionally, you can use the `-d` or `--debug` option to enable debug logging.

```bash
python fgt-backup.py -d
python manual-backup.py -d
```

## Configuration

### CSV file format

The `fortigates.csv` file should have the following format:

```csv
name,ip_1,ip_2,apikey
Fortigate1,192.168.1.1,,xxxxxxxxxxxxxxxxx
Fortigate2,10.0.0.1:9999,myfortigate.fortiddns.com:9999,yyyyyyyyyyyyyyyyy
```

> [!TIP]
> FQDN addresses can be used too!

Where:

- `name`: A name to identify the Fortigate
- `ip_1`: Primary IP/FQDN address of the Fortigate
- `ip_2`: Secondary IP/FQDN address of the Fortigate (optional)
- `apikey`: API key provided by the Fortigate

#### Notes:

1. If you are using a custom administrative port (other than 443) you should include it with the IP address in `<IP>:<PORT>` format.
2. If your Fortigate does not have a secondary IP address, just leave it blank as `Fortigate1` example.

### SSL certificate warnings

Starting in version v0.6.0, the script does not check for SSL certificates by default anymore and will not display warnings if you are using self-signed certificates.

If you still want to enable SSL certificate checks, comment the following lines in the `utils/networker.py` file:

```python
# Comment these two lines below to enable SSL certificate checks
requests.packages.urllib3.disable_warnings()
req.verify = False
```

### Project structure

The main scripts are located in the root directory of the project. The `utils` folder contains some functions used by the main scripts. While the scripts are running, the `backups` and `logs` folders are created to store the backups and logs in the following structure:

- `backups/yyyy-mm-dd`: Contains the backup files for each Fortigate in the format `bkp-<fortigate_name>-<datetime>.conf` or `manual-bkp-<fortigate_name>-<datetime>.conf` if you are using the `manual-backup.py` script.
- `logs/`: Contains the log files in the format `bkp-<datetime>.log` or `manual-bkp-<datetime>.log` if you are using the `manual-backup.py` script.

> [!NOTE]
> The datetime used in the file names is obtained as soon as the script is started and is the same for all files. The datetime format is `yyyy-mm-ddTHHMMSS`.

## Generating the API key

The main reason to use the API key is that you don't need to enter your login credentials anywhere or access the firewall directly.

But to do it so you need to create a _REST API Admin_ with _super_admin_ rights firstly. Follow the steps below.

### 1. Access the firewall
    
Login to the firewall GUI with your credentials and make sure you have _super_admin_ rights.

### 2. Create a new _REST API Admin_

Click on System > Administrators and create a new _REST API Admin_.

<img src="https://raw.githubusercontent.com/mcarneir0/fortigate-backup-api/refs/heads/assets/02-new-rest-api-admin.png" alt= "Create admin option" title="Create admin option">

Insert a username, comments (optional), select any profile from the list (will be changed later), disable _PKI Group_ and _CORS_.

<img src="https://raw.githubusercontent.com/mcarneir0/fortigate-backup-api/refs/heads/assets/03-new-rest-admin.png" alt="Creating admin user" width="800" height="380" title="Creating admin user">

> [!IMPORTANT]
> _Trusted Hosts_ is optional on FortiOS 7.x but mandatory on 6.x versions.

> [!WARNING]
> It is **strongly recommended that you fill in your IP or network range** in _Trusted Hosts_ to ensure that only requests made from these addresses are accepted; otherwise, **anyone with access to the API token could have unrestricted and/or unauthorized access to the firewall.**

Click OK and you will be prompted to store the generated API key in a secure location. Remember that **this key will not be fully displayed again**, so if you lose it, you will have to generate another one.

<img src="https://raw.githubusercontent.com/mcarneir0/fortigate-backup-api/refs/heads/assets/04-api-key.png" alt= "API key" title="API key">

### 3. Grant _super_admin_ permissions to the user

FortiOS doesn't allow creating _super_admin REST API_ users directly. But this permission is needed to backup other _super_admin_ users you may have on the firewall.

To do this, you need to run the following commands in the _CLI Console_, click on the option in the upper right corner to open it.

```bash
# config system api-user
(api-user) edit <username>
(<username>) set accprofile super_admin
(<username>) set vdom root
(<username>) next
(api-user) end 
```
<img src="https://raw.githubusercontent.com/mcarneir0/fortigate-backup-api/refs/heads/assets/05-cli-console-option.png" alt= "CLI option" title="CLI option" align="right">

<img src="https://raw.githubusercontent.com/mcarneir0/fortigate-backup-api/refs/heads/assets/06-cli-console.png" alt= "CLI commands" title="CLI commands">

Close the CLI and you're good to go.

## Support for

- Python 3.8.x / 3.10.x / 3.11.x / 3.12.x / 3.13.x
- FortiOS 6.0.x / 6.2.x / 7.0.x / 7.2.x / 7.4.x / 7.6.x

## References

 - [FortiGate REST API Token Authentication](https://www.insoftservices.uk/fortigate-rest-api-token-authentication/)
 - [Technical Tip: Get backup config file on FortiGate using RestAPI via Python script](https://community.fortinet.com/t5/FortiGate/Technical-Tip-Get-backup-config-file-on-FortiGate-using-RestAPI/ta-p/202286)

## License

This project is licensed under the GPL-2.0 License - see the [LICENSE](https://github.com/mcarneir0/fortigate-backup-api/blob/main/LICENSE) file for details.
