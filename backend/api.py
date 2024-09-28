from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from supabase import create_client, Client
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)