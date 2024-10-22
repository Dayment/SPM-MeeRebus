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


        
    def test_get_employee_fail(self):
        self.mock_supabase.table().select().eq().eq().execute.return_value = MagicMock(data=None)
        response = self.client.get('/employee/150065')
        self.assertEqual(response.status_code, 404)


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


    def test_get_all_employees_fail(self):
        self.mock_supabase.table().select().eq().execute.return_value = MagicMock(data=None)
        response = self.client.get('/employee')
        self.assertEqual(response.status_code, 404)

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

    def test_get_arrangemen_fail(self):
        self.mock_supabase.table().select().eq().execute.return_value = MagicMock(data=None)
        response = self.client.get('/arrangement/1')
        self.assertEqual(response.status_code, 404)

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

    def test_get_all_arrangements_fail(self):
        self.mock_supabase.table().select().execute.return_value = MagicMock(data=None)
        response = self.client.get('/arrangement')
        self.assertEqual(response.status_code, 404)

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

    def test_get_employee_arrangement(self):
        self.mock_supabase.table().select().eq().execute.return_value = MagicMock(data=None)
        response = self.client.get('/arrangement/emp/1')
        self.assertEqual(response.status_code, 404)


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
        self.mock_supabase.table().select().eq().execute.return_value = MagicMock(data=mock_data)
        response = self.client.get('/arrangement/emp/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_data)

    def test_get_approved_arrangements(self):
        mock_data = [{'arrangement_id': 1, 'status': 1}, {'arrangement_id': 2, 'status': 0}]
        self.mock_supabase.table().select().in_().execute.return_value = MagicMock(data=mock_data)
        response = self.client.get('/arrangement/approved')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), mock_data)

    # def test_cancel_arrangement_success(self):
    #     arrangement_id = 1
    #     mock_arrangement_data = {
    #         "arrangement_id": arrangement_id,
    #         "status": 1  
    #     }
    #     # This is basically arrangement_response
    #     # Mock the Supabase response for fetching the arrangement
    #     self.mock_supabase.table().select().eq().single().execute.return_value = MagicMock(data=mock_arrangement_data)
        
    #     # Mock the Supabase response for updating the arrangement status
    #     self.mock_supabase.table().update().eq().execute.return_value = MagicMock(data={"status": 3})

    #     response = self.client.put(f'/arrangement/cancel/{arrangement_id}')
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(json.loads(response.data), {"message": "Arrangement cancelled successfully."})

    def test_cancel_arrangement_failure(self):
        arrangement_id = 1
        
        mock_arrangement_data = {
            "arrangement_id": arrangement_id,
            "status": 3
        }
        
        self.mock_supabase.table().select().eq().single().execute.return_value = MagicMock(data=mock_arrangement_data)
        self.mock_supabase.table().update().eq().execute.return_value = MagicMock(data=None)

        response = self.client.put(f'/arrangement/cancel/{arrangement_id}')
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.data), {"error": "Failed to cancel the arrangement."})
        

    def test_cancel_arrangement_not_found(self):
        arrangement_id = 1000000000000000
        # Mock response for fetching a non-existing arrangement
        self.mock_supabase.table().select().eq().single().execute.return_value = MagicMock(data=None)

        response = self.client.put(f'/arrangement/cancel/{arrangement_id}')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {"error": "Arrangement not found."})


    def test_get_arrangement_for_dept(self):
        arrangement_id = 20

        self.mock_supabase.table().select().eq().single().execute.return_value = MagicMock(data=None)

        pass

    @patch('api.supabase')
    def test_get_unique_departments_success(self, mock_supabase):
        # Mock the Supabase client response for successful department retrieval
        mock_supabase.table().select().execute.return_value = MagicMock(
            data=[{'dept': 'Engineering'}, {'dept': 'HR'}, {'dept': 'Marketing'}]
        )
        
        # Simulate a GET request to /departments
        response = self.client.get('/departments')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct departments are in the response data
        self.assertIn(b'Engineering', response.data)
        self.assertIn(b'HR', response.data)
        self.assertIn(b'Marketing', response.data)

    @patch('api.supabase')
    def test_get_unique_departments_no_data(self, mock_supabase):
        # Mock the Supabase client response when no departments are found
        mock_supabase.table().select().execute.return_value = MagicMock(data=[])
        
        # Simulate a GET request to /departments
        response = self.client.get('/departments')
        
        # Assert that the status code is 404 Not Found
        self.assertEqual(response.status_code, 404)
        
        # Assert the proper error message is in the response
        self.assertIn(b'No departments found', response.data)

    @patch('api.supabase')
    def test_get_unique_departments_internal_error(self, mock_supabase):
        # Mock the Supabase client response to raise an exception
        mock_supabase.table().select().execute.side_effect = Exception('Internal Server Error')
        
        # Simulate a GET request to /departments
        response = self.client.get('/departments')
        
        # Assert that the status code is 500 Internal Server Error
        self.assertEqual(response.status_code, 500)
        
        # Assert the error message is in the response
        self.assertIn(b'Internal Server Error', response.data)

    @patch('api.supabase')
    def test_get_unique_event_dates_success(self, mock_supabase):
        # Mock the Supabase client response for successful event date retrieval
        mock_supabase.table().select().execute.return_value = MagicMock(
            data=[{'date': '2024-10-15', 'description': 'Annual Meeting', 'event_id': 1},
                  {'date': '2024-11-20', 'description': 'Team Workshop', 'event_id': 2}]
        )
        
        # Simulate a GET request to /event-dates
        response = self.client.get('/event-dates')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct event dates, descriptions, and event IDs are in the response data
        self.assertIn(b'2024-10-15', response.data)
        self.assertIn(b'Annual Meeting', response.data)
        self.assertIn(b'1', response.data)  # Event ID
        self.assertIn(b'2024-11-20', response.data)
        self.assertIn(b'Team Workshop', response.data)
        self.assertIn(b'2', response.data)  # Event ID

    @patch('api.supabase')
    def test_get_unique_event_dates_no_data(self, mock_supabase):
        # Mock the Supabase client response when no event dates are found
        mock_supabase.table().select().execute.return_value = MagicMock(data=[])
        
        # Simulate a GET request to /event-dates
        response = self.client.get('/event-dates')
        
        # Assert that the status code is 404 Not Found
        self.assertEqual(response.status_code, 404)
        
        # Assert the proper error message is in the response
        self.assertIn(b'No events found', response.data)  # Updated message to match actual API response
    
    @patch('api.supabase')
    def test_get_unique_event_dates_internal_error(self, mock_supabase):
        # Mock the Supabase client response to raise an exception
        mock_supabase.table().select().execute.side_effect = Exception('Internal Server Error')
        
        # Simulate a GET request to /event-dates
        response = self.client.get('/event-dates')
        
        # Assert that the status code is 500 Internal Server Error
        self.assertEqual(response.status_code, 500)
        
        # Assert the error message is in the response
        self.assertIn(b'Internal Server Error', response.data)


    @patch('api.supabase')
    def test_create_event_success(self, mock_supabase):
        # Mock successful event and junction table insertions
        mock_supabase.table().insert().execute.side_effect = [
            MagicMock(data=[{'event_id': 1}]),  # Event creation response
            MagicMock(data=[{'employee_staff_id': 1}])  # Employee-event junction table insertion response
        ]
        
        # Simulate a POST request to /create-event
        data = {
            'date': '2024-10-15T10:00:00',
            'empId': 1,
            'creator': 2
        }
        
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

    @patch('api.supabase')
    def test_create_event_missing_date(self, mock_supabase):
        data = {
            'empId': 1,
            'creator': 2
        }
        
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 400 due to missing date
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing date, empId, or creator', response.data)

    @patch('api.supabase')
    def test_create_event_missing_empid(self, mock_supabase):
        data = {
            'date': '2024-10-15T10:00:00',
            'creator': 2
        }
        
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 400 due to missing empId
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing date, empId, or creator', response.data)

    @patch('api.supabase')
    def test_create_event_missing_creator(self, mock_supabase):
        data = {
            'date': '2024-10-15T10:00:00',
            'empId': 1
        }
        
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 400 due to missing creator
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing date, empId, or creator', response.data)

    @patch('api.supabase')
    def test_create_event_insertion_fails(self, mock_supabase):
        # Mock the response to simulate event insertion failure
        mock_supabase.table().insert().execute.return_value = MagicMock(data=None, error='Event insertion failed')

        # Prepare the data for the POST request
        data = {
            'date': '2024-10-15T10:00:00',
            'empId': 1,
            'creator': 2
        }

# Send a POST request to the create-event endpoint
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 500 Internal Server Error
        self.assertEqual(response.status_code, 500)
        
        # Assert the error message "Unknown error while inserting event" is in the response
        self.assertIn(b'Event insertion failed', response.data)
        
    @patch('api.supabase')
    def test_create_event_junction_insertion_fails(self, mock_supabase):
        # Mock the event insertion success
        mock_supabase.table().insert().execute.side_effect = [
            MagicMock(data=[{'event_id': 1}]),  # Successful event insertion
            MagicMock(data=None, error='Junction insertion failed')  # Failed junction insertion
        ]

        # Prepare the data for the POST request
        data = {
            'date': '2024-10-15T10:00:00',
            'empId': 1,
            'creator': 2
        }

        # Send a POST request to the create-event endpoint
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 500 Internal Server Error
        self.assertEqual(response.status_code, 500)
        
        # Assert the error message "Unknown error while inserting into employee_has_events" is in the response
        self.assertIn(b'Junction insertion failed', response.data)        
        
    @patch('api.supabase')
    def test_create_event_raises_exception(self, mock_supabase):
        # Simulate an exception being raised during the event insertion
        mock_supabase.table().insert().execute.side_effect = Exception('Simulated Exception')

        # Prepare the data for the POST request
        data = {
            'date': '2024-10-15T10:00:00',
            'empId': 1,
            'creator': 2
        }

        # Send a POST request to the create-event endpoint
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 500 Internal Server Error
        self.assertEqual(response.status_code, 500)
        
        # Assert the response contains the simulated exception message
        self.assertIn(b'Simulated Exception', response.data)

        # Assert the response contains the traceback information
        self.assertIn(b'Traceback', response.data)

    @patch('api.supabase')
    def test_delete_event_success(self, mock_supabase):
        # Mock the response for deleting from the junction table and event table
        mock_supabase.table().delete().eq().execute.side_effect = [
            MagicMock(data=[{'employee_staff_id': 1}]),  # Mock deletion from employee_has_events
            MagicMock(data=[{'event_id': 1}])  # Mock deletion from events table
        ]
        
        # Simulate a POST request to /delete-event
        response = self.client.post('/delete-event', json={'eventId': 1})
        
        # Assert the response is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Event and its related records deleted successfully', response.data)

    @patch('api.supabase')
    def test_delete_event_missing_event_id(self, mock_supabase):
        # Simulate a POST request without eventId
        response = self.client.post('/delete-event', json={})
        
        # Assert the response is 400 Bad Request due to missing eventId
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Event ID is required', response.data)

    @patch('api.supabase')
    def test_delete_event_junction_table_fail(self, mock_supabase):
        # Mock the response where deletion from the junction table fails
        mock_supabase.table().delete().eq().execute.side_effect = [
            MagicMock(data=[]),  # No rows affected in employee_has_events
            MagicMock(data=[{'event_id': 1}])  # Deletion from events table still proceeds
        ]
        
        # Simulate a POST request to /delete-event
        response = self.client.post('/delete-event', json={'eventId': 1})
        
        # Assert the response is still 200 OK, because both deletions are performed, but warn about junction table
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Event and its related records deleted successfully', response.data)

    @patch('api.supabase')
    def test_delete_event_fail_on_event_table(self, mock_supabase):
        # Mock successful deletion from employee_has_events
        mock_supabase.table().delete().eq().execute.side_effect = [
            MagicMock(data=[{'employee_staff_id': 1}]),  # Success for junction table
            Exception('Simulated exception during event deletion')  # Trigger an exception for the event table
        ]
        
        # Simulate a POST request to /delete-event
        response = self.client.post('/delete-event', json={'eventId': 1})
        
        # Assert that the response is 500 Internal Server Error due to the exception
        self.assertEqual(response.status_code, 500)
        
        # Assert the exception message is in the response data
        self.assertIn(b'Simulated exception during event deletion', response.data)

if __name__ == '__main__':
    unittest.main()