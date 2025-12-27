import psycopg2
import json

# "postgresql://postgres:password@postgres:5432/dsanagbot"
DB_URL = "postgresql://postgres:password@postgres:5432/dsanagbot"

def init_db():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        chat_id BIGINT PRIMARY KEY,
        username VARCHAR(100),
        phase VARCHAR(20) DEFAULT 'phase1',
        day_number INTEGER DEFAULT 1,
        solve_rate DECIMAL(5,4) DEFAULT 0.0,
        streak INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT NOW()
    );
    
    CREATE TABLE IF NOT EXISTS daily_schedule (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT REFERENCES users(chat_id),
        day_number INTEGER,
        task1 TEXT, task2 TEXT, task3 TEXT,
        completed1 BOOLEAN DEFAULT FALSE,
        completed2 BOOLEAN DEFAULT FALSE,
        completed3 BOOLEAN DEFAULT FALSE,
        reminders_sent INTEGER DEFAULT 0,
        created_at DATE DEFAULT CURRENT_DATE
    );
    
    CREATE TABLE IF NOT EXISTS ai_todo (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT REFERENCES users(chat_id),
        status VARCHAR(20) DEFAULT 'todo',
        priority INTEGER DEFAULT 1,
        task_description TEXT NOT NULL,
        current_step INTEGER DEFAULT 0,
        total_steps INTEGER,
        context JSONB,
        result TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database initialized with AI Todo system!")

if __name__ == "__main__":
    init_db()
