import mysql.connector
from prettytable import PrettyTable
from database.database import Database

class ViewSummaryByLocation:
    def __init__(self, db_config):
        self.db = Database(**db_config)

    def view_summary_by_location(self):
        cursor = None
        try:
            connection = self.db.connect()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT location, COUNT(*) AS count FROM reports GROUP BY location")
                records = cursor.fetchall()
                if records:
                    table = PrettyTable(['Location', 'Number of Crimes'])
                    for record in records:
                        table.add_row([record['location'], record['count']])
                    print("\nSummary of Reported Crimes by Location:")
                    print(table)
                else:
                    print("\nNo crimes reported yet.")
            else:
                print("Failed to connect to the database.")
        except mysql.connector.Error as error:
            print(f"Failed to retrieve summary: {error}")
        finally:
            if cursor:
                cursor.close()
            self.db.close()
