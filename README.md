# Email IP

Emails IP address of client.

This script is meant to be run on a Raspberry Pi in order to obtain its IP address via email on startup.

## Usage

Change the settings in the constants as marked:

```python
### CHANGE THE FOLLOWING SETTINGS ###
PI_NAME = 'raspberry pi'
RECIPIENT_EMAIL = 'pi@example.com'
SENDER_GMAIL = 'example@gmail.com'
SENDER_PASSWORD = 'example_password'
#####################################
```

Add this python script to run on startup.

e.g. If you're on raspbian, add the following lines to `/etc/rc.local`:

```bash
if [ "$(hostname -I)" ]; then
    python /path/to/email_ip.py
fi
```

---

## To Do

* write function to store and encrypt settings from command line
* write function to install script to /etc/rc.local
