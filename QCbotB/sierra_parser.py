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

from patterns import IDS, CFORMAT, CAUDN, CLANG, CTYPE,\
    CCUTTER, CDEW, OAUDN, OIAUDN, CRANGES

module_logger = logging.getLogger('QCBtests')

p1 = re.compile(IDS['p1'], flags=re.IGNORECASE)
p2 = re.compile(IDS['p2'], flags=re.IGNORECASE)


def parse_dates(data, counter):
    date = None
    for f in ['%m-%d-%Y', '%m-%d-%y']:
        try:
            date = datetime.strptime(data, f)
            return date
        except ValueError:
            pass
    if date is None and data != '  -  -  ':
        module_logger.error(
            'ValueError on date in line {}, found data: {}'.format(
                counter, data))


def verify_bib_id(data, counter=None):
    try:
        m = p1.match(data)
        if m:
            return int(m.group()[1:-1])
        else:
            module_logger.error(
                'Incorrect bib id in line {}, found data: {}'.format(
                    counter, data))
            return None
    except TypeError:
        module_logger.error(
            'TypeError on bib id in line {}, found data: {}'.format(
                counter, data))
        return None


def verify_ord_id(data, counter=None):
    try:
        m = p2.match(data)
        if m:
            return int(m.group()[1:-1])
        else:
            module_logger.error(
                'Incorrect order id in line {}, found data: {}'.format(
                    counter, data))
            return None
    except TypeError:
        module_logger.error(
            'TypeError on ord id in line {}, found data {}'.format(
                counter, data))
        return None


def parse_subjects(data, counter=None):
    data = data.split('~')
    subjects = []
    for s in data:
        if 'fast (OCoLC)' in s:
            continue
        else:
            subjects.append(s)

    subjects = '~'.join(subjects)
    return subjects


def find_bib_format(rec_type, t008, subjects, counter=None):
    try:
        if rec_type in 'acdeijmoprt':
            form = t008[23]
        elif rec_type in 'efgk':
            form = t008[29]
        else:
            module_logger.error(
                'Incorrect item form in 008'
                'field in line {}, found data: {}'.format(
                    counter, t008))
            return None
    except IndexError:
        module_logger.error(
            'IndexError; incorrect 008 length in line {}, '
            'found data: {}'.format(
                counter, t008))
        return None

    if rec_type in 'aeft':  # print and cartographic
        if form in ' dfr':
            if 'librettos' in subjects:
                b_format = 'lib'
            else:  # rest print
                b_format = 'print'
        elif form in 'abc':  # micro formats
            b_format = 'micro'
        elif form in 'soq':
            b_format = 'eres'  # eBook
        else:
            b_format = None
    elif rec_type in 'cd':  # scores
        b_format = 'score'
    elif rec_type == 'i':  # audio book
        if form == ' ':
            b_format = 'audio'
        elif form in 'soq':  # eAudio book
            b_format = 'eres'
        else:
            b_format = None
    elif rec_type == 'j':  # music cd
        if form == ' ':
            b_format = 'cd'
        elif form in 'soq':
            b_format = 'eres'  # eMusic
        else:
            b_format = None
    elif rec_type == 'g':  # dvd
        if form == ' ':
            b_format = 'dvd'
        elif form in 'soq':  # eVideo
            b_format = 'eres'
        else:
            b_format = None
    elif rec_type in 'op':  # kit
        b_format = 'kit'
    elif rec_type == 'k':  # photo
        b_format = 'photo'
    elif rec_type == 'm':  # comp eres
        b_format = 'eres'
    elif rec_type == 'r':  # mifi
        b_format = '3dobj'
    else:
        b_format = None

    return b_format


def find_main_language(t008, t041, counter=None):
    langs = set()
    try:
        langs.add(t008[35:38])
    except IndexError:
        module_logger.error(
            'IndexError: incorrect '
            '008 length in line {}, found data: {}'.format(
                counter, t008))
        return None
    try:
        if len(t041.strip()) != 0:
            langs = sorted(langs.union(set(t041.split('~'))))
    except TypeError:
        module_logger.error(
            'TypeError: incorrect type in 041, found data: {}'.format(
                t041))
        return None
    return '~'.join(langs)


def parse_title(data):
    if '880-0' in data:
        data = data[7:]
    return data


def parse_name(data, counter=None):
    if '880-' in data:
        data = data[7:].strip()
    if data != '':
        author = data.split(',')[0].strip()
        if author[-1] == '.':
            author = author[:-1]
        author = unidecode(author).upper()
        return author
    else:
        return None


def parse_subject_person(data, counter=None):
    # can have multiple 600s, consider only 1st
    if data != '':
        data = data.split('~')
        name = data[0]
        if '(Fictitious' in name:
            return None
        else:
            name = parse_name(data[0], counter)
            return name
    else:
        return None


def idenfity_critical_work(subject_person, t600t, counter=None):
    if t600t != '':
        return True
    else:
        if 'Criticism' in subject_person:
            return True
        else:
            return False


def parse_branches(locations, counter=None):
    locs = locations.split(',')
    try:
        locs = ','.join(sorted([x[0:2] for x in locs if x[0] in '0123456789']))
        return locs
    except IndexError:
        module_logger.error(
            'IndexError in line {}, found data: {}'.format(
                counter, locations))
        return None


