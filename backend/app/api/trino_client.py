from trino.dbapi import connect

def get_trino_conn():
    return connect(
        host="localhost",
        port=8080,
        user="admin",
        catalog="postgres",
        schema="public"
    )