import mysql.connector
from database.database import Database
from operations.view_crime_reports import ViewCrimeReports

class DeleteCrime:
    def __init__(self, db_config):
        self.db = Database(**db_config)
        self.view_reports = ViewCrimeReports(db_config)

    def delete_crime(self):
        cursor = None
        try:
            connection = self.db.connect()
            if connection:
                cursor = connection.cursor()
                self.view_reports.view_crime_reports()
                choice = int(input("Enter the ID of the crime to delete: "))
                cursor.execute("DELETE FROM reports WHERE id = %s", (choice,))
                connection.commit()
                if cursor.rowcount > 0:
                    print("Crime deleted successfully.")
                else:
                    print("Invalid crime ID.")
            else:
                print("Failed to connect to the database.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except mysql.connector.Error as error:
            print(f"Failed to delete crime: {error}")
        finally:
            if cursor:
                cursor.close()
            self.db.close()
