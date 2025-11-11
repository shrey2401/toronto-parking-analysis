import pandas as pd
import mysql.connector
from mysql.connector import Error

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234567890',  
    'database': 'toronto_parking_db'
}

def create_database():
    """Step 1: Create the database if it doesn't exist"""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        print(f"✓ Database '{MYSQL_CONFIG['database']}' created/verified")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"✗ Error creating database: {e}")
        raise

def create_table():
    """Step 2: Create the parking_tickets table"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS parking_tickets (
            ticket_id INT PRIMARY KEY AUTO_INCREMENT,
            date_of_infraction DATE,
            infraction_code INT,
            infraction_description VARCHAR(255),
            set_fine_amount DECIMAL(10, 2),
            location_street VARCHAR(255),
            latitude DECIMAL(10, 8),
            longitude DECIMAL(11, 8),
            ward VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("✓ Table 'parking_tickets' created/verified")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"✗ Error creating table: {e}")
        raise

def upload_data():
    """Step 3: Upload cleaned CSV data to MySQL"""
    try:
        # Read CSV file
        csv_path = 'data/parking_tickets_cleaned.csv'
        df = pd.read_csv(csv_path)
        
        print(f"📊 Loaded {len(df)} records from CSV")
        
        # Connect to database
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # SQL insert statement
        insert_query = """
        INSERT INTO parking_tickets 
        (date_of_infraction, infraction_code, infraction_description, 
         set_fine_amount, location_street, latitude, longitude, ward)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Prepare data as tuples
        data_tuples = []
        for _, row in df.iterrows():
            data_tuples.append((
                row.get('date_of_infraction'),
                row.get('infraction_code'),
                row.get('infraction_description'),
                row.get('set_fine_amount'),
                row.get('location_street'),
                row.get('latitude'),
                row.get('longitude'),
                row.get('ward')
            ))
        
        # Insert all rows at once
        cursor.executemany(insert_query, data_tuples)
        conn.commit()
        
        print(f"✓ Successfully uploaded {cursor.rowcount} records to MySQL")
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"✗ Error uploading data: {e}")
        raise
    except FileNotFoundError:
        print(f"✗ CSV file not found at {csv_path}")
        raise

def verify_upload():
    """Step 4: Verify data was uploaded correctly"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Count total records
        cursor.execute("SELECT COUNT(*) FROM parking_tickets")
        count = cursor.fetchone()[0]
        
        # Show first 5 rows
        cursor.execute("SELECT * FROM parking_tickets LIMIT 5")
        sample = cursor.fetchall()
        
        print(f"\n✓ Database contains {count} total records")
        print("Sample rows (first 5):")
        for row in sample:
            print(f"  {row}")
        
        cursor.close()
        conn.close()
    except Error as e:
        print(f"✗ Error verifying upload: {e}")
        raise

if __name__ == "__main__":
    print("🚗 Toronto Parking Analysis - Database Upload\n")
    
    try:
        create_database()
        create_table()
        upload_data()
        verify_upload()
        print("\n✅ Upload complete!")
    except Exception as e:
        print(f"\n❌ Upload failed: {e}")
        exit(1)