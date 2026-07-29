from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import sqlite3
import time
import os
import sys
import psutil
import json
import uuid

app = Flask(__name__)
CORS(app, origins="*")

DB_PATH = os.path.join(os.path.dirname(__file__), "caganx_admin.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Active Users / Sessions
    c.execute('''CREATE TABLE IF NOT EXISTS active_sessions (
        session_id TEXT PRIMARY KEY,
        ip TEXT,
        user_agent TEXT,
        page TEXT,
        first_seen REAL,
        last_seen REAL
    )''')
    
    # Users Management
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        role TEXT DEFAULT 'User',
        status TEXT DEFAULT 'Active',
        ip TEXT,
        created_at REAL,
        last_seen REAL
    )''')
    
    # Activity Logs
    c.execute('''CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        username TEXT,
        ip TEXT,
        action TEXT,
        details TEXT,
        timestamp REAL
    )''')
    
    # Error Logs
    c.execute('''CREATE TABLE IF NOT EXISTS error_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        page TEXT,
        error_msg TEXT,
        stack_trace TEXT,
        timestamp REAL
    )''')
    
    # Banned IPs / Users
    c.execute('''CREATE TABLE IF NOT EXISTS bans (
        ip TEXT PRIMARY KEY,
        reason TEXT,
        created_at REAL
    )''')

    # System Settings (Maintenance mode, announcements)
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )''')
    
    # Defaults
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('maintenance', '0')")
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('announcement', '')")
    
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Clean up stale sessions (> 30s inactivity)
def cleanup_sessions():
    conn = get_db()
    c = conn.cursor()
    cutoff = time.time() - 30
    c.execute("DELETE FROM active_sessions WHERE last_seen < ?", (cutoff,))
    conn.commit()
    conn.close()

# API: Heartbeat from main site
@app.route("/api/ping", methods=["POST"])
def ping():
    data = request.json or {}
    session_id = data.get("session_id") or request.remote_addr
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "Unknown")
    page = data.get("page", "/")
    now = time.time()
    
    conn = get_db()
    c = conn.cursor()
    
    # Check if banned
    c.execute("SELECT ip FROM bans WHERE ip = ?", (ip,))
    if c.fetchone():
        conn.close()
        return jsonify({"status": "banned", "message": "Erişiminiz engellenmiştir."}), 403

    c.execute("SELECT session_id FROM active_sessions WHERE session_id = ?", (session_id,))
    if c.fetchone():
        c.execute("UPDATE active_sessions SET last_seen = ?, page = ?, ip = ? WHERE session_id = ?", (now, page, ip, session_id))
    else:
        c.execute("INSERT INTO active_sessions (session_id, ip, user_agent, page, first_seen, last_seen) VALUES (?, ?, ?, ?, ?, ?)",
                  (session_id, ip, user_agent, page, now, now))
        # Log first visit activity
        c.execute("INSERT INTO activity_logs (session_id, username, ip, action, details, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                  (session_id, "Misafir", ip, "Siteye Giriş", f"Sayfa: {page}", now))

    # Check maintenance mode & announcement
    c.execute("SELECT key, value FROM settings")
    settings = {row["key"]: row["value"] for row in c.fetchall()}
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "status": "ok",
        "maintenance": settings.get("maintenance", "0") == "1",
        "announcement": settings.get("announcement", "")
    })

# API: Log user activity (card click, video edit, etc.)
@app.route("/api/log_activity", methods=["POST"])
def log_activity():
    data = request.json or {}
    session_id = data.get("session_id") or request.remote_addr
    username = data.get("username", "Misafir")
    ip = request.remote_addr
    action = data.get("action", "Genel Aksiyon")
    details = data.get("details", "")
    now = time.time()
    
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO activity_logs (session_id, username, ip, action, details, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
              (session_id, username, ip, action, details, now))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

# API: Log Javascript Error
@app.route("/api/log_error", methods=["POST"])
def log_error():
    data = request.json or {}
    ip = request.remote_addr
    page = data.get("page", "/")
    error_msg = data.get("error", "Bilinmeyen Hata")
    stack_trace = data.get("stack", "")
    now = time.time()
    
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO error_logs (ip, page, error_msg, stack_trace, timestamp) VALUES (?, ?, ?, ?, ?)",
              (ip, page, error_msg, stack_trace, now))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

# ADMIN API: Get Full Dashboard Data
@app.route("/admin/api/stats", methods=["GET"])
def admin_stats():
    cleanup_sessions()
    conn = get_db()
    c = conn.cursor()
    
    # Active Users
    c.execute("SELECT COUNT(*) FROM active_sessions")
    active_count = c.fetchone()[0]
    
    # Total Users / Visits
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    
    # Total Edits Today
    today_start = time.time() - 86400
    c.execute("SELECT COUNT(*) FROM activity_logs WHERE timestamp >= ?", (today_start,))
    edits_today = c.fetchone()[0]
    
    # Active Users Detail List
    c.execute("SELECT session_id, ip, user_agent, page, last_seen FROM active_sessions ORDER BY last_seen DESC LIMIT 20")
    active_users = [dict(row) for row in c.fetchall()]

    # Recent Activity Stream
    c.execute("SELECT id, username, ip, action, details, timestamp FROM activity_logs ORDER BY id DESC LIMIT 25")
    recent_logs = [dict(row) for row in c.fetchall()]

    # Recent Error Logs
    c.execute("SELECT id, ip, page, error_msg, timestamp FROM error_logs ORDER BY id DESC LIMIT 15")
    error_logs = [dict(row) for row in c.fetchall()]

    # Users List
    c.execute("SELECT id, username, email, role, status, ip, created_at, last_seen FROM users ORDER BY id DESC")
    users = [dict(row) for row in c.fetchall()]

    # Ban List
    c.execute("SELECT ip, reason, created_at FROM bans")
    bans = [dict(row) for row in c.fetchall()]

    # Settings
    c.execute("SELECT key, value FROM settings")
    settings = {row["key"]: row["value"] for row in c.fetchall()}

    # System Performance Metrics
    cpu_percent = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    conn.close()
    
    return jsonify({
        "active_users": active_count,
        "total_users": total_users,
        "edits_today": edits_today,
        "active_list": active_users,
        "recent_logs": recent_logs,
        "error_logs": error_logs,
        "users": users,
        "bans": bans,
        "settings": settings,
        "system": {
            "cpu": cpu_percent,
            "ram_percent": ram.percent,
            "ram_used_mb": round(ram.used / (1024 * 1024), 1),
            "ram_total_mb": round(ram.total / (1024 * 1024), 1),
            "disk_percent": disk.percent
        }
    })

# ADMIN API: Toggle Maintenance Mode
@app.route("/admin/api/toggle_maintenance", methods=["POST"])
def toggle_maintenance():
    data = request.json or {}
    val = "1" if data.get("maintenance") else "0"
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('maintenance', ?)", (val,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok", "maintenance": val == "1"})

# ADMIN API: Set Announcement
@app.route("/admin/api/set_announcement", methods=["POST"])
def set_announcement():
    data = request.json or {}
    msg_text = data.get("text", "")
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('announcement', ?)", (msg_text,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok", "announcement": msg_text})

# ADMIN API: Ban / Unban IP
@app.route("/admin/api/ban_ip", methods=["POST"])
def ban_ip():
    data = request.json or {}
    ip = data.get("ip", "").strip()
    reason = data.get("reason", "Kural ihlali")
    if not ip:
        return jsonify({"status": "error", "message": "Geçersiz IP"}), 400
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO bans (ip, reason, created_at) VALUES (?, ?, ?)", (ip, reason, time.time()))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/admin/api/unban_ip", methods=["POST"])
def unban_ip():
    data = request.json or {}
    ip = data.get("ip", "").strip()
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM bans WHERE ip = ?", (ip,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

# Render Admin GUI
@app.route("/")
def admin_page():
    html_file = os.path.join(os.path.dirname(__file__), "admin_panel.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Admin Panel Arayüzü Hazırlanıyor...</h1>"

if __name__ == "__main__":
    print("🛡️ caganx AI edit - Özel Admin Panel Sunucusu Başlatıldı! (Port 9090)")
    app.run(host="0.0.0.0", port=9090, debug=False)
