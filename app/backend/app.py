import os

import psycopg
from flask import Flask, jsonify

app = Flask(__name__)


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "apppassword"),
    )


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.get("/api")
def api():
    return jsonify(
        {
            "message": "Hello from the backend API",
            "service": "backend",
        }
    )


@app.get("/api/db")
def database_check():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]

        return jsonify(
            {
                "database": "connected",
                "version": version,
            }
        )

    except Exception as exc:
        return jsonify(
            {
                "database": "connection_failed",
                "error": str(exc),
            }
        ), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
