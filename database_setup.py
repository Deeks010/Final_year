import sqlite3

def setup_database():
    """
    Creates the storyweaver.db file and all necessary tables.
    This is safe to run multiple times.
    """
    db_name = 'storyweaver.db'
    print(f"--- Setting up database '{db_name}'... ---")

    try:
        # Connect to the database. It will be created if it doesn't exist.
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create child_profiles table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS child_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            interests TEXT,
            favorite_activities TEXT,
            autism_severity TEXT,
            communication_level TEXT,
            personalized_themes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        print("✓ Table 'child_profiles' created or already exists.")

        # Create story_sessions table for tracking
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS story_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_id INTEGER NOT NULL,
            personalized_theme TEXT,
            educational_theme TEXT,
            language TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            duration_seconds INTEGER,
            completed BOOLEAN DEFAULT 0,
            FOREIGN KEY (child_id) REFERENCES child_profiles(id)
        );
        """)
        print("✓ Table 'story_sessions' created or already exists.")

        # Create button_clicks table for tracking user interactions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS button_clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            button_type TEXT NOT NULL,
            part_number INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES story_sessions(id)
        );
        """)
        print("✓ Table 'button_clicks' created or already exists.")

        # Create audio_replays table for tracking audio replay events
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS audio_replays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            part_number INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES story_sessions(id)
        );
        """)
        print("✓ Table 'audio_replays' created or already exists.")

        # Create quiz_results table for storing quiz performance
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            user_answer TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES story_sessions(id)
        );
        """)
        print("✓ Table 'quiz_results' created or already exists.")

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("--- Database setup complete. ---")

    except sqlite3.Error as e:
        print(f"An error occurred during database setup: {e}")

if __name__ == "__main__":
    setup_database()

