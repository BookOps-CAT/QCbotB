# responsible for fetching and managing ftp files
from ftplib import FTP, error_reply, error_perm
from datetime import datetime, timedelta
import logging


from setup_dirs import DATA


# ToDo: tests for find_todays_file and aged_out_report

module_logger = logging.getLogger('qcbot_log.ftp_worker')


def find_todays_file(dir_list=None):
    """Identifies filename of most recent Sierra report"""
    fhdate = datetime.strftime(datetime.now(), '%Y%m%d')
    if dir_list is not None:
        # grab the latest file with date
        for fh in sorted(dir_list, reverse=True):
            if 'BookOpsQC.{}'.format(fhdate) in fh:
                    return fh
    return None


def aged_out_report(fh):
    try:
        fh_date = fh[10:]
        todays_date = datetime.now()
        fh_date = datetime.strptime(fh_date, '%Y%m%d%H%M%S')
        age = todays_date - fh_date
        num_days = timedelta(days=30)
        if age > num_days:
            return True
        else:
            return False
    except IndexError:
        module_logger.warning(
            'ftp_worker: Found unsupported report '
            'filename type in archive: {}'.format(
                fh))
        return False
    except ValueError:
        module_logger.warning(
            'ftp_worker: Found unsupported report '
            'filename type in archive: {}'.format(
                fh))
        return False


def ftp_maintenance(host, user, passw, folder):
    """Performs maintenace of FTP storage"""
    module_logger.info('ftp:worker: Connecting to FTP...')
    try:
        ftp = FTP(host)
        conn = ftp.login(user, passw)
        if conn[:3] == '230':
            module_logger.info('ftp_worker: Succesfully connected to FTP...')

            # archive previous reports
            ftp.cwd(folder)  # change to desired directory
            files = ftp.nlst()  # retrieve all files in the folder
            todays_file = find_todays_file(files)
            if todays_file is not None:
                files.remove(todays_file)
            try:
                module_logger.info(
                    'ftp_worker: Begining moving old files to archive...')
                for file in files:
                    dst_file = './archive/{}'.format(file)
                    ftp.rename(file, dst_file)
                module_logger.info(
                    'ftp_worker: Succcessfully moved {} '
                    'file(s) to archive'.format(
                        len(files)))
            except error_reply:
                module_logger.error(
                    'ftp_worker: Encountered following error: {}'.format(
                        error_reply))

            # delete older reports from archive
            ftp.cwd('./archive')
            files = ftp.nlst()
            deleted = 0
            for file in files:
                if aged_out_report(file):
                    deleted += 1
                    try:
                        ftp.delete(file)
                    except error_perm:
                        module_logger.error(
                            'ftp_worker: No permission to delete '
                            'file: {}'.format(
                                file))
                    except error_reply:
                        module_logger.error(
                            'ftp_worker: Encountered following '
                            'error: {}'.format(
                                error_reply))
            module_logger.info(
                'ftp_worker: Removed {} old files from the archive'.format(
                    deleted))

        else:
            module_logger.warning(
                'ftp_worker: Unsucessful login to FTP server, '
                'FTP response: {}'.format(conn))
    except error_reply:
        module_logger.error(
            'ftp_worker: Encountered following error: {}'.format(
                error_reply))
    finally:
        try:
            ftp.quit()
            module_logger.info(
                'ftp_worker: FTP connection closed succesfully.')
        except error_reply:
            ftp.close()


def ftp_download(host, user, passw, folder):
    fetched = False
    try:
        module_logger.info('ftp_worker: Connecting to FTP...')
        ftp = FTP(host)     # connect to host, default port
        conn = ftp.login(user, passw)
        if conn[:3] == '230':  # '230 Login successful.'
            module_logger.info('fpt_worker: Succesfully connected to FTP...')
            ftp.cwd(folder)  # change to desired directory
            files = ftp.nlst()  # retrieve all files in the folder
            todays_file = find_todays_file(files)
            if todays_file is None:
                module_logger.warning(
                    'ftp_worker: not able to find sierra report')
            else:
                module_logger.info(
                    'ftp_worker: Identified todays sierra '
                    'report as: {}'.format(
                        todays_file))
                ftp.retrbinary(
                    'RETR {}'.format(todays_file),
                    open(DATA, 'wb').write)
                fetched = True
                module_logger.info(
                    'fpt_worker: Downloaded todays sierra report')
        else:
            module_logger.error(
                'ftp_worker: Unsucessful login to FTP server, '
                'FTP response: {}'.format(conn))
    except error_reply:
        module_logger.error(
            'ftp_worker: Encountered following error: {}'.format(
                error_reply))
    finally:
        try:
            ftp.quit()
            module_logger.info(
                'ftp_worker: FTP connection closed succesfully.')
        except error_reply:
            ftp.close()
        return fetched
