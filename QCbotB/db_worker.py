# methods to access and query datastore

from sqlalchemy.exc import IntegrityError
import logging


from datastore import dal


module_logger = logging.getLogger('QCBtests')


def insert_or_ignore(model, **kwargs):
    dal.connect()
    dal.session = dal.Session()
    instance = dal.session.query(model).filter_by(id=kwargs['id']).first()
    if not instance:
        instance = model(**kwargs)
        try:
            dal.session.add(instance)
            dal.session.commit()
        except IntegrityError:
            # record table name and record that failed
            module_logger.error(
                'datastore IntegrityError: {} ; {}'.format(
                    model, kwargs))
    dal.session.close()


def delete_table_data(model):
    dal.connect()
    dal.session = dal.Session()
    num_rows_deleted = dal.session.query(model).delete()
    dal.session.commit()
    dal.session.close()
    return num_rows_deleted
