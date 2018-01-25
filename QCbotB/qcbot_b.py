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


def analize(fh=None):

    if fh is None:
        # ToDo: call ftp_worker to download Sierra report
        pass

    # pass report to sierra_parser
    data_generator = report_data(fh)

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
            'Unable to add data {} to datastore. Error: {}'.format(file, e))


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

    # # clean-up Bibs and Orders tables
    # with session_scope() as session:
    #     delete_table_data(session, Orders)
    #     delete_table_data(session, Bibs)

# ToDo: provide options to interact with bot


def analize_in_test_mode(file):
    """
    attempts to parse a report (file) and load its data
    to datastore, and outputs errors to console
    """
    pass


def view_conflicts(start_date, end_date):
    """
    creates a report on conflicts found between given dates
    """
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


def settings(**kwargs):
    s = shelve.open('settings')
    if kwargs['ftp']:
        s['ftp_host'] = kwargs['ftp'][0]
        s['ftp_user'] = kwargs['ftp'][1]
        s['ftp_pass'] = kwargs['ftp'][2]

    s.close()

if __name__ == "__main__":
    import argparse
    from datetime import datetime

    logging.config.dictConfig(LOGGING)
    main_logger = logging.getLogger('QCBtests')
    today = datetime.strftime(datetime.now(), '%d-%m-%y')

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
        settings(ftp=args.ftp)
        print 'FTP settings saved...'
    elif args.ingest is not None:
        print args.ingest[0]
        # analize(args.ingest[0])
    elif args.test is not None:
        analize_in_test_mode(args.ingest[0])
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
    else:
        # while testing provide report test file
        fh = './files/sierra_test_list2.txt'
        analize(fh)
