import shelve
import logging
import logging.config
import loggly.handlers

from logging_setup import LOGGING
from sierra_parser import report_data
from db_worker import (insert_or_ignore, delete_table_data,
                       insert_or_update,
                       run_query)
from datastore import (Bibs, Orders, Conflicts, Tickets,
                       TickConfJoiner, session_scope)
from conflict_parser import conflict2dict
from ftp_worker import ftp_download, ftp_maintenance


def analize(report_fh=None):

    # # clean-up Bibs and Orders tables to prep
    # datastore for new set
    with session_scope() as session:
        delete_table_data(session, Orders)
        delete_table_data(session, Bibs)

    fetched = False
    if report_fh is None:
        s = shelve.open('settings', flag='r')
        host = s['ftp_host']
        user = s['ftp_user']
        passw = s['ftp_pass']
        ret = s['orders_retention']
        # fetch the latests Sierra report
        fetched = ftp_download(host, user, passw, 'bpl')
        s.close()
        if fetched:
            data_generator = report_data('./files/report.txt', ret)
        else:
            main_logger.warning(
                'No new sierra report - skippig analysis')
        # perform ftp maintenance
        ftp_maintenance(host, user, passw, 'bpl')
    else:
        s = shelve.open('settings', flag='r')
        ret = s['orders_retention']
        data_generator = report_data(report_fh, ret)
        fetched = True

    if fetched:
        # since bibs and orders are somewhat vetted by the sierra_parser
        # it's OK to add them in bulk to datastore
        # if any exception encountered the whole batch will be rolled back!
        try:
            with session_scope() as session:
                for record in data_generator:
                    bib = record[0]
                    order = record[1]
                    insert_or_ignore(session, Bibs, **bib)
                    insert_or_ignore(session, Orders, **order)
        except Exception as e:
            main_logger.critical(
                'Unable to add data {} to datastore. '
                'Error: {}'.format(file, e))

        # update conflicts table and prepare queries
        # this time enter each conflict in it's own session
        # so well formed queries can be used
        queries = dict()
        conflicts = conflict2dict()

        # update Conflict table in datastore
        for conflict in conflicts:
            queries[conflict['id']] = conflict['query']
            conflict.pop('query', None)
            try:
                with session_scope() as session:
                    insert_or_update(session, Conflicts, **conflict)
            except Exception as e:
                main_logger.critical(
                    'unable to add data to datastore: {}, error: {}'.format(
                        conflict, e))

        # run conflict queries and save errors in the datastore
        for cid, query in queries.iteritems():
            try:
                with session_scope() as session:
                    results = run_query(session, query)
                    for row in results:
                        tic = dict(
                            bid=row.bid,
                            title=row.title)
                        ticket = insert_or_ignore(session, Tickets, **tic)
                        # flush session so ticket obj gets id needed for joiner
                        session.flush()
                        joiner = dict(
                            tid=ticket.id,
                            cid=cid)
                        insert_or_ignore(session, TickConfJoiner, **joiner)

            except Exception as e:
                # think about better logging here
                main_logger.critical(
                    'Unable to add data to datastore, error: {}, {}: {}'.format(
                        e, row, cid))

        # # ToDo: report findings
    # # call servicenow_worker


def analize_in_test_mode(file):
    """
    attempts to parse a report (file) and load its data
    to datastore, and outputs errors to console
    """
    pass


def view_conflicts(start_date, end_date):
    """Creates a report on conflicts found between given dates"""
    pass


def release_and_issue_tickets(date):
    """
    finds unreported to ServiceNow conflicts discovered
    on given date and issues tickets
    """
    pass


def validate_dates(dates):
    """
    takes a list of date strings and
    returns list of date objects
    """
    dobj = []
    for d in dates:
        try:
            dobj.append(datetime.strptime(d, '%d-%m-%y'))
        except ValueError:
            raise
    return dobj


