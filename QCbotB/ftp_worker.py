# responsible for fetching and managing ftp files
from ftplib import FTP, error_reply
from datetime import datetime
import logging


# TODO:
# - move downloaded file to archive
# - delete reports older than 30 days from archive

module_logger = logging.getLogger('QCBtests')


def find_todays_file(dir_list=None):
    """
    identifies filename of most recent Sierra report
    """
    fhdate = datetime.strftime(datetime.now(), '%Y%m%d')
    if dir_list is not None:
        # grab the latest file with date
        for fh in sorted(dir_list, reverse=True):
            if 'BookOpsQC.{}'.format(fhdate) in fh:
                    return fh
    return None


def ftp_download(host, user, passw, folder):
    fetched = False
    try:
        module_logger.info('ftp_worker: Connecting to FTP...')
        ftp = FTP(host)     # connect to host, default port
        res = ftp.login(user, passw)
        if res[:3] == '230':  # '230 Login successful.'
            module_logger.info('fpt_worker: Succesfully connected to FTP...')
            ftp.cwd(folder)  # change to desired directory
            files = ftp.nlst()  # retrieve all files in the folder
            todays_file = find_todays_file(files)
            if todays_file is None:
                module_logger.warning(
                    'ftp_worker: not able to find sierra report')
            else:
                module_logger.info(
                    'ftp_worker: Identified todays sierra report')
                ftp.retrbinary(
                    'RETR {}'.format(todays_file),
                    open('./files/report.txt', 'wb').write)
                fetched = True
                module_logger.info(
                    'fpt_worker: Downloaded todays sierra report')
        else:
            module_logger.error(
                'ftp_worker: Unsucessful login to FTP server, '
                'FTP response: {}'.format(res))
    except error_reply:
        module_logger.error(
            'ftp_worker: Encountered following error: {}'.format(
                error_reply))
    finally:
        try:
            ftp.close()
            module_logger.info(
                'ftp_worker: FTP connection closed succesfully.')
        except error_reply:
            ftp.quit()
        return fetched


if __name__ == '__main__':
    import shelve

    s = shelve.open('settings')
    ftp_download(s['ftp_host'], s['ftp_user'], s['ftp_pass'], 'bpl')
    s.close()
    # print todays_file(['BookOpsQC.20180122104500', 'BookOpsQC.20180122100000'])
