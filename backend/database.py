import sqlite3

DATABASE = "crop_predictions.db"


def init_db():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_prediction(disease, confidence):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO predictions (disease, confidence) VALUES (?, ?)",
        (disease, confidence)
    )

    connection.commit()
    connection.close()


def get_predictions():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, disease, confidence, created_at
        FROM predictions
        ORDER BY id DESC
    """)

    results = cursor.fetchall()
    connection.close()

    return results
