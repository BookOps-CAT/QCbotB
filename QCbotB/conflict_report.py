# creates an error report

from datetime import date

from datastore import session_scope
from db_worker import run_query


def create_report(query_date=None):
    if query_date is None:
        query_date = date.today().strftime('%Y-%m-%d')

    stmn = """SELECT timestamp, bid, bibs.title, bibs.b_call, copies.oid, copies.copies,
        code, description
        FROM tickets
        JOIN bibs ON tickets.bid = bibs.id
        JOIN copies ON tickets.id = copies.tid
        JOIN tick_conf_joiner ON tick_conf_joiner.tid = tickets.id
        JOIN conflicts ON tick_conf_joiner.cid = conflicts.id
        WHERE timestamp LIKE "{}%" """.format(query_date)

    msg = []
    msg.append('BPL QCbot report for day {}:'.format(query_date))
    msg.append('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
        'bib id' + ' ' * 4,
        'order id' + ' ' * 2,
        'copies',
        'title' + ' ' * 20,
        'call #' + ' ' * 19,
        'error code',
        'error description'))

    with session_scope() as session:
        results = run_query(session, stmn)
        for record in results:
            # shorten title if needed
            try:
                title = record.title[:25]
            except IndexError:
                title = record.title
            except TypeError:
                title = ''

            # shorten call number if needed
            try:
                callNo = record.b_call[:25]
            except IndexError:
                callNo = record.b_call
            except TypeError:
                callNo = ''

            # copies
            clen = 6 - len('{}'.format(record.copies))
            copies = '{}{}'.format(
                record.copies, ' ' * clen)

            # title
            tlen = 25 - len(title)
            title = '{}{}'.format(
                title, ' ' * tlen)

            # call number
            cnlen = 25 - len(callNo)
            callNo = '{}{}'.format(
                callNo, ' ' * cnlen)

            # error code
            code = '{}{}'.format(
                record.code, ' ' * 3)

            # create a new line with data
            msg.append(
                'b{}a\to{}a\t{}\t{}\t{}\t{}\t{}'.format(
                    record.bid,
                    record.oid,
                    copies,
                    title,
                    callNo,
                    code,
                    record.description))

    return '\n'.join(msg)
