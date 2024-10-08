import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json

import api

class FlaskAPITestCase(unittest.TestCase):
    # Set up the Flask app ONCE. Reused during each test case, BUT DB is reset for each test case in setup(). Less overhead since not remaking Flask app each time
    # Some sort of issue happens when I have the Flask app and stuff made in setup
    @classmethod
    @patch('api.create_supabase_client')
    def setUpClass(cls, mock_create_supabase_client):
        cls.mock_supabase = MagicMock()
        mock_create_supabase_client.return_value = cls.mock_supabase
        
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        }
        
        cls.app = api.create_app(test_config)
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            api.db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            api.db.session.remove()
            api.db.drop_all()

    # Using to reset the DB
    def setUp(self):
        self.mock_supabase.reset_mock()

    def test_get_employee(self):
        mock_data = [{
                        "country": "Singapore",
                        "dept": "Engineering",
                        "email": "Noah.Goh@allinone.com.sg",
                        "position": "Senior Engineers",
                        "reporting_manager": 151408,
                        "role": 2,
                        "staff_fname": "Noah",
                        "staff_id": 150065,
                        "staff_lname": "Goh"
                    }]
        self.mock_supabase.table().select().eq().eq().execute.return_value = MagicMock(data=mock_data)
        response = self.client.get('/employee/150065')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_data[0])

    def test_get_all_employees(self):
        mock_data = [ {
                        "country": "Singapore",
                        "dept": "CEO",
                        "email": "jack.sim@allinone.com.sg",
                        "position": "MD",
                        "reporting_manager": 130002,
                        "role": 1,
                        "staff_fname": "Jack",
                        "staff_id": 130002,
                        "staff_lname": "Sim"
                    },
                    {
                        "country": "Singapore",
                        "dept": "Sales",
                        "email": "Derek.Tan@allinone.com.sg",
                        "position": "Director",
                        "reporting_manager": 130002,
                        "role": 1,
                        "staff_fname": "Derek",
                        "staff_id": 140001,
                        "staff_lname": "Tan"
                    }]
        self.mock_supabase.table().select().eq().execute.return_value = MagicMock(data=mock_data)
        response = self.client.get('/employee')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_data)

    def test_get_arrangement(self):
        mock_data = [
                        {
                            "arrangement_id": 1,
                            "date": "2024-09-20T09:00:00",
                            "reason_man": "Don't like you",
                            "reason_staff": "Testing",
                            "reporting_manager": 210001,
                            "staff_id": 150065,
                            "status": 1,
                            "time": 1
                        }
                    ]
        self.mock_supabase.table().select().eq().execute.return_value = MagicMock(data=mock_data)
        response = self.client.get('/arrangement/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_data[0])

    def test_get_all_arrangements(self):
        mock_data = [   {
                            "arrangement_id": 1,
                            "date": "2024-09-20T09:00:00",
                            "reason_man": "Don't like you",
                            "reason_staff": "Testing",
                            "reporting_manager": 210001,
                            "staff_id": 150065,
                            "status": 1,
                            "time": 1
                        },                    
                        {
                            "arrangement_id": 2,
                            "date": "2024-09-21T14:00:00",
                            "reason_man": None,
                            "reason_staff": "Testing",
                            "reporting_manager": 210001,
                            "staff_id": 150075,
                            "status": 0,
                            "time": 2
                        }]
        self.mock_supabase.table().select().execute.return_value = MagicMock(data=mock_data)
        response = self.client.get('/arrangement')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_data)

    def test_get_employee_arrangement(self):
        mock_data = [{
                        "arrangement_id": 1,
                        "date": "2024-09-20T09:00:00",
                        "reason_man": None,
                        "reason_staff": "Testing",
                        "reporting_manager": 210001,
                        "staff_id": 150065,
                        "status": 1,
                        "time": 1
                    }]
        self.mock_supabase.table().select().eq().execute.return_value = MagicMock(data=mock_data[0])
        response = self.client.get('/arrangement/emp/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_data[0])

    def test_get_employee_arrangement_multi(self):
        mock_data = [    {
        "arrangement_id": 1,
        "date": "2024-09-20T09:00:00",
        "reason_man": None,
        "reason_staff": "Testing",
        "reporting_manager": 210001,
        "staff_id": 150065,
        "status": 1,
        "time": 1
    },
    {
        "arrangement_id": 10,
        "date": "2024-11-01T09:00:00",
        "reason_man": None,
        "reason_staff": "Just for testin",
        "reporting_manager": 210001,
        "staff_id": 150065,
        "status": 0,
        "time": 1
    },
                    ]
        self.mock_supabase.table().select().eq().execute.return_value = MagicMock(data=mock_data[0])
        response = self.client.get('/arrangement/emp/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_data[0])

    def test_get_approved_arrangements(self):
        mock_data = [{'arrangement_id': 1, 'status': 1}, {'arrangement_id': 2, 'status': 0}]
        self.mock_supabase.table().select().in_().execute.return_value = MagicMock(data=mock_data)
        response = self.client.get('/arrangement/approved')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_data)


if __name__ == '__main__':
    unittest.main()