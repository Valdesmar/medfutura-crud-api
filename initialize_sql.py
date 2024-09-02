import sqlite3

with sqlite3.connect("pessoas.db") as conn:
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
