from os.path import join, expanduser


# HOME = 'C:\\QCbots\\QCbot-B'
HOME = '.'  # use for development
LOG = join(HOME, 'log\\qcbotb.log')
CONFLICTS = join(HOME, 'files\\conflicts.xml')
DATA = join(HOME, 'files\\report.txt')
CRED_DIR = join(expanduser('~'), '.google')
CRED = join(CRED_DIR, 'credentials.json')
SECR = join(CRED_DIR, 'client_secret.json')
ADDR = join(CRED_DIR, 'gmail_contacts.json')
LOCAL = join(expanduser('~'), 'AppData\\Local\\QCbot-B')
SETTINGS = join(LOCAL, 'settings')
DATASTORE = join(LOCAL, 'datastore.db')
