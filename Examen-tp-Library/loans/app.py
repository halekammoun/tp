from flask import Flask, request, jsonify
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
    return jsonify(service="loans", status="ok")

@app.get("/loans")
def list_loans():
    try:
        conn = connect_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, member_id, book_id, created_at FROM loans ORDER BY id DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Error as exc:
        return jsonify(error="Database unavailable", detail=str(exc)), 503

@app.post("/loans")
def create_loan():
    data = request.get_json(silent=True) or {}
    member_id, book_id = data.get("member_id"), data.get("book_id")
    if not isinstance(member_id, int) or not isinstance(book_id, int):
        return jsonify(error="integer member_id and book_id are required"), 400
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO loans(member_id, book_id) VALUES (%s, %s)", (member_id, book_id))
        conn.commit()
        loan_id = cur.lastrowid
        cur.close()
        conn.close()
        return jsonify(message="Loan created", id=loan_id), 201
    except Error as exc:
        return jsonify(error="Database unavailable", detail=str(exc)), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
