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
    return jsonify(service="members", status="ok")

@app.get("/members")
def list_members():
    try:
        conn = connect_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, name, created_at FROM members ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Error as exc:
        return jsonify(error="Database unavailable", detail=str(exc)), 503

@app.post("/members")
def add_member():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify(error="name is required"), 400
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO members(name) VALUES (%s)", (name,))
        conn.commit()
        member_id = cur.lastrowid
        cur.close()
        conn.close()
        return jsonify(message="Member added", id=member_id), 201
    except Error as exc:
        return jsonify(error="Database unavailable", detail=str(exc)), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
