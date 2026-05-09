import psycopg

conn = psycopg.connect(
    host="127.0.0.1",
    port=5434,
    dbname="boardgames",
    user="bg",
    password="bg"
)

print("OK")
conn.close()