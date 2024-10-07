import os
import sqlite3
import csv

# Define your libraries here
GPLMLIBS = ["ana", "cap", "con", "cpd", "dio", "ics", "ind", "mpu", "mcu", "pwr", "rfm", "res", "reg", "xtr", "osc", "opt", "art", "swi"]

def parts_db_create():
    db_path = os.path.join(os.getcwd(), 'parts.sqlite')
    print(f"Creating database in {db_path}")

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Process each library
    for lib in GPLMLIBS:
        print(f"Processing library: {lib}")

        # Drop the table if it exists
        try:
            cursor.execute(f'DROP TABLE IF EXISTS "{lib}"')
            print(f"Dropped table {lib} if it exists")
        except sqlite3.Error as e:
            print(f"Error dropping table {lib}: {e}")
            continue

        # Import the CSV file if it exists
        csv_file = f"{lib}.csv"
        if os.path.isfile(csv_file):
            print(f"Importing {csv_file} into table {lib}")
            try:
                with open(csv_file, newline='') as file:
                    reader = csv.reader(file)
                    header = next(reader)  # Get the header row

                    # Create the table with columns based on the header row
                    columns = ', '.join(f'"{col}" TEXT' for col in header)
                    cursor.execute(f'CREATE TABLE "{lib}" ({columns})')

                    # Insert the CSV data into the table
                    for row in reader:
                        placeholders = ', '.join('?' for _ in row)
                        cursor.execute(f'INSERT INTO "{lib}" VALUES ({placeholders})', row)
            except (sqlite3.Error, IOError) as e:
                print(f"Error importing {csv_file}: {e}")
        else:
            print(f"Warning: {csv_file} not found. Skipping.")

    # Commit and close the connection
    conn.commit()
    conn.close()

    print("Database creation completed")
    print(f"Final database size: {os.path.getsize(db_path)} bytes")

# Call the function to create the database
parts_db_create()
