import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

try:
    # Create OrderTracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS core_ordertracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            status VARCHAR(20) NOT NULL,
            message TEXT NOT NULL,
            location VARCHAR(200) DEFAULT "",
            updated_by VARCHAR(100) DEFAULT "System",
            created_at DATETIME NOT NULL,
            FOREIGN KEY (order_id) REFERENCES core_order (id)
        )
    ''')
    print('Created core_ordertracking table')
except Exception as e:
    print(f'Error creating table: {e}')

# Commit changes and close
conn.commit()
conn.close()
print('OrderTracking table created successfully!')
