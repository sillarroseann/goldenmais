import sqlite3
import os

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

try:
    # Add tracking_number column
    cursor.execute('ALTER TABLE core_order ADD COLUMN tracking_number VARCHAR(50) DEFAULT ""')
    print('Added tracking_number column')
except Exception as e:
    print(f'tracking_number column might already exist: {e}')

try:
    # Add estimated_delivery column
    cursor.execute('ALTER TABLE core_order ADD COLUMN estimated_delivery DATETIME')
    print('Added estimated_delivery column')
except Exception as e:
    print(f'estimated_delivery column might already exist: {e}')

try:
    # Add delivered_at column
    cursor.execute('ALTER TABLE core_order ADD COLUMN delivered_at DATETIME')
    print('Added delivered_at column')
except Exception as e:
    print(f'delivered_at column might already exist: {e}')

try:
    # Add delivery_notes column
    cursor.execute('ALTER TABLE core_order ADD COLUMN delivery_notes TEXT DEFAULT ""')
    print('Added delivery_notes column')
except Exception as e:
    print(f'delivery_notes column might already exist: {e}')

# Commit changes and close
conn.commit()
conn.close()
print('Database updated successfully!')
