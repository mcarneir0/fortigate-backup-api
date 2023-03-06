
# Fortigate Config Backup Tool

This simple script makes it easy to perform backups of multiple Fortigate firewalls. It reads a list of Fortigates from a CSV file, performs a backup of each one, and saves the backup file to a local directory.

## Summary

- [Installation](https://github.com/mcarneir0/fortigate-backup-api#installation)
- [Usage](https://github.com/mcarneir0/fortigate-backup-api#usage)
- [Configuration](https://github.com/mcarneir0/fortigate-backup-api#configuration)
  - [CSV file](https://github.com/mcarneir0/fortigate-backup-api#csv-file-format)
  - [SSL certificate](https://github.com/mcarneir0/fortigate-backup-api#ssl-certificate-warnings)
  - [Folders](https://github.com/mcarneir0/fortigate-backup-api#folder-structure)
- [Generating API key](https://github.com/mcarneir0/fortigate-backup-api#generating-the-api-key)
  1. [Access the firewall](https://github.com/mcarneir0/fortigate-backup-api#1-access-the-firewall)
  2. [Temp profile](https://github.com/mcarneir0/fortigate-backup-api#2-create-a-temporary-admin-profile)
  3. [Create REST API user](https://github.com/mcarneir0/fortigate-backup-api#3-create-a-new-rest-api-admin)
     - [Trusted hosts warning](https://github.com/mcarneir0/fortigate-backup-api#warning)
  4. [_Super_admin_ permission](https://github.com/mcarneir0/fortigate-backup-api#4-grant-super_admin-permissions-to-the-user)
- [Environment](https://github.com/mcarneir0/fortigate-backup-api#environment)
- [References](https://github.com/mcarneir0/fortigate-backup-api#references)
- [License](https://github.com/mcarneir0/fortigate-backup-api#license)


## Installation

#### Requirements

- [Python 3.6](https://www.python.org/downloads/) or newer
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

1. Add the details of each Fortigate to backup in the `fortigates.csv` file.
2. Run the script.
    ```bash
    python fgt-backup.py
    ```

## Configuration

### CSV file format

The `fortigates.csv` file should have the following format:

```csv
name,ip_1,ip_2,token
Fortigate1,192.168.1.1,,xxxxxxxxxxxxxxxxx
Fortigate2,10.0.0.1:9999,myfortigate.fortiddns.com:9999,yyyyyyyyyyyyyyyyy
```
> FQDN addresses can be used too!

Where:

- `name`: A name to identify the Fortigate
- `ip_1`: Primary IP address of the Fortigate
- `ip_2`: Secondary IP address of the Fortigate (optional)
- `token`: API key provided by the Fortigate

#### Notes:

1. If you are using a custom administrative port (other than 443) you should include with the IP address with `<IP>:<PORT>` format.
2. If your Fortigate does not have a secondary IP address, just leave it blank as `Fortigate1` example.

### SSL certificate warnings

By default, the script verifies the SSL certificate of the Fortigates. **If you have self-signed certificates, you may want to disable this feature.** To do so, uncomment the following two lines at the beginning of the script:

```python
# requests.packages.urllib3.disable_warnings()
# req.verify = False
```

### Folder structure

The script creates two folders:

- `backups`: Contains the backup files.
- `logs`: Contains the log files.

The backup files are saved in a subfolder on `backups` with the current date in the format mm-dd-yyyy.

The log files are saved in the `logs` folder with the name `bkp-<current_date>.log`.

## Generating the API key

The main reason to use the API key is that you don't need to enter your login credentials anywhere or access the firewall directly.

But to do it so you need to create a _REST API Admin_ with _super_admin_ rights firstly. Follow the steps below.

### 1. Access the firewall
    
Login to the firewall GUI with your credentials and make sure you have _super_admin_ rights.

### 2. Create a temporary Admin Profile

Click on System > Admin Profiles and create a new Admin Profile with no permissions.

<img src="https://github.com/mcarneir0/fortigate-backup-api/blob/assets/01-new-admin-profile.png" alt="Creating admin profile" width="640" height="380" title="Creating admin profile">

### 3. Create a new _REST API Admin_

Click on System > Administrators and create a new _REST API Admin_.

<img src="https://github.com/mcarneir0/fortigate-backup-api/blob/assets/02-new-rest-api-admin.png" alt= "Create admin option" title="Create admin option">

Insert a username, commentary (optional), select the administrator profile created, disable _PKI Group_ and _CORS_.

<img src="https://github.com/mcarneir0/fortigate-backup-api/blob/assets/03-new-rest-admin.png" alt="Creating admin user" width="800" height="380" title="Creating admin user">

> _Trusted Hosts_ is optional on FortiOS 7.x but mandatory on 6.x versions.

### WARNING!

It is **highly recommended that you fill in your IP or network** in the _Trusted Hosts_ so that you guarantee that only requests made from these addresses will be accepted, **otherwise anyone with access to the API token will have unrestricted access to the firewall.**

Click OK and you will be prompted to store the generated API key in a secure location. Keep in mind that this key will not be shown again so if you lose it, you will have to generate another one.

<img src="https://github.com/mcarneir0/fortigate-backup-api/blob/assets/04-api-key.png" alt= "API key" title="API key">

### 4. Grant _super_admin_ permissions to the user

That's why we created that temporary profile earlier, Fortigate doesn't allow creating _super_admin_ _REST API_ users directly. But this permission is needed to backup other _super_admin_ users you may have on the firewall.

To do this, you need to run the following commands in the _CLI Console_, click on the option in the upper right corner to open it.

```bash
# config system api-user
(api-user) # edit <username>
(<username>) # set accprofile super_admin
(<username>) # set vdom root
(<username>) # next
(api-user) # end 
```
<img src="https://github.com/mcarneir0/fortigate-backup-api/blob/assets/05-cli-console-option.png" alt= "CLI option" title="CLI option" align="right">

<img src="https://github.com/mcarneir0/fortigate-backup-api/blob/assets/06-cli-console.png" alt= "CLI commands" title="CLI commands">

Now close the CLI, delete the temporary user profile and you're good to go.

## Environment

Tested with:

- Windows 11
- Ubuntu 22.04.2 LTS
- CentOS 7
- Python 3.11.2 / 3.11.1 / 3.10.9 / 3.10.6 / 3.6.8
- FortiOS 6.0.x / 6.2.x / 7.0.x / 7.2.x

## References

 - [FortiGate REST API Token Authentication](https://www.insoftservices.uk/fortigate-rest-api-token-authentication/)
 - [Technical Tip: Get backup config file on FortiGate using RestAPI via Python script](https://community.fortinet.com/t5/FortiGate/Technical-Tip-Get-backup-config-file-on-FortiGate-using-RestAPI/ta-p/202286)

## License

This project is licensed under the GPL-2.0 License - see the [LICENSE](https://github.com/mcarneir0/fortigate-backup-api/blob/main/LICENSE) file for details.
