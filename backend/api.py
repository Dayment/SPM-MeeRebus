from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from supabase import create_client, Client
import os
import traceback


app=Flask(__name__)
CORS(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = "https://xysbrhskuhqgthgxeiac.supabase.co"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.xysbrhskuhqgthgxeiac:@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# url = os.environ.get("postgresql://postgres.xysbrhskuhqgthgxeiac:@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres")
url = "https://xysbrhskuhqgthgxeiac.supabase.co"
# key = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5c2aJyaHNrdWhxZ3RoZ3hlaWFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU3OTA1MzgsImV4cCI6MjA0MTM2NjUzOH0.P9Jd12v5yeOTeDltRs-_x-HlXN0ml4YS1N7NWY1WAwk")
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5c2JyaHNrdWhxZ3RoZ3hlaWFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU3OTA1MzgsImV4cCI6MjA0MTM2NjUzOH0.P9Jd12v5yeOTeDltRs-_x-HlXN0ml4YS1N7NWY1WAwk"
supabase = create_client(url, key)
class employee(db.Model):
    __tablename__ = 'employee'  
    staff_id = db.Column(db.Integer, primary_key=True)
    staff_fname = db.Column(db.String(50), nullable=False)
    staff_lname = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    reporting_manager = db.Column(db.Integer, db.ForeignKey('employee.staff_id'))
    role = db.Column(db.Integer, nullable=False)


# Get specific employee
@app.route('/employee/<int:staff_id>', methods=['GET'])
def get_employee(staff_id):
    response = supabase.table('employee').select('*').eq('staff_id', staff_id).eq('country', 'Singapore').execute()
    
    if response.data:
        # Return first employee found, should be the only employee anyways since staff_id is primary key
        return jsonify(response.data[0]), 200  
    else:
        return jsonify({"error": "Employee not found or not authorized to log in from this location."}), 404

# Get all employees
@app.route('/employee', methods=['GET'])
def get_all_employees():
    # Query Supabase to fetch all employees
    response = supabase.table('employee').select('*').eq('country', 'Singapore').execute()
    
    if response.data:
        # Return all employee data
        return jsonify(response.data), 200  
    else:
        return jsonify({"error": "No employees found"}), 404

# Get all unique departments
@app.route('/departments', methods=['GET'])
def get_unique_departments():
    try:
        # Query Supabase to get distinct department names
        response = supabase.table('employee').select('dept').execute()

        if response.data:
            # Extract unique department names
            departments = {employee['dept'] for employee in response.data if employee.get('dept')}  # Use a set for uniqueness
            return jsonify(list(departments)), 200
        else:
            return jsonify({"error": "No departments found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/event-dates', methods=['GET'])
def get_unique_event_dates():
    try:
        # Query Supabase to get distinct event dates and their descriptions
        response = supabase.table('events').select('date, description').execute()

        if response.data:
            # Create a dictionary mapping event date to event description
            event_dates_dict = {event['date']: event['description'] for event in response.data if event.get('date') and event.get('description')}
            return jsonify(event_dates_dict), 200
        else:
            return jsonify({"error": "No event dates found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/all-events-datetimes', methods=['GET'])
def get_all_event_datetimes():
    try:
        # Query Supabase to get the event dates (assuming the column name is 'date')
        response = supabase.table('events').select('date').execute()

        # Debugging: Print the response to verify what is being returned
        print(response.data)

        if response.data:
            # Extract all event dates, ensuring we only include non-null dates
            event_dates = [event.get('date') for event in response.data if event.get('date')]
            
            # If the event_dates list is populated, return it, otherwise return a "not found" message
            if event_dates:
                return jsonify(event_dates), 200
            else:
                return jsonify({"error": "No valid event dates found"}), 404
        else:
            return jsonify({"error": "No events found"}), 404
    except Exception as e:
        # Log the error for further debugging
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/create-event', methods=['POST'])
def create_event():
    try:
        # Parse the JSON data from the request body
        event_data = request.json

        # Extract fields
        date = event_data.get('date')
        empID = event_data.get('empId')  # This corresponds to employee_Staff_ID
        creatorID = event_data.get('creator')  # The creator of the event

        # Validate input (check if 'date', 'empID', and 'creatorID' are provided)
        if not date or not empID or not creatorID:
            return jsonify({"error": "Missing date, empId, or creator"}), 400

        # Debugging logs for incoming data
        print(f"Received event data: {event_data}")

        # Ensure the Supabase client is initialized correctly
        if 'supabase' not in globals():
            raise Exception("Supabase client not initialized")

        # Step 1: Insert the event into the 'events' table
        event_response = supabase.table('events').insert({
            'date': date
        }).execute()

        # Check if the event was successfully inserted
        if event_response.data:
            # Retrieve the generated event_id
            event_id = event_response.data[0]['event_id']
            print(f"Event created with ID: {event_id}")

            # Step 2: Insert into the 'employee_has_events' table
            junction_response = supabase.table('employee_has_events').insert({
                'employee_staff_id': empID,  # employee ID
                'events_event_id': event_id,  # The newly created event ID
                'creator': creatorID  # The creator ID
            }).execute()

            # Check if the junction table insertion was successful
            if junction_response.data:
                return jsonify({"success": True, "event_id": event_id}), 200
            else:
                # Log the error if something goes wrong while inserting into the junction table
                error_message = junction_response.error or 'Unknown error while inserting into employee_has_events'
                print(f"Error inserting into employee_has_events: {error_message}")
                return jsonify({"success": False, "error": error_message}), 500
        else:
            # Log the error if the event insertion fails
            error_message = event_response.error or 'Unknown error while inserting event'
            print(f"Error inserting event: {error_message}")
            return jsonify({"success": False, "error": error_message}), 500

    except Exception as e:
        # Log the full traceback for debugging
        error_trace = traceback.format_exc()
        print(f"Error: {str(e)}\nTraceback: {error_trace}")
        return jsonify({"success": False, "error": str(e), "traceback": error_trace}), 500
    
class arrangement(db.Model):
    __tablename__ = 'arrangement'  
    arrangement_id = db.Column(db.Integer, primary_key=True) # Auto incrementing, no need to manually key in
    staff_id = db.Column(db.Integer, db.ForeignKey('employee.staff_id'), nullable=False)
    reporting_manager = db.Column(db.Integer, db.ForeignKey('employee.staff_id'), nullable=False)
    time = db.Column(db.Integer, nullable=False)  # 1 = AM, 2 = PM, 3 = Whole Day
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False)  # 0 = Pending, 1 = Accepted, 2 = Rejected
    reason = db.Column(db.String(255), nullable=True)  # Reason for rejection 


# Get specific arrangement by arrangement_id
@app.route('/arrangement/<int:arrangement_id>', methods=['GET'])
def get_arrangement(arrangement_id):
    response = supabase.table('arrangement').select('*').eq('arrangement_id', arrangement_id).execute()
    
    if response.data:
        return jsonify(response.data[0]), 200  
    else:
        return jsonify({"error": "Arrangement not found"}), 404

# Get all arrangements
# Use for HR or whoever is supposed to see everything
@app.route('/arrangement', methods=['GET'])
def get_all_arrangements():
    response = supabase.table('arrangement').select('*').execute()
    
    if response.data:
        return jsonify(response.data), 200  
    else:
        return jsonify({"error": "No arrangements found"}), 404
    

# Get arrangement for specific employee
@app.route('/arrangement/emp/<int:staff_id>', methods=['GET'])
def get_employee_arrangement(staff_id):
    response = supabase.table('arrangement').select('*').eq('staff_id', staff_id).execute()
    if response.data:
        return jsonify(response.data), 200  
    else:
        return jsonify({"error": "No arrangements found"}), 404
    

# Get arrangment for employee's team
# @app.route('/arrangement/posi/<int:staff_id>', methods=['GET'])
# def get_arrangements_by_team(staff_id):
#     # Get department for the employee
#     employee_response = supabase.table('employee').select('position').eq('staff_id', staff_id).execute()
    
#     if not employee_response.data:
#         return jsonify({"error": "Employee not found"}), 404
    
#     posi = employee_response.data[0]['position']

#     # Get all the info for staff with that posiiton / department
#     position_staff_response = supabase.table('employee').select('staff_id').eq('position', posi).eq('country', 'Singapore').execute()
#     # print("-------------------------------------CHECK HERE-----------------------------------")
#     # print(position_staff_id)
#     # print(type(position_staff_id))

#     # Extract staff IDs into an array
#     staff_ids = [staff['staff_id'] for staff in position_staff_response.data]

#     # Get all arrangements for these staff IDs
#     arrangements_response = supabase.table('arrangement').select('*').in_('staff_id', staff_ids).execute()
#     # print("-------------------------------------CHECK HERE-----------------------------------")
#     # print(arrangements_response.data)

#     if arrangements_response.data:
#         return jsonify(arrangements_response.data), 200
#     else:
#         return jsonify({"error": "No arrangements found for this department"}), 404
    

@app.route('/arrangement/posi/<int:staff_id>', methods=['GET'])
def get_arrangements_by_position(staff_id):
    # Get employee details
    employee_response = supabase.table('employee').select('*').eq('staff_id', staff_id).execute()
    
    if not employee_response.data:
        return jsonify({"error": "Employee not found"}), 404
    
    # Get position
    employee_data = employee_response.data[0]
    position = employee_data['position']

    position_staff_response = supabase.table('employee').select('staff_id').eq('position', position).eq('country', 'Singapore').execute()
    # print("-------------------------------------CHECK HERE-----------------------------------")
    # print(position_staff_response)

    staff_ids = [staff['staff_id'] for staff in position_staff_response.data]

    # Get all arrangements for employees with the same position. This is team schedule
    arrangements_response = supabase.table('arrangement').select('*').in_('staff_id', staff_ids).execute()
    
    # print("-----------------------------------------------")
    # print(arrangements_response)

    if arrangements_response.data:
        output = []
        
        for arrangement in arrangements_response.data:
            # Get employee details for each arrangement
            arrangement_staff_response = supabase.table('employee').select('*').eq('staff_id', arrangement['staff_id']).execute()
            
            if arrangement_staff_response.data:
                staff_info = arrangement_staff_response.data[0]
                
                # Manually building, don't think the 1 liner version will cut it here
                output.append({
                    "arrangement_id": arrangement['arrangement_id'],
                    "date": arrangement['date'],
                    "employee": staff_info,
                    "reason": arrangement.get('reason'),
                    "reporting_manager": arrangement['reporting_manager'],
                    "staff_id": arrangement['staff_id'],
                    "status": arrangement['status'],
                    "time": arrangement['time']
                })
        
        return jsonify(output), 200
    else:
        return jsonify({"error": "No arrangements found for this position"}), 404
    

# Get arrangement for a whole department
@app.route('/arrangement/dept/<int:staff_id>', methods=['GET'])
def get_arrangements_by_department(staff_id):
    # Get employee details
    employee_response = supabase.table('employee').select('*').eq('staff_id', staff_id).execute()
    
    if not employee_response.data:
        return jsonify({"error": "Employee not found"}), 404
    
    # Get department
    employee_data = employee_response.data[0]
    department = employee_data['dept']

    department_staff_response = supabase.table('employee').select('staff_id').eq('dept', department).eq('country', 'Singapore').execute()
    # print("-------------------------------------CHECK HERE-----------------------------------")
    # print(department)

    staff_ids = [staff['staff_id'] for staff in department_staff_response.data]

    # Get all arrangements for employees with the same position. This is team schedule
    arrangements_response = supabase.table('arrangement').select('*').in_('staff_id', staff_ids).execute()
    
    print("-----------------------------------------------")
    print(arrangements_response.data)

    if arrangements_response.data:
        output = []
        
        for arrangement in arrangements_response.data:
            # Get employee details for each arrangement
            arrangement_staff_response = supabase.table('employee').select('*').eq('staff_id', arrangement['staff_id']).execute()
            
            if arrangement_staff_response.data:
                staff_info = arrangement_staff_response.data[0]
                
                # Manually building, don't think the 1 liner version will cut it here
                output.append({
                    "arrangement_id": arrangement['arrangement_id'],
                    "date": arrangement['date'],
                    "employee": staff_info,
                    "reason": arrangement.get('reason'),
                    "reporting_manager": arrangement['reporting_manager'],
                    "staff_id": arrangement['staff_id'],
                    "status": arrangement['status'],
                    "time": arrangement['time']
                })
        
        return jsonify(output), 200
    else:
        return jsonify({"error": "No arrangements found for this position"}), 404


# Get all pending and approved WFH arrangements
@app.route('/arrangement/approved', methods=['GET'])
def get_approved_arrangements():
    response = supabase.table('arrangement').select('*, employee!arrangement_staff_id_fkey(*)').in_('status', [0,1]).execute()
    
    if response.data:
        return jsonify(response.data), 200  
    else:
        return jsonify({"error": "No approved arrangements found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)