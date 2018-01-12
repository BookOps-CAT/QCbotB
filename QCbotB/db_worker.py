# methods to access and query datastore

from sqlalchemy.exc import IntegrityError
import logging


from datastore import dal


module_logger = logging.getLogger('QCBtests')


def update_table(model, **kwargs):
    if 'id' in kwargs:
        instance = dal.session.query(model).filter_by(id=kwargs['id']).first()
    else:
        # add as new
        instance = dal.session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        try:
            dal.session.add(instance)
            dal.session.commit()
        except IntegrityError:
            module_logger.error(
                'datastore IntegrityError: {} ; {}'.format(
                    model, kwargs))
    else:
        for key, value in kwargs.iteritems():
            setattr(instance, key, value)
            dal.session.commit()
    dal.session.close()


def insert_or_ignore(model, **kwargs):
    if 'id' in kwargs:
        instance = dal.session.query(model).filter_by(id=kwargs['id']).first()
    else:
        instance = dal.session.query(model).filter_by(**kwargs).first()
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
    # dal.connect()
    # dal.session = dal.Session()
    num_rows_deleted = dal.session.query(model).delete()
    dal.session.commit()
    dal.session.close()
    return num_rows_deleted


def run_query(sql_stmn):
    return dal.session.execute("{}".format(sql_stmn))
