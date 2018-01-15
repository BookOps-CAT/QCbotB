# methods to access and query datastore

import logging


module_logger = logging.getLogger('QCBtests')


def insert_or_update(session, model, **kwargs):
    """
    updates data in specified table

    parameters
    ----------
    model : class
        name of table
    kwargs : dict
        values to be added or updated

    returns
    -------
    Boolean
        True if operation successful, False on failed
    """

    if 'id' in kwargs:
        instance = session.query(model).filter_by(id=kwargs['id']).first()
    else:
        instance = session.query(model).filter_by(**kwargs).first()

    if not instance:
        instance = model(**kwargs)
        session.add(instance)
    else:
        for key, value in kwargs.iteritems():
            setattr(instance, key, value)
        session.add(instance)
    return instance.id


def insert_or_ignore(session, model, **kwargs):
    """
    adds data to specified table
    if data is found to exist in the table nothing is added

    parameters
    ----------
    session: obj
        sqlalchemy session
    model : class
        name of table
    kwargs: dict
        values to be entered to the table

    returns
    -------
    int
        returns id of added or already found record
    """

    if 'id' in kwargs:
        instance = session.query(model).filter_by(id=kwargs['id']).first()
    else:
        instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
    return instance


def delete_table_data(session, model):
    """
    deletes data from specified datastore table

    parameters
    ----------
    session : session
    model : datastore class

    returns
    -------
    int
        number of deleted rows
    """
    num_rows_deleted = session.query(model).delete()
    return num_rows_deleted


def run_query(session, sql_stmn=None):
    """
    runs conflict SQL statement on datastore

    parameters
    ----------
    session : session object
    sql_stmn : SQL statement to run

    returns
    -------
    list
        list of datastore query results
    """

    if sql_stmn is None:
        return []
    else:
        results = session.execute("{}".format(sql_stmn))
        return results
