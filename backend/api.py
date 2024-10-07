from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from supabase import create_client, Client
from datetime import datetime, timedelta
import os


app=Flask(__name__)
CORS(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = "https://xysbrhskuhqgthgxeiac.supabase.co"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.xysbrhskuhqgthgxeiac:@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# url = os.environ.get("postgresql://postgres.xysbrhskuhqgthgxeiac:@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres")
url = "https://xysbrhskuhqgthgxeiac.supabase.co"
# key = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5c2JyaHNrdWhxZ3RoZ3hlaWFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU3OTA1MzgsImV4cCI6MjA0MTM2NjUzOH0.P9Jd12v5yeOTeDltRs-_x-HlXN0ml4YS1N7NWY1WAwk")
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

#note
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
# @app.route('/arrangement/approved', methods=['GET'])
# def get_approved_arrangements():
#     response = supabase.table('arrangement').select('*, employee!arrangement_staff_id_fkey(*)').in_('status', [0,1]).execute()
    
#     if response.data:
#         return jsonify(response.data), 200  
#     else:
#         return jsonify({"error": "No approved arrangements found"}), 404
    
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

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)