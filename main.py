from operations.report_crime import ReportCrime
from operations.view_crime_reports import ViewCrimeReports
from operations.delete_crime import DeleteCrime
from operations.view_summary_by_location import ViewSummaryByLocation
from database.database import Database
from menu import Menu

def main():
    db_config = {
        'host': 'localhost',
        'database': 'crime_reports_db',
        'user': 'root',
        'password': 'find your way'
    }

    database = Database(**db_config)
    database.create_table()

    while True:
        Menu.display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            reporter = ReportCrime(db_config)
            reporter.report_crime()
        elif choice == '2':
            viewer = ViewCrimeReports(db_config)
            viewer.view_crime_reports()
        elif choice == '3':
            deleter = DeleteCrime(db_config)
            deleter.delete_crime()
        elif choice == '4':
            summary_viewer = ViewSummaryByLocation(db_config)
            summary_viewer.view_summary_by_location()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
