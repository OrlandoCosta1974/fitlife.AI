import sqlite3

def init_db():
    conn = sqlite3.connect('fitlife.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    conn.commit()
    conn.close()
    print("Banco e tabela 'users' criados com sucesso!")

if __name__ == "__main__":
    init_db()
