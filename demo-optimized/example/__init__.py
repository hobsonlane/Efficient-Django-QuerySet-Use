from datetime import datetime
from django.db import connection as con
import sqlparse

class QueryTimer(object):
    """Based on https://github.com/jfalkner/Efficient-Django-QuerySet-Use"""

    def __init__(self, time=None, num_queries=None, sql=''):
        self.time, self.num_queries = time, num_queries
        self.start_time, self.start_queries = None, None
        self.sql = sql
        self.start()

    def start(self):
        self.queries = []
        self.start_time = datetime.now()
        self.start_queries = len(con.queries)

    def stop(self):
        self.time = datetime.now() - self.start_time
        self.queries = con.queries[self.start_queries:]
        self.num_queries = len(self.queries)

    def format_sql(self):
        if self.time is None or self.queries is None:
            self.stop()
        if self.queries or not self.sql:
            self.sql = []
            for query in self.queries:
                self.sql += [sqlparse.format(query['sql'], reindent=True, keyword_case='upper')]
        return self.sql

    def __repr__(self):
        return '%s(time=%s, num_queries=%s, sql=%s)' % (self.__class__.__name__, self.time, self.num_queries)


def start():
    global start_time
    global query_count
    start_time = datetime.now()
    query_count = len(con.queries)

def finish():
    print "Time: %s"%(datetime.now()-start_time)
    print "Queries: %s"%(len(con.queries)-query_count)

    for query in con.queries[query_count:]:
        print sqlparse.format(query['sql'], reindent=True, keyword_case='upper')
