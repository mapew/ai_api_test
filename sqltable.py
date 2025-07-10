import sqlite3

conn = sqlite3.connect("test.db")

cursor = conn.cursor()
sqlcommend = "INSERT INTO Hold (ITEM, LOT, REASON, ACTION) VALUES (?,?,?,?)"

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Hold (
        ITEM TEXT,
        LOT TEXT,
        REASON TEXT,
        ACTION TEXT
        )
    """)
sqlcommend = "INSERT INTO Hold (ITEM, LOT, REASON, ACTION) VALUES (?,?,?,?)"
values = ("Coconut", "LOT123", "Damaged packaging", "Dispose")


try:
    cursor.execute(sqlcommend, values)
except sqlite3.Error as e:
    print(f"Error inserting data: {e}")


cursor.execute("SELECT * FROM Hold")

# Print each row from the result
rows = cursor.fetchall()
for row in rows:
    print(row)


conn.commit()
conn.close()
