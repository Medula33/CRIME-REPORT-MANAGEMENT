from flask import Flask, render_template, request, redirect, url_for
from operations.report_crime import ReportCrime
from operations.view_crime_reports import ViewCrimeReports
from operations.delete_crime import DeleteCrime
from operations.view_summary_by_location import ViewSummaryByLocation
from database.database import Database

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'database': 'crime_reports_db',
    'user': 'root',
    'password': 'find your way'
}

database = Database(**db_config)
database.create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report_crime', methods=['GET', 'POST'])
def report_crime():
    if request.method == 'POST':
        location = request.form['location']
        crime_type = request.form['crime_type']
        description = request.form['description']
        notes = request.form['notes']
        reporter = ReportCrime(db_config)
        cursor = None
        try:
            connection = reporter.db.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO reports (location, crime_type, description, notes) VALUES (%s, %s, %s, %s)",
                    (location, crime_type, description, notes)
                )
                connection.commit()
                cursor.close()
                reporter.db.close()
                return redirect(url_for('index'))
        except Exception as e:
            if cursor:
                cursor.close()
            reporter.db.close()
            print(f"Error: {e}")
    return render_template('report_crime.html')

@app.route('/view_crime_reports')
def view_crime_reports():
    viewer = ViewCrimeReports(db_config)
    cursor = None
    reports = []
    try:
        connection = viewer.db.connect()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, location, crime_type, description, notes, time FROM reports")
            reports = cursor.fetchall()
            cursor.close()
            viewer.db.close()
    except Exception as e:
        if cursor:
            cursor.close()
        viewer.db.close()
        print(f"Error: {e}")
    return render_template('view_crime_reports.html', reports=reports)

@app.route('/delete_crime', methods=['GET', 'POST'])
def delete_crime():
    if request.method == 'POST':
        crime_id = request.form['crime_id']
        deleter = DeleteCrime(db_config)
        cursor = None
        try:
            connection = deleter.db.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM reports WHERE id = %s", (crime_id,))
                connection.commit()
                cursor.close()
                deleter.db.close()
                return redirect(url_for('view_crime_reports'))
        except Exception as e:
            if cursor:
                cursor.close()
            deleter.db.close()
            print(f"Error: {e}")
    return render_template('delete_crime.html')

@app.route('/view_summary_by_location')
def view_summary_by_location():
    summary_viewer = ViewSummaryByLocation(db_config)
    cursor = None
    summary = []
    try:
        connection = summary_viewer.db.connect()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT location, COUNT(*) AS count FROM reports GROUP BY location")
            summary = cursor.fetchall()
            cursor.close()
            summary_viewer.db.close()
    except Exception as e:
        if cursor:
            cursor.close()
        summary_viewer.db.close()
        print(f"Error: {e}")
    return render_template('view_summary_by_location.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
