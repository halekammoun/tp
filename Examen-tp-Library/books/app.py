from flask import Flask, jsonify
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "database"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "libraryuser"),
        password=os.getenv("DB_PASSWORD", "LibraryPass123!"),
        database=os.getenv("DB_NAME", "librarydb"),
    )

@app.get("/health")
def health():
    return jsonify(service="books", status="ok")

@app.get("/books")
def list_books():
    try:
        conn = connect_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, title, author FROM books ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Error as exc:
        return jsonify(error="Database unavailable", detail=str(exc)), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
