import logging
import logging.config
import loggly.handlers

from logging_setup import LOGGING
from sierra_parser import report_data
from db_worker import insert_or_ignore, delete_table_data
import datastore as db
from datastore import dal

logging.config.dictConfig(LOGGING)
main_logger = logging.getLogger('QCBtests')

data_generator = report_data('./files/sierra_test_list.txt')

# connect to datastore and save records
dal.connect()
dal.session = dal.Session()
for record in data_generator:
    bib = record[0]
    order = record[1]
    # print bib
    # print order
    insert_or_ignore(db.Bibs, **bib)
    insert_or_ignore(db.Orders, **order)

print delete_table_data(db.Orders)
print delete_table_data(db.Bibs)

# if __name__ == "__main__":
#     # option -install sets up datastore
#     # should check if datastore exist to run