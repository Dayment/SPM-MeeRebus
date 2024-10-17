from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from supabase import create_client, Client
from datetime import datetime, timedelta
import os
import traceback
from dotenv import load_dotenv



db = SQLAlchemy()
supabase = None

def create_supabase_client():
    return create_client(os.getenv("URL"), os.getenv("KEY"))

def create_app(test_config=None):
    global supabase
    
    app = Flask(__name__)
    CORS(app)
    load_dotenv()

    if test_config is not None:
        app.config.update(test_config)
    elif app.config.get('TESTING'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("URI")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    if supabase is None:
        supabase = create_supabase_client()



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
            # Query Supabase to get event_id, date, and description fields
            response = supabase.table('events').select('event_id, date, description').execute()

            # Debugging: Print the response to verify what is being returned
            print(response.data)

            if response.data:
                # Create a dictionary with date as key and an array [description, event_id] as value
                event_data_dict = {
                    event.get('date'): [event.get('description'), event.get('event_id')]
                    for event in response.data
                    if event.get('event_id') and event.get('date') and event.get('description')  # Ensure non-null values
                }
                
                # If the event_data_dict is populated, return it, otherwise return a "not found" message
                if event_data_dict:
                    return jsonify(event_data_dict), 200
                else:
                    return jsonify({"error": "No valid event data found"}), 404
            else:
                return jsonify({"error": "No events found"}), 404
        except Exception as e:
            # Log the error for further debugging
            print(f"Error fetching event dates: {str(e)}")
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
            description = event_data.get('description')
            
            # Validate input (check if 'date', 'empID', and 'creatorID' are provided)
            if not date or not empID or not creatorID:
                return jsonify({"error": "Missing date, empId, or creator"}), 400

            # Debugging logs for incoming data
            print(f"Received event data: {event_data}")

            # Step 1: Insert the event into the 'events' table
            event_response = supabase.table('events').insert({
                'date': date,
                'description': description
                
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
                        "reason_staff": arrangement.get('reason_staff'),
                        "reason_man": arrangement.get('reason_man'),
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
                        "reason_staff": arrangement.get('reason_staff'),
                        "reason_man": arrangement.get('reason_man'),
                        "reporting_manager": arrangement['reporting_manager'],
                        "staff_id": arrangement['staff_id'],
                        "status": arrangement['status'],
                        "time": arrangement['time']
                    })
            
            return jsonify(output), 200
        else:
            return jsonify({"error": "No arrangements found for this position"}), 404


    # # Get all pending and approved WFH arrangements
    @app.route('/arrangement/approved', methods=['GET'])
    def get_approved_arrangements():
        response = supabase.table('arrangement').select('*, employee!arrangement_staff_id_fkey(*)').in_('status', [0,1]).execute()
        
        if response.data:
            return jsonify(response.data), 200  
        else:
            return jsonify({"error": "No approved arrangements found"}), 404
        
    # Get all WFH arrangemetns with employee obj
    @app.route('/arrangement/obj', methods=['GET'])
    def get_approved_arrangements_obj():
        response = supabase.table('arrangement').select('*').execute()

        staff_ids = [staff['staff_id'] for staff in response.data]
        arrangements_response = supabase.table('arrangement').select('*').in_('staff_id', staff_ids).execute()

        if arrangements_response.data:
            output = []
            
            for arrangement in arrangements_response.data:
                # Get employee details for each arrangement
                arrangement_staff_response = supabase.table('employee').select('*').eq('staff_id', arrangement['staff_id']).execute()
                
                if arrangement_staff_response.data:
                    staff_info = arrangement_staff_response.data[0]
                    
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
            return jsonify({"error": "No arrangements found"}), 404
        
    # Create WFH Request
    @app.route('/arrangement/submit', methods=['POST'])
    def create_WFH_request():
        try:
            data = request.json
            staff_id = data.get('staff_id')
            wfh_date = data.get('date') 
            wfh_time = data.get('time') 
            reason = data.get('reason')
            requestType = data.get('requestType')
            
            if not staff_id or not wfh_date or not wfh_time:
                return jsonify({"error": "Missing required fields: staff_id, date, or time."}), 400
            timestamp_hour = ""
            time = 0
            if wfh_time == 'AM':
                timestamp_hour = "09:00"
                time=1
            elif wfh_time=="Full Day":
                timestamp_hour = "09:00"
                time=3
            else:
                timestamp_hour = "14:00"
                time = 2
            
            #implement blocked days
            blocked_days = ['2024-12-25 00:00:00', '2024-01-01 00:00:00'] 

            wfh_date_obj = datetime.strptime(f"{wfh_date} {timestamp_hour}:00", "%Y-%m-%d %H:%M:%S")

            
            today = datetime.now()
            if wfh_date_obj < today:
                return jsonify({"error": "The selected date is in the past."}), 400
            
            if wfh_date_obj.strftime('%Y-%m-%d %H:%M:%S') in blocked_days:
                return jsonify({"error": "The selected day is blocked off by HR or management."}), 400
            
            # get employee reporting manager
            employee_data_res = supabase.table('employee').select('reporting_manager').eq('staff_id', staff_id).single().execute()
            if employee_data_res.data:
                reporting_manager = employee_data_res.data['reporting_manager']
            else:
                reporting_manager = None

            if requestType == "Recurring":
                recurrence_frequency = data.get("recurrenceFrequency")
                recurrence_end_date = data.get("recurrenceEndDate")

                if not recurrence_frequency or not recurrence_end_date:
                    return jsonify({"error": "For recurring request, please define frequency and end date."})
            
                recurrence_end_date_obj = datetime.strptime(f"{recurrence_end_date} 23:59:59", "%Y-%m-%d %H:%M:%S")

                recurring_dates = calculate_recurring(wfh_date_obj, recurrence_frequency, recurrence_end_date_obj)
                for date in recurring_dates:
                    result = supabase.table('arrangement').insert({
                    "staff_id": staff_id,
                    "reporting_manager": reporting_manager,  
                    "time": time,
                    "date": date.strftime('%Y-%m-%d %H:%M:%S'),  
                    "status": 0, 
                    "reason_staff":reason,
                    }).execute()
            elif requestType == "Adhoc":
                result = supabase.table('arrangement').insert({
                    "staff_id": staff_id,
                    "reporting_manager": reporting_manager,  
                    "time": time,
                    "date": wfh_date_obj.strftime('%Y-%m-%d %H:%M:%S'),  
                    "status": 0, 
                    "reason_staff":reason,
                    }).execute()

            return jsonify({"message": "WFH request submitted successfully and is now pending approval."}), 201
            

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Set arrangement status to 3 (Cancelled)
    @app.route('/arrangement/cancel/<int:arrangement_id>', methods=['PUT'])
    def cancel_arrangement(arrangement_id):
        try:
            # Get the arrangement by its ID
            arrangement_response = supabase.table('arrangement').select('*').eq('arrangement_id', arrangement_id).single().execute()

            if arrangement_response.data:
                # Update the status to 3 (Cancelled)
                update_response = supabase.table('arrangement').update({
                    "status": 3
                }).eq('arrangement_id', arrangement_id).execute()

                if update_response.data:
                    return jsonify({"message": "Arrangement cancelled successfully."}), 200
                else:
                    return jsonify({"error": "Failed to cancel the arrangement."}), 500
            else:
                return jsonify({"error": "Arrangement not found."}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/delete-event', methods=['POST'])
    def delete_event():
        try:
            # Get the JSON data from the request body
            data = request.json
            event_id = data.get('eventId')

            # Ensure that the event ID is provided
            if not event_id:
                return jsonify({'success': False, 'message': 'Event ID is required'}), 400

            # Log the event ID for debugging
            print(f"Attempting to delete event with ID: {event_id}")
            print('1')
            # Step 1: Delete the entry in the junction table (employee_has_events)
            junction_delete_response = supabase.table('employee_has_events').delete().eq('events_event_id', event_id).execute()
            print('2')
            # Check if the deletion in the junction table was successful
            print('3')
            # Step 2: Delete the event from the events table
            event_delete_response = supabase.table('events').delete().eq('event_id', event_id).execute()
            print('4')
            # Check if the event was successfully deleted

            # If both deletions are successful, return success message
            return jsonify({'success': True, 'message': 'Event and its related records deleted successfully'}), 200

        except Exception as e:
            # Return a 500 error if something goes wrong
            print(f"Exception occurred: {str(e)}")
            return jsonify({'success': False, 'message': str(e)}), 500 
           
    # Reset arrangement status from 3 to 0
    @app.route('/arrangement/test_scrum_8_reset_arrangement_status/<int:arrangement_id>', methods=['PUT'])
    def uncancel_arrangement(arrangement_id):
        try:
            # Get the arrangement by its ID
            arrangement_response = supabase.table('arrangement').select('*').eq('arrangement_id', arrangement_id).single().execute()

            if arrangement_response.data:
                # Update the status to 3 (Cancelled)
                update_response = supabase.table('arrangement').update({
                    "status": 0
                }).eq('arrangement_id', arrangement_id).execute()

                if update_response.data:
                    return jsonify({"message": "Arrangement uncancelled successfully."}), 200
                else:
                    return jsonify({"error": "Failed to uncancel the arrangement."}), 500
            else:
                return jsonify({"error": "Arrangement not found."}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

            
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


class arrangement(db.Model):
    __tablename__ = 'arrangement'  
    arrangement_id = db.Column(db.Integer, primary_key=True) # Auto incrementing, no need to manually key in
    staff_id = db.Column(db.Integer, db.ForeignKey('employee.staff_id'), nullable=False)
    reporting_manager = db.Column(db.Integer, db.ForeignKey('employee.staff_id'), nullable=False)
    time = db.Column(db.Integer, nullable=False)  # 1 = AM, 2 = PM, 3 = Whole Day
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False)  # 0 = Pending, 1 = Accepted, 2 = Rejected 3 = Cancelled
    reason_staff = db.Column(db.String(255), nullable=False) # Reason for applying
    reason_man = db.Column(db.String(255), nullable=True)  # Reason for rejection 

#functions
def calculate_recurring(start_date, recurrence_frequency, end_date):
    recurring_dates = []
    current_date = start_date
    while current_date <= end_date:
        recurring_dates.append(current_date)
        
        if recurrence_frequency == 'daily':
            current_date += timedelta(days=1)
        elif recurrence_frequency == 'weekly':
            current_date += timedelta(weeks=1)
        else:
            break  

    return recurring_dates

    

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)