"""
KimiGPT - Database Initialization
"""

import sqlite3
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Get absolute path to database
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "database", "kimigpt.db")


def init_database(db_path=None):
    """Initialize SQLite database"""
    if db_path is None:
        db_path = DEFAULT_DB_PATH

    logger.info("Initializing database...")

    # Ensure database directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            website_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_prompt TEXT,
            analysis TEXT,
            files_path TEXT,
            zip_path TEXT,
            qa_score REAL,
            status TEXT DEFAULT 'completed'
        )
    ''')

    # Create api_usage table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tokens_used INTEGER,
            response_time REAL,
            success BOOLEAN,
            error TEXT
        )
    ''')

    # Create sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active',
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

    logger.info("✓ Database initialized successfully")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_database()
