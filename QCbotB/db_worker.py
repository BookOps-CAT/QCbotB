# methods to access and query datastore

from sqlalchemy.exc import IntegrityError
import logging


from datastore import dal


module_logger = logging.getLogger('QCBtests')


def update_table(model, **kwargs):
    """
    updates data in specified table

    parameters
    ----------
    model : class
        name of table
    kwargs : dict
        values to be added or updated

    """
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
    """
    adds data to specified table
    if data is found to exist in the table nothing is added

    parameters
    ----------
    model : class
        name of table
    kwargs: dict
        values to be entered to the table
    """
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
    """
    deletes data from specified datastore table

    returns
    -------
    int
        number of deleted rows
    """
    num_rows_deleted = dal.session.query(model).delete()
    dal.session.commit()
    dal.session.close()
    return num_rows_deleted


def run_query(sql_stmn=None):
    """
    runs conflict SQL statement on datastore

    returns
    -------
    list
        list of datastore query results
    """
    if sql_stmn is None:
        return []
    else:
        return dal.session.execute("{}".format(sql_stmn))
