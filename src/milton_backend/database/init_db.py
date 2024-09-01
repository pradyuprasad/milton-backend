from .database import Database

def create_tags_table():
    db = Database()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        group_id TEXT NOT NULL,
        notes TEXT,
        created TEXT,
        popularity INTEGER,
        series_count INTEGER
    );
    """
    db._cursor.execute(create_table_query)
    db._conn.commit()

def create_series_table():
    db = Database()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fred_id TEXT NOT NULL UNIQUE,
        realtime_start TEXT,
        realtime_end TEXT,
        title TEXT NOT NULL,
        observation_start TEXT,
        observation_end TEXT,
        frequency TEXT,
        frequency_short TEXT,
        units TEXT,
        units_short TEXT,
        seasonal_adjustment TEXT,
        seasonal_adjustment_short TEXT,
        last_updated TEXT,
        popularity INTEGER,
        group_popularity INTEGER,
        notes TEXT
    );
    """
    db._cursor.execute(create_table_query)
    db._conn.commit()

def initialize_database():
    create_tags_table()
    create_series_table()
    print("Database initialization complete.")

if __name__ == "__main__":
    initialize_database()    
