# # -*- coding: utf-8 -*-

# parser for exported data from Sierra list
#
# Sierra order list criteria:
# BIBLIOGRAPHIC  CAT DATE  equals yesterday      OR (ORDER  CREATED  equals yesterday      AND BIBLIOGRAPHIC  CALL #  not equal to  "")
#
# Export formatting:
# Field delimiter: ^
# Text qualifier: None
# Repeated field delimiter: ~
# Maximum field length: None

# Order of exported elements:
# RECORD #(BIBLIO)
# CAT DATE
# REC TYPE(BIBLIO)
# TITLE
# AUTHOR
# CALL
# SUBJECT
# RECORD #(ORDER)
# CREATED(ORDER)
# LOCATION
# COPIES
# VEN NOTE

import unicodecsv as csv
from datetime import datetime
import logging
import re
from unidecode import unidecode

from patterns import IDS, CFORMAT, CAUDN, \
    CLANG1, CLANG2, CTYPE, \
    CCUTTER, CDEW, OAUDN, OIAUDN, CRANGES, \
    SUBJECT_PERSON_FALSE, SUBJECT_PERSON, \
    CRITICAL_WORKS

module_logger = logging.getLogger('QCBtests')


def parse_dates(value=None):
    date = None
    if value != '  -  -  ':
        for f in ['%m-%d-%Y', '%m-%d-%y']:
            try:
                date = datetime.strptime(value, f)
                return date
            except ValueError:
                pass
            except TypeError:
                module_logger.error(
                    'TypeError on date: {}'.format(
                        type(value)))


def verify_bib_id(value=None):
    p1 = re.compile(IDS['p1'], flags=re.IGNORECASE)
    try:
        m = p1.match(value)
        if m:
            return int(m.group()[1:-1])
        else:
            module_logger.error(
                'Incorrect value of bib id, found value: {}'.format(
                    value))
    except TypeError:
        module_logger.error(
            'TypeError on bib id, found type: {}'.format(
                type(value)))


def verify_ord_id(value=None):
    p2 = re.compile(IDS['p2'], flags=re.IGNORECASE)
    try:
        m = p2.match(value)
        if m:
            return int(m.group()[1:-1])
        else:
            module_logger.error(
                'Incorrect value of order id in line, found value: {}'.format(
                    value))
    except TypeError:
        module_logger.error(
            'TypeError on ord id in line, found type {}'.format(
                type(value)))


def parse_subjects(value=None):
    value = value.split('~')
    subjects = []
    for s in value:
        if 'fast (OCoLC)' in s:
            continue
        else:
            subjects.append(s)

    subjects = '~'.join(subjects)
    return subjects


def verify_b_type(value=None):
    try:
        if value in 'acdefgijkmoprt' and value != '':
            return value
    except TypeError:
        module_logger.error('TypeError on rec type, found type: {}'.format(
            type(value)))


def parse_title(value=None):
    try:
        if '880-0' in value:
            value = value[7:]
        if value != '':
            return value.strip()
    except TypeError:
        module_logger.error('TypeError on parse_title, found type: {}'.format(
            type(value)))


def parse_name(value=None):
    try:
        if '880-' in value:
            value = value[7:].strip()
        if value.strip() != '':
            name = value.split(',')[0].strip()
            if name[-1] == '.':
                name = name[:-1]
            name = unidecode(name).upper()
            return name
    except TypeError:
        module_logger.error('TypeError on parse_name, found type: {}'.format(
            type(value)))


def parse_subject_person(value=None):
    # can have multiple 600s, consider only 1st
    p1 = re.compile(SUBJECT_PERSON_FALSE)
    m = p1.search(value)
    if not m:
        # not non-fiction
        # p2 = re.compile(SUBJECT_PERSON, re.UNICODE)
        for p in SUBJECT_PERSON:
            p2 = re.compile(p, re.UNICODE)
            m = p2.search(value)
            if m:
                return m.group(1)


def idenfity_critical_work(value=None):
    # find out if possible to extract from subject strings
    found = False
    for p in CRITICAL_WORKS:
        p = re.compile(p)
        m = p.search(value)
        if m:
            found = True
            break
    return found


def parse_branches(value=None):
    try:
        branches = value.split(',')
        branches = ','.join(
            sorted([x[0:2] for x in branches if x[0] in '0123456789']))
        return branches
    except IndexError:
        module_logger.error(
            'IndexError on parse_branches, found data: {}'.format(
                value))
    except TypeError:
        module_logger.error(
            'TypeError on parse_branches, found data: {}'.format(
                type(value)))


def parse_shelves(value=None):
    unique_shelves = set()
    try:
        shelves = value.split(',')
        shelves = [
            l[:l.index('(')].strip() if '(' in l else l.strip() for l in shelves]
        for l in shelves:
            if len(l) == 5:
                unique_shelves.add(l[-3:])
            else:
                continue
    except TypeError:
        module_logger.error(
            'TypeError on parse_shelves, found data: {}'.format(
                type(value)))
        return None
    except IndexError:
        module_logger.error(
            'IndexError on parse_shelves, found data: {}'.format(
                type(value)))
        return None
    finally:
        if len(unique_shelves) > 0:
            return ','.join(sorted(unique_shelves))


def parse_call_format(value=None):
    try:
        found = False
        for pattern in CFORMAT:
            p = re.compile(pattern[0])
            m = p.match(value)
            if m:
                found = True
                c_format = pattern[1]
                break
        if not found:
            c_format = 'pr'
        return c_format
    except TypeError:
        module_logger.error(
            'TypeError on parse_call_format found type: {}'.format(
                type(value)))


def parse_call_audn(value=None):
    try:
        found = False
        for pattern in CAUDN:
            p = re.compile(pattern[0])
            m = p.search(value)
            if m:
                found = True
                c_audn = pattern[1]
                break
        if not found:
            c_audn = 'a'
        return c_audn
    except TypeError:
        module_logger.error(
            'TypeError on parse_call_audn, found type: {}'.format(
                type(value)))


def world_lang_prefix(value=None):
    found = False
    try:
        if value[:3] in 'DVD,KIT,LIB,BOO':
            patterns = CLANG1
        else:
            patterns = CLANG2
        for pattern in patterns:
            p = re.compile(pattern)
            m = p.search(value)
            if m:
                found = True
                break
        return found
    except IndexError:
        module_logger.error(
            'IndexError on world_lang_perfix, found value: {}'.format(
                value))
        return found
    except TypeError:
        module_logger.error(
            'TypeError on world_lang_perfix, found type: {}'.format(
                type(value)))
        return found


def parse_call_type(value=None):
    try:
        found = False
        for pattern in CTYPE:
            p = re.compile(pattern[0])
            m = p.search(value)
            if m:
                found = True
                c_type = pattern[1]
                break
        if not found:
            c_type = None
            module_logger.error(
                'Unidentified call number type: {}'.format(
                    value))
        return c_type
    except TypeError:
        module_logger.error(
            'TypeError on parse_call_cutter, found type: {}'.format(
                type(value)))


def parse_call_cutter(value=None):
    try:
        found = False
        p = re.compile(CCUTTER)
        m = p.search(value)
        if m:
            found = True
        return found
    except TypeError:
        module_logger.error(
            'TypeError on parse_call_cutter, found type: {}'.format(
                type(value)))


def parse_call_dewey(value=None):
    try:
        p = re.compile(CDEW)
        m = p.search(value)
        if m:
            c_dew = m.group().strip()
        else:
            c_dew = None
        return c_dew
    except TypeError:
        module_logger.error(
            'TypeError on parse_call_dewey, found type: {}'.format(
                type(value)))


def identify_dewey_range(value=None):
    found = None
    try:
        if value is not None:
            r = int(value[0:3])
            for key, value in CRANGES.iteritems():
                if r in value:
                    found = key
                    break
    except TypeError:
        module_logger.error(
            'TypeError on identify_dewey_range, found type: {}'.format(
                type(value)))
    except IndexError:
        module_logger.error(
            'IndexError on identify_dewey_range, found value: {}'.format(
                value))
    finally:
        return found


def parse_ord_audn(value=None):
    try:
        codes = set()
        if value != '':
            shelves = value.split(',')
            for s in shelves:
                if s in OIAUDN:
                    codes.add(OIAUDN[s])
                elif s[0] in OAUDN:
                    codes.add(s[0])
                else:
                    codes.add('z')
    except TypeError:
        module_logger.error(
            'TypeError on parser_ord_audn, found type: {}'.format(
                type(value)))
    except IndexError:
        module_logger.error(
            'IndexError on parser_ord_audn, found value: {}'.format(
                value))
    except AttributeError:
        pass
    finally:
        if len(codes) > 0:
            return ','.join(sorted(codes))


def parse_o_shelf(value=None):
    try:
        codes = set()
        if value != '':
            shelves = value.split(',')
            for s in shelves:
                codes.add(s[1:])
    except TypeError:
        module_logger.error(
            'TypeError on parse_o_shelf, found type: {}'.format(
                type(value)))
    except IndexError:
        module_logger.error(
            'IndexError on parse_o_shelf, found value: {}'.format(
                value))
    except AttributeError:
        pass
    finally:
        if len(codes) > 0:
            return','.join(sorted(codes))


def report_data(fh, order_age_in_days):
    with open(fh, 'r') as file:
        reader = csv.reader(
            file, encoding='utf-8',
            delimiter='^', quoting=csv.QUOTE_NONE)
        reader.next()  # skip header
        # print list(enumerate(reader.next()))  # skip header

        for row in reader:
            try:
                bid = verify_bib_id(row[0])
                b_date = parse_dates(row[1])
                o_date = parse_dates(row[8])
                oid = verify_ord_id(row[7])

                # skip rows with incomplete data
                if bid is None or b_date is None or oid is None or \
                        o_date is None:
                    continue

                # omit rows with orders older number of days set in settings
                age = datetime.now() - o_date
                if age.days > order_age_in_days:
                    continue

                # ingore cancelled orders
                if row[12] == 'z':
                    continue

                b_type = None
                b_call = row[5].strip()
                c_dewey = parse_call_dewey(b_call)
                subjects = parse_subjects(row[6])

                yield (
                    dict(
                        id=bid,
                        b_date=b_date,
                        b_type=b_type,
                        title=parse_title(row[3]),
                        author=parse_name(row[4]),
                        b_call=b_call,
                        c_format=parse_call_format(b_call),
                        c_audn=parse_call_audn(b_call),
                        c_wl=world_lang_prefix(b_call),
                        c_type=parse_call_type(b_call),
                        c_cutter=parse_call_cutter(b_call),
                        c_dewey=c_dewey,
                        c_division=identify_dewey_range(c_dewey),
                        subjects=subjects,
                        subject_person=parse_subject_person(subjects),
                        crit_work=idenfity_critical_work(subjects)),
                    dict(
                        id=oid,
                        bid=bid,
                        o_date=o_date,
                        o_branch=parse_branches(row[9]),
                        o_shelf=parse_o_shelf(parse_shelves(row[9])),
                        o_audn=parse_ord_audn(parse_shelves(row[9])),
                        copies=0 if row[10] == '' else int(row[10]),
                        ven_note=None if row[11].strip() == '' else row[11].strip()))  # see if more detailed parsing for vendor notes is needed

            except IndexError:
                module_logger.error(
                    'IndexError at report_data, '
                    'enumerated value: {}'.format(
                        list(enumerate(row))))
                continue


if __name__ == '__main__':
    import logging.config
    import loggly.handlers

    from logging_setup import LOGGING

    logging.config.dictConfig(LOGGING)

    test_fh = './files/report_test1.txt'
    data = report_data(test_fh, 900)
    for x in data:
        try:
            if x[0]['crit_work'] is not None:
                print(x[0]['crit_work'], x[0]['subjects'])
            # print(x[1])
        except:
            pass

