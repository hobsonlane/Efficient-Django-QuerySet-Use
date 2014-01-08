from datetime import datetime
import django.db
import sqlparse

class QueryTimer(object):
    """Based on https://github.com/jfalkner/Efficient-Django-QuerySet-Use

    >>> from example.models import Sample
    >>> qt = QueryTimer()
    >>> cm_list = list(Sample.objects.values()[:10])
    >>> qt.stop()  # doctest: +ELLIPSIS
    QueryTimer(time=0.0..., num_queries=1)
    """

    def __init__(self, time=None, num_queries=None, sql='', connection=None):
        self.connection = connection or django.db.connection
        self.time, self.num_queries = time, num_queries
        self.start_time, self.start_queries, self.queries = None, None, None
        self.sql = sql
        self.start()

    def start(self):
        self.queries = []
        self.start_time = datetime.datetime.now()
        self.start_queries = len(self.connection.queries)

    def stop(self):
        self.time = (datetime.datetime.now() - self.start_time).total_seconds()
        self.queries = self.connection.queries[self.start_queries:]
        self.num_queries = len(self.queries)
        print self

    def format_sql(self):
        if self.time is None or self.queries is None:
            self.stop()
        if self.queries or not self.sql:
            self.sql = []
            for query in self.queries:
                self.sql += [sqlparse.format(query['sql'], reindent=True, keyword_case='upper')]
        return self.sql

    def __repr__(self):
        return '%s(time=%s, num_queries=%s)' % (self.__class__.__name__, self.time, self.num_queries)



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
