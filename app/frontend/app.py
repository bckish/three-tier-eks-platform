import os

import requests
from flask import Flask, render_template_string

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5000")


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Three-Tier Kubernetes Application</title>
</head>
<body>
    <h1>Three-Tier Kubernetes Application</h1>

    <h2>Frontend</h2>
    <p>Frontend is running successfully.</p>

    <h2>Backend</h2>
    <p>{{ backend_message }}</p>

    <h2>Database</h2>
    <p>{{ database_status }}</p>
</body>
</html>
"""


@app.get("/")
def home():
    backend_message = "Backend unavailable"
    database_status = "Database unavailable"

    try:
        response = requests.get(
            f"{BACKEND_URL}/api",
            timeout=3,
        )

        if response.ok:
            backend_message = response.json().get(
                "message",
                "Backend responded successfully",
            )
    except requests.RequestException as exc:
        backend_message = f"Backend connection failed: {exc}"

    try:
        response = requests.get(
            f"{BACKEND_URL}/api/db",
            timeout=3,
        )

        if response.ok:
            database_status = response.json().get(
                "database",
                "Unknown",
            )
    except requests.RequestException as exc:
        database_status = f"Database check failed: {exc}"

    return render_template_string(
        HTML,
        backend_message=backend_message,
        database_status=database_status,
    )


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002,
    )