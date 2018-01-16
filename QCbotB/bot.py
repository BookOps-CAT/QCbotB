import logging
import logging.config
import loggly.handlers

from logging_setup import LOGGING
from sierra_parser import report_data
from db_worker import (insert_or_ignore, delete_table_data, insert_or_update,
                       run_query)
from datastore import Bibs, Orders, Conflicts, Tickets, session_scope
from conflict_parser import conflict2dict

logging.config.dictConfig(LOGGING)
main_logger = logging.getLogger('QCBtests')


# ToDo: call ftp_worker to download Sierra report

fh = './files/sierra_test_list.txt'

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
# as above, if a problem encountered the whole session transactions
# will be rolled back
queries = dict()
try:
    with session_scope() as session:
        conflicts = conflict2dict()

        # update Conflict table in datastore
        for conflict in conflicts:
            queries[conflict['id']] = conflict['query']
            conflict.pop('query', None)
            insert_or_update(session, Conflicts, **conflict)
except Exception as e:
    main_logger.critical(
        'unable to add data to datastore: {}, error: {}'.format(
            conflict, e))

# run conflict queries and save errors in the datastore
# will not run if conflicts.xml have problems
try:
    with session_scope() as session:
        for id, query in queries.iteritems():
            results = run_query(session, query)
            for row in results:
                ticket = dict(
                    conflict_id=id,
                    b_id=row.id,
                    title=row.title,
                    copies=row.copies)
                insert_or_ignore(session, Tickets, **ticket)
except Exception as e:
    main_logger.critical(
        'Unable to add data to datastore: {}, error: {}'.format(
            ticket, e))

# # ToDo: report findings
# # call servicenow_worker

# # clean-up Bibs and Orders tables
# with session_scope() as session:
#     delete_table_data(session, Orders)
#     delete_table_data(session, Bibs)

# # ToDo: provide options to interact with bot
# # if __name__ == "__main__":
# #     # option -install sets up datastore
# #     # should check if datastore exist to run