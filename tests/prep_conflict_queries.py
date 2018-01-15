# add here datastore SQL queries for testing

queries = {
    1: 'SELECT bibs.id, title, copies FROM bibs JOIN orders ON orders.b_id = bibs.id WHERE bibs.c_cutter = 0 AND bibs.c_type != "fea" AND (bibs.c_type != "eas" AND bibs.author IS NULL)',
    2: 'SELECT bibs.id, title, copies FROM bibs JOIN orders ON orders.b_id = bibs.id WHERE (bibs.b_call LIKE "%0" OR bibs.b_call LIKE "%1" OR bibs.b_call LIKE "%2" OR bibs.b_call LIKE "%3" OR bibs.b_call LIKE "%4" OR bibs.b_call LIKE "%5" OR bibs.b_call LIKE "%6" OR bibs.b_call LIKE "%7" OR bibs.b_call LIKE "%8" OR bibs.b_call LIKE "%9")',
    3: 'SELECT bibs.id, title, copies FROM bibs JOIN orders ON orders.b_id = bibs.id WHERE bibs.c_cutter = 1 AND bibs.c_type = "eas" AND bibs.author IS NULL',
    4: 'SELECT bibs.id, title, copies FROM bibs JOIN orders ON orders.b_id = bibs.id WHERE bibs.c_dewey NOT NULL AND bibs.c_dewey LIKE "%0" AND bibs.c_dewey LIKE "%.%"',
}
