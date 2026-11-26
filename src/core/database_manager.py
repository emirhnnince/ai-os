"""
AI OS Birleşik SQLite Veritabanı Yöneticisi (Unified Database Layer)
Kullanıcı profilleri, Google OAuth oturumları, öğrenilen hafıza kuralları,
sistem ayarları ve e-öğrenme ilerlemelerini tek, güvenli ve şifrelenebilir bir yerde tutar.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "db"))
DB_PATH = os.path.join(DB_DIR, "ai_os_core.db")

class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_schema()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 1. Users & Auth (Local & Google)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                auth_type TEXT NOT NULL, -- guest, local, google
                email TEXT,
                google_sub TEXT,
                password_hash TEXT,
                preferences_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 2. Dynamic Learned Knowledge Rules
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                pattern TEXT NOT NULL,
                reflection TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 3. Telemetry & Hardware Logs
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                details_json TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 4. Global Settings (i18n, model, privacy)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """)
            conn.commit()

    def set_setting(self, key: str, value: str):
        with self.get_connection() as conn:
            conn.cursor().execute(
                "INSERT OR REPLACE INTO system_settings (key, value) VALUES (?, ?)",
                (key, str(value))
            )
            conn.commit()

    def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
        with self.get_connection() as conn:
            row = conn.cursor().execute("SELECT value FROM system_settings WHERE key = ?", (key,)).fetchone()
            return row["value"] if row else default

    def add_learned_rule(self, category: str, pattern: str, reflection: str, confidence: float = 1.0):
        with self.get_connection() as conn:
            conn.cursor().execute(
                "INSERT INTO learned_rules (category, pattern, reflection, confidence) VALUES (?, ?, ?, ?)",
                (category, pattern, reflection, confidence)
            )
            conn.commit()

    def get_learned_rules(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            rows = conn.cursor().execute("SELECT * FROM learned_rules ORDER BY id DESC LIMIT 50").fetchall()
            return [dict(r) for r in rows]

    def register_or_update_google_user(self, email: str, name: str, google_sub: str) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            user_id = f"google_{google_sub[:8]}"
            cursor.execute("""
            INSERT INTO users (id, username, auth_type, email, google_sub, last_login)
            VALUES (?, ?, 'google', ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                email = excluded.email,
                last_login = CURRENT_TIMESTAMP
            """, (user_id, name, email, google_sub))
            conn.commit()
            return {"user_id": user_id, "username": name, "email": email, "auth_type": "google"}
