import mysql.connector
from mysql.connector import Error
import pandas as pd

class TorontoParkingDB:
    """Helper class to connect to MySQL and run queries easily"""
    
    def __init__(self, host='localhost', user='root', password='1234567890', database='toronto_parking_db'):
        """Initialize database connection settings"""
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.conn = None
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.conn = mysql.connector.connect(**self.config)
            if self.conn.is_connected():
                print("✓ Connected to MySQL database")
                return True
        except Error as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def disconnect(self):
        """Close connection to MySQL"""
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("✓ Disconnected from MySQL")
    
    def query_to_dataframe(self, query):
        """Run SQL query and get results as a DataFrame (for SELECT queries)"""
        try:
            if not self.conn or not self.conn.is_connected():
                self.connect()
            
            df = pd.read_sql(query, self.conn)
            print(f"✓ Query executed: {len(df)} rows returned")
            return df
        except Error as e:
            print(f"✗ Query error: {e}")
            return None
    
    def execute_query(self, query):
        """Run SQL query without returning results (for INSERT, UPDATE, DELETE)"""
        try:
            if not self.conn or not self.conn.is_connected():
                self.connect()
            
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            print(f"✓ Query executed successfully")
            cursor.close()
            return True
        except Error as e:
            print(f"✗ Query error: {e}")
            self.conn.rollback()
            return False
    
    # Pre-built query methods (ready to use!)
    
    def get_summary_stats(self):
        """Get basic summary statistics"""
        query = """
        SELECT 
            COUNT(*) as total_tickets,
            COUNT(DISTINCT DATE(date_of_infraction)) as unique_dates,
            AVG(set_fine_amount) as avg_fine,
            MIN(set_fine_amount) as min_fine,
            MAX(set_fine_amount) as max_fine
        FROM parking_tickets
        """
        return self.query_to_dataframe(query)
    
    def get_top_infractions(self, limit=10):
        """Get most common infraction types"""
        query = f"""
        SELECT 
            infraction_description,
            COUNT(*) as count,
            ROUND(AVG(set_fine_amount), 2) as avg_fine
        FROM parking_tickets
        GROUP BY infraction_description
        ORDER BY count DESC
        LIMIT {limit}
        """
        return self.query_to_dataframe(query)
    
    def get_by_ward(self):
        """Get tickets grouped by ward"""
        query = """
        SELECT 
            ward,
            COUNT(*) as count,
            ROUND(AVG(set_fine_amount), 2) as avg_fine
        FROM parking_tickets
        WHERE ward IS NOT NULL
        GROUP BY ward
        ORDER BY count DESC
        """
        return self.query_to_dataframe(query)
    
    def get_by_date(self):
        """Get tickets grouped by date"""
        query = """
        SELECT 
            DATE(date_of_infraction) as date,
            COUNT(*) as count
        FROM parking_tickets
        WHERE date_of_infraction IS NOT NULL
        GROUP BY DATE(date_of_infraction)
        ORDER BY date
        """
        return self.query_to_dataframe(query)
    
    def get_fine_distribution(self):
        """Get distribution of fine amounts"""
        query = """
        SELECT 
            CASE 
                WHEN set_fine_amount < 50 THEN 'Under $50'
                WHEN set_fine_amount < 100 THEN '$50-$100'
                WHEN set_fine_amount < 150 THEN '$100-$150'
                ELSE 'Over $150'
            END as fine_range,
            COUNT(*) as count
        FROM parking_tickets
        WHERE set_fine_amount IS NOT NULL
        GROUP BY fine_range
        ORDER BY fine_range
        """
        return self.query_to_dataframe(query)

if __name__ == "__main__":
    # Test: Try connecting and running a query
    db = TorontoParkingDB(password='1234567890')
    db.connect()
    
    print("\n📊 Summary Statistics:")
    stats = db.get_summary_stats()
    print(stats)
    
    print("\n📌 Top 10 Infractions:")
    infractions = db.get_top_infractions(limit=10)
    print(infractions)
    
    db.disconnect()