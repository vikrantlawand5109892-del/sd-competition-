from flask import Flask, g
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
app.config['DB_CONFIG'] = {
    "host": "localhost",
    "user": "root",
    "password": "asma239",
    "database": "travelease"
}

def get_db():
    """Get database connection"""
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**app.config['DB_CONFIG'])
            g.db.autocommit = True
        except Error as e:
            print("Error connecting to MySQL:", e)
            return None
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize database tables"""
    with app.app_context():
        db = get_db()
        if db:
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100),
                    service_type VARCHAR(50),
                    origin VARCHAR(100),
                    destination VARCHAR(100),
                    date VARCHAR(50),
                    extra_info VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db.commit()
            cursor.close()

def save_booking(username, service, origin, destination, date, extra_info):
    """Save booking to database"""
    db = get_db()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO bookings (username, service_type, origin, destination, date, extra_info)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, service, origin, destination, date, extra_info))
            db.commit()
            cursor.close()
            return True
        except Error as e:
            print("Error saving booking:", e)
            return False

# Register the close_db function to run when the app context tears down
app.teardown_appcontext(close_db)