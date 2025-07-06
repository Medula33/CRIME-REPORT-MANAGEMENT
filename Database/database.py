import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
                return self.connection
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed")

    def create_table(self):
        cursor = None
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reports (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        location VARCHAR(255) NOT NULL,
                        crime_type VARCHAR(255) NOT NULL,
                        description TEXT NOT NULL,
                        notes TEXT,
                        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                connection.commit()
                print("Table 'reports' created successfully.")
        except mysql.connector.Error as e:
            print(f"Error creating table: {e}")
        finally:
            if cursor:
                cursor.close()
            self.close()
