def _department_filter(request):
    """Read the requested department from the query string."""
    return request.args.get("dept", "")


def _compose(base_query, value):
    """Attach a department condition to a query."""
    return base_query + " WHERE dept = '" + value + "'"


def run_report(request, conn):
    sql = _compose("SELECT id, name FROM staff", _department_filter(request))
    return conn.execute(sql).fetchall()