def parse_shelves(locations, counter=None):
    shelves = set()
    locations = locations.split(',')
    locations = [
        l[:l.index('(')].strip() if '(' in l else l.strip() for l in locations]
    for l in locations:
        if len(l) == 5:
            shelves.add(l[-3:])  # this may backfire
        else:
            continue
    return ','.join(sorted(shelves))


def parse_call_format(callno):
    found = False
    for pattern in CFORMAT:
        p = re.compile(pattern[0])
        m = p.match(callno)
        if m:
            found = True
            c_format = pattern[1]
            break
    if not found:
        c_format = 'pr'
    return c_format


def parse_call_audn(callno):
    found = False
    for pattern in CAUDN:
        p = re.compile(pattern[0])
        m = p.search(callno)
        if m:
            found = True
            c_audn = pattern[1]
            break
    if not found:
        c_audn = 'a'
    return c_audn


def parse_call_lang(callno):
    found = False
    for pattern in CLANG:
        p = re.compile(pattern)
        m = p.search(callno)
        if m:
            found = True
            c_lang = m.group(1)
            break
    if not found:
        c_lang = 'eng'

    return c_lang.lower()


def parse_call_type(callno):
    found = False
    for pattern in CTYPE:
        p = re.compile(pattern[0])
        m = p.search(callno)
        if m:
            found = True
            c_type = pattern[1]
            break
    if not found:
        c_type = None
        module_logger.error(
            'Unidentified call number type: {}'.format(
                callno))
    return c_type


def parse_call_cutter(callno):
    found = False
    p = re.compile(CCUTTER)
    m = p.search(callno)
    if m:
        found = True
    return found


def parse_call_dewey(callno):
    p = re.compile(CDEW)
    m = p.search(callno)
    if m:
        c_dew = m.group().strip()
        # print c_dew
    else:
        c_dew = None
    return c_dew


def identify_dewey_range(dewey):
    found = None
    if dewey is not None:
        r = int(dewey[0:3])
        for key, value in CRANGES.iteritems():
            if r in value:
                found = key
                break
    return found


def parse_ord_audn(shelves_str):
    codes = []
    if shelves_str != '':
        shelves = shelves_str.split(',')
        for s in shelves:
            if s in OIAUDN:
                codes.append(OIAUDN[s])
            elif s[0] in OAUDN:
                codes.append(OAUDN[s[0]])
            else:
                codes.append('z')
    if len(codes) == 0:
        return None
    else:
        return ','.join(sorted(codes))


def parse_o_shelf(shelves_str):
    codes = []
    if shelves_str != '':
        shelves = shelves_str.split(',')
        for s in shelves:
            codes.append(s[1:])
    if len(codes) == 0:
        return None
    else:
        return','.join(sorted(codes))


def report_data(fh):
    with open(fh, 'r') as file:
        reader = csv.reader(
            file, encoding='utf-8',
            delimiter='^', quoting=csv.QUOTE_NONE)
        reader.next()  # skip header

        counter = 1
        for row in reader:
            counter += 1

            try:
                bid = verify_bib_id(row[0], counter)
                b_date = parse_dates(row[1], counter)
                o_date = parse_dates(row[12], counter)
                oid = verify_ord_id(row[11], counter)

                # skip rows with incomplete data
                if bid is None or b_date is None or oid is None or \
                        o_date is None:
                    continue

                # omit rows with orders older than 6 months
                age = datetime.now() - o_date
                if age.days > 180:
                    continue

                b_type = row[2]
                b_call = row[5]
                c_dewey = parse_call_dewey(b_call)
                subjects = parse_subjects(row[8], counter)

                yield (
                    dict(
                        id=bid,
                        b_date=b_date,
                        b_type=b_type,
                        title=parse_title(row[3]),
                        author=parse_name(row[4], counter),
                        b_call=b_call,
                        c_format=parse_call_format(b_call),
                        c_audn=parse_call_audn(b_call),
                        c_lang=parse_call_lang(b_call),
                        c_type=parse_call_type(b_call),
                        c_cutter=parse_call_cutter(b_call),
                        c_dewey=c_dewey,
                        c_division=identify_dewey_range(c_dewey),
                        b_lang=find_main_language(row[6], row[7], counter),
                        subjects=subjects,
                        subject_person=parse_subject_person(row[9], counter),
                        crit_work=idenfity_critical_work(
                            row[9], row[10], counter),
                        b_format=find_bib_format(
                            b_type, row[6], subjects, counter)),
                    dict(
                        id=oid,
                        bid=bid,
                        o_date=o_date,
                        o_branch=parse_branches(row[13], counter),
                        o_shelf=parse_o_shelf(parse_shelves(row[13], counter)),
                        o_audn=parse_ord_audn(parse_shelves(row[13], counter)),
                        copies=0 if row[14] == '' else int(row[14]),
                        ven_note=None if row[15].strip() == '' else row[15].strip())) # see if more detailed parsing for vendor notes is needed

            except IndexError:
                module_logger.error(
                    'IndexError in line {}, '
                    'found data: {}'.format(
                        counter, list(enumerate(row))))
                continue


if __name__ == '__main__':
    import logging.config
    import loggly.handlers

    from logging_setup import LOGGING

    logging.config.dictConfig(LOGGING)

    test_fh = './files/sierra_test_list.txt'
    data = report_data(test_fh)
    print [x for x in data.next()[1]]