def set_settings(**kwargs):
    """Sets FTP and orders retention parameters"""
    try:
        s = shelve.open('settings')
        if 'ftp' in kwargs:
            s['ftp_host'] = kwargs['ftp'][0]
            s['ftp_user'] = kwargs['ftp'][1]
            s['ftp_pass'] = kwargs['ftp'][2]
        if 'orders_retention' in kwargs:
            s['orders_retention'] = kwargs['orders_retention']
    finally:
        s.close()


def get_settings():
    """Returns current FTP and orders retention settings"""
    try:
        s = shelve.open('settings', flag='r')
        v = dict(s)
        return v
    finally:
        s.close()


if __name__ == "__main__":
    import argparse
    from datetime import datetime

    logging.config.dictConfig(LOGGING)
    main_logger = logging.getLogger('QCBtests')
    today = datetime.strftime(datetime.now(), '%d-%m-%y')

    # verify settings are present and if not add generic ones
    s = shelve.open('settings')
    if 'ftp_host' not in s:
        s['ftp_host'] = None
    if 'ftp_user' not in s:
        s['fpt_user'] = None
    if 'ftp_pass' in s:
        s['ftp_pass'] = None
    if 'orders_retention' not in s:
        s['orders_retention'] = 180
    s.close()

    parser = argparse.ArgumentParser(description='QCBot-B Help')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--ftp',
        help='FTP authentication settings, format: --ftp [IP USER PASSWORD]',
        nargs=3,
        type=str)
    group.add_argument(
        '--ingest',
        help='process given in path sierra report',
        nargs=1,
        metavar='FILE',
        type=str)
    group.add_argument(
        '--release',
        nargs=1,
        metavar='DD-MM-YY',
        help='release unreported conflicts discovered on specified'
             ' date and issue SerivceNow tickets, '
             'use format dd-mm-yy')
    group.add_argument(
        '--retention',
        nargs=1,
        help='sets age of orders in days (integer) '
             'to be considered for QC analysis',
        type=int)
    group.add_argument(
        '--view_settings',
        action='store_true',
        help='display current settings (ftp, etc.)')
    group.add_argument(
        '--test',
        help='test processing given in path Sierra report',
        nargs=1,
        metavar='FILE',
        type=str)
    group.add_argument(
        '--version',
        help="display bot's version",
        action='version',
        version='v.0.0.1')  # auto pull from version?
    group.add_argument(
        '--view',
        help='view conflicts found on particular date, used dd-mm-yy',
        nargs='*',
        metavar='DD-MM-YY DD-MM-YY')
    args = parser.parse_args()
    if args.ftp is not None:
        set_settings(ftp=args.ftp)
        print 'FTP settings saved...'
    elif args.ingest is not None:
        print 'ingesting & analyzing file: {}'.format(args.ingest[0])
        analize(args.ingest[0])
    elif args.test is not None:
        print 'testing ingesting & analyzing file: {}'.format(
            args.test[0])
        analize_in_test_mode(args.test[0])
    elif args.view is not None:
        if len(args.view) == 0:
            view_conflicts(today, today)
        elif len(args.view) == 1:
            dates = validate_dates(args.view)
            view_conflicts(dates[0], today)
        elif len(args.view) == 2:
            dates = validate_dates(args.view)
            view_conflicts(dates[0], dates[1])
        else:
            parser.error(
                '--view option accepts no values (date range today-today),'
                ' one value (range start date-today), or'
                'two values (start date-end date)')
    elif args.release is not None:
        release_and_issue_tickets(args.release[0])
    elif args.view_settings:
        s = get_settings()
        for key, value in sorted(s.iteritems()):
            print '{}={}'.format(key, value)
    elif args.retention is not None:
        set_settings(orders_retention=args.retention)
        print 'Done. Analysis will consider only order no ' \
            'older than {} days'.format(args.retention)

    else:
        # while testing provide report test file
        # fh = './files/report.txt'
        analize()
