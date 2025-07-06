import mysql.connector
from prettytable import PrettyTable
from database.database import Database

class ViewCrimeReports:
    def __init__(self, db_config):
        self.db = Database(**db_config)

    def view_crime_reports(self):
        cursor = None
        try:
            connection = self.db.connect()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT id, location, crime_type, description, notes, time FROM reports")
                records = cursor.fetchall()
                if not records:
                    print("\nNo crimes reported yet.")
                else:
                    table = PrettyTable(['ID', 'Location', 'Crime Type', 'Description', 'Notes', 'Time'])
                    for record in records:
                        table.add_row([record['id'], record['location'], record['crime_type'], record['description'], record['notes'], record['time']])
                    print(table)
            else:
                print("Failed to connect to the database.")
        except mysql.connector.Error as error:
            print(f"Failed to retrieve crime reports: {error}")
        finally:
            if cursor:
                cursor.close()
            self.db.close()

