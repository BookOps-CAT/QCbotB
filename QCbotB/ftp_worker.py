# responsible for fetching and managing ftp files

from ftplib import FTP, error_reply
from datetime import datetime


def todays_file(dir_list=None):
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
    try:
        ftp = FTP(host)     # connect to host, default port
        res = ftp.login(user, passw)
        if res[:3] == '230':  # '230 Login successful.'
            ftp.cwd(folder)  # change to desired directory
            files = []
            ftp.retrlines('NLST', files.append)
            report = todays_file(files)
            # print report
            ftp.retrbinary(
                'RETR {}'.format(report),
                open('./files/report.txt', 'wb').write)
        else:
            print 'ftp included respons other than 230: {}'.format(res)
    except error_reply:
        # log error
        print error_reply
    finally:
        try:
            ftp.close()
        except error_reply:
            ftp.quit()


if __name__ == '__main__':
    import shelve

    s = shelve.open('settings')
    ftp_download(s['ftp_host'], s['ftp_user'], s['ftp_pass'], 'bpl')
    s.close()
    # print todays_file(['BookOpsQC.20180122104500', 'BookOpsQC.20180122100000'])
