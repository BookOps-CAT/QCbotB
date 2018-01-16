from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, ForeignKey, Integer, String, Boolean,
                        create_engine)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from contextlib import contextmanager
import logging


module_logger = logging.getLogger('QCBtests')

Base = declarative_base()
conn_string = 'sqlite:///datastore.db'


class Bibs(Base):
    __tablename__ = 'bibs'
    id = Column(Integer, primary_key=True, autoincrement=False)
    b_date = Column(String)
    b_type = Column(String)
    title = Column(String, nullable=False)
    author = Column(String)
    b_lang = Column(String, nullable=False)
    b_format = Column(String, nullable=False)
    b_call = Column(String)
    c_format = Column(String, nullable=False)
    c_audn = Column(String, nullable=False)
    c_lang = Column(String, nullable=False)
    c_type = Column(String, nullable=False)
    c_cutter = Column(Boolean, nullable=False)
    c_dewey = Column(String)
    c_division = Column(String)
    subjects = Column(String)
    subject_person = Column(String)
    crit_work = Column(Boolean, nullable=False)

    orders = relationship('Orders', cascade='all, delete-orphan')

    def __repr__(self):
        return "<Bib(id='b%sa', b_date='%s', b_type='%s', title='%s', " \
            "author='%s, b_lang='%s', b_format='%s', b_call='%s', " \
            "c_format='%s', c_audn='%s', c_lang='%s', c_type='%s', " \
            "c_cutter'%s', c_dewey='%s', c_division='%s', subjects='%s', " \
            "subject_person='%s', crit_work='%s')>" % (
                self.id, self.b_date, self.b_type, self.title,
                self.author, self.b_lang, self.b_format,
                self.b_call, self.c_format, self.c_audn,
                self.c_lang, self.c_type, self.c_cutter,
                self.c_dewey, self.c_division, self.subjects,
                self.subject_person, self.crit_work)


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=False)
    b_id = Column(Integer, ForeignKey('bibs.id'), nullable=False)
    o_date = Column(String, nullable=False)
    o_branch = Column(String, nullable=False)
    o_shelf = Column(String)
    o_audn = Column(String)
    copies = Column(Integer, nullable=False)
    ven_note = Column(String)

    def __repr__(self):
        return "<Order(id='o%sa', b_id='b%sa', o_date='%s', " \
            "o_branch='%s', o_shelf='%s', o_audn='%s', copies='%s', " \
            "ven_note='%s')>" % (
                self.id, self.b_id, self.o_date, self.o_branch,
                self.o_shelf, self.o_audn, self.copies, self.ven_note)


class Conflicts(Base):
    __tablename__ = 'conflicts'
    id = Column(Integer, primary_key=True, autoincrement=False)
    level = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    desc = Column(String, nullable=False)

    def __repr__(self):
        return "<Conflicts(id='%s', level='%s', code='%s', desc='%s')>" % (
            self.id, self.level, self.code, self.desc)


class Tickets(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    timestamp = Column(String, nullable=False, default=datetime.now())
    servicenow_id = Column(Integer)
    b_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    o_id = Column(Integer)
    copies = Column(Integer, nullable=False)  # use last order as default

    def __repr__(self):
        return "<Tickets(id='%s', timestamp='%s', " \
            "servicenow_id='%s', b_id='%s', title='%s', o_id='%s')>" % (
                self.id, self.timestamp,
                self.servicenow_id, self.b_id, self.title, self.o_id)


class Tick_Conf_Joiner(Base):
    __tablename__ = 'tick_conf_joiner'
    t_id = Column(
        Integer, ForeignKey('tickets.id'), primary_key=True)
    c_id = Column(
        Integer, ForeignKey('conflicts.id'), primary_key=True)

    def __repr__(self):
        return "<Ticket-Conflict-Joiner(t_id='%s', c_id='%s')>" % (
            self.t_id, self.c_id)


class DataAccessLayer:

    def __init__(self):
        self.conn_string = conn_string
        self.engine = None
        self.session = None

    def connect(self):
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


dal = DataAccessLayer()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    dal.connect()
    session = dal.Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
