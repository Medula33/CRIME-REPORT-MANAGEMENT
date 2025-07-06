import mysql.connector
from database.database import Database

class ReportCrime:
    def __init__(self, db_config):
        self.db = Database(**db_config)

    def report_crime(self):
        cursor = None
        try:
            connection = self.db.connect()
            if connection:
                cursor = connection.cursor()
                print("\nPlease provide details of the crime:")
                location = input("Location: ")
                crime_type = input("Crime Type: ")
                description = input("Description: ")
                notes = input("Additional Notes: ")
                cursor.execute("INSERT INTO reports (location, crime_type, description, notes) VALUES (%s, %s, %s, %s)", 
                               (location, crime_type, description, notes))
                connection.commit()
                print("Crime reported successfully.")
            else:
                print("Failed to connect to the database.")
        except mysql.connector.Error as error:
            print(f"Failed to report crime: {error}")
        finally:
            if cursor:
                cursor.close()
            self.db.close()
