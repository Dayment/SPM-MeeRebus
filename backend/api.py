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
    response = supabase.table('employee').select('*').eq('staff_id', staff_id).execute()
    
    if response.data:
        # Return first employee found, should be the only employee anyways since staff_id is primary key
        return jsonify(response.data[0]), 200  
    else:
        return jsonify({"error": "Employee not found"}), 404

# Get all employees
@app.route('/employee', methods=['GET'])
def get_all_employees():
    # Query Supabase to fetch all employees
    response = supabase.table('employee').select('*').execute()
    
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
    
# Get all approved WFH arrangements
@app.route('/arrangement/approved', methods=['GET'])
def get_approved_arrangements():
    response = supabase.table('arrangement').select('*').gt('status', 0).execute()
    
    if response.data:
        return jsonify(response.data), 200  
    else:
        return jsonify({"error": "No approved arrangements found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)