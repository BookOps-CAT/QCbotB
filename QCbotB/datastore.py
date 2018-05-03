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
    b_call = Column(String)
    c_format = Column(String, nullable=False)
    c_audn = Column(String, nullable=False)
    c_wl = Column(Boolean, nullable=False)
    c_type = Column(String)
    c_cutter = Column(Boolean, nullable=False)
    c_dewey = Column(String)
    c_division = Column(String)
    subjects = Column(String)
    subject_person = Column(String)
    crit_work = Column(Boolean)

    orders = relationship('Orders', cascade='all, delete-orphan')

    def __repr__(self):
        return "<Bib(id='b%sa', b_date='%s', b_type='%s', title='%s', " \
            "author='%s, b_call='%s', " \
            "c_format='%s', c_audn='%s', c_wl='%s', c_type='%s', " \
            "c_cutter'%s', c_dewey='%s', c_division='%s', subjects='%s', " \
            "subject_person='%s', crit_work='%s')>" % (
                self.id, self.b_date, self.b_type, self.title,
                self.author, self.b_call, self.c_format, self.c_audn,
                self.c_wl, self.c_type, self.c_cutter,
                self.c_dewey, self.c_division, self.subjects,
                self.subject_person, self.crit_work)


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=False)
    bid = Column(Integer, ForeignKey('bibs.id'), nullable=False)
    o_date = Column(String, nullable=False)
    o_branch = Column(String, nullable=False)
    o_shelf = Column(String)
    o_audn = Column(String)
    copies = Column(Integer, nullable=False)
    ven_note = Column(String)

    def __repr__(self):
        return "<Order(id='o%sa', bid='b%sa', o_date='%s', " \
            "o_branch='%s', o_shelf='%s', o_audn='%s', copies='%s', " \
            "ven_note='%s')>" % (
                self.id, self.bid, self.o_date, self.o_branch,
                self.o_shelf, self.o_audn, self.copies, self.ven_note)


class Conflicts(Base):
    __tablename__ = 'conflicts'
    id = Column(Integer, primary_key=True, autoincrement=False)
    tier = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)

    def __repr__(self):
        return "<Conflicts(id='%s', level='%s', code='%s', desc='%s')>" % (
            self.id, self.tier, self.code, self.description)


class Tickets(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    timestamp = Column(String, nullable=False, default=datetime.now())
    servicenow_id = Column(Integer)
    bid = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    fixed = Column(Boolean, default=False)

    copies = relationship('Copies', cascade='all, delete-orphan')
    conflicts = relationship('TickConfJoiner', cascade='all, delete-orphan')

    def __repr__(self):
        return "<Tickets(id='%s', timestamp='%s', " \
            "servicenow_id='%s', bid='%s', title='%s')>" % (
                self.id, self.timestamp,
                self.servicenow_id, self.bid, self.title)


class TickConfJoiner(Base):
    __tablename__ = 'tick_conf_joiner'
    tid = Column(
        Integer, ForeignKey('tickets.id'), primary_key=True)
    cid = Column(
        Integer, ForeignKey('conflicts.id'), primary_key=True)

    def __repr__(self):
        return "<Ticket-Conflict-Joiner(tid='%s', cid='%s')>" % (
            self.tid, self.cid)


class Copies(Base):
    __tablename__ = 'copies'
    tid = Column(
        Integer, ForeignKey('tickets.id'), primary_key=True)
    oid = Column(
        Integer, primary_key=True, autoincrement=False)
    copies = Column(Integer, default=0)

    def __repr__(self):
        return "<Copies(tid='%s', oid='%s', copies='%s')>" % (
            self.t_id, self.o_id, self.copies)


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
