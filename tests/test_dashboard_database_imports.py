from dashboard.utils import database


def test_execute_query_alias_exists():
    assert hasattr(database, "execute_query")
    assert callable(database.execute_query)
