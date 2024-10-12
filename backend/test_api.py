import unittest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.append(os.path.abspath('./backend'))
print(sys.path)  # Add this line to check the path is correct

from api import app  # Import the Flask app

class TestDepartmentsEndpoint(unittest.TestCase):
    
    def setUp(self):
        # Set up the test client for the Flask app
        self.client = app.test_client()
        self.client.testing = True

    @patch('app.supabase')
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

    @patch('app.supabase')
    def test_get_unique_departments_no_data(self, mock_supabase):
        # Mock the Supabase client response when no departments are found
        mock_supabase.table().select().execute.return_value = MagicMock(data=[])
        
        # Simulate a GET request to /departments
        response = self.client.get('/departments')
        
        # Assert that the status code is 404 Not Found
        self.assertEqual(response.status_code, 404)
        
        # Assert the proper error message is in the response
        self.assertIn(b'No departments found', response.data)

    @patch('app.supabase')
    def test_get_unique_departments_internal_error(self, mock_supabase):
        # Mock the Supabase client response to raise an exception
        mock_supabase.table().select().execute.side_effect = Exception('Internal Server Error')
        
        # Simulate a GET request to /departments
        response = self.client.get('/departments')
        
        # Assert that the status code is 500 Internal Server Error
        self.assertEqual(response.status_code, 500)
        
        # Assert the error message is in the response
        self.assertIn(b'Internal Server Error', response.data)


class TestEventDatesEndpoint(unittest.TestCase):
    
    def setUp(self):
        # Set up the test client for the Flask app
        self.client = app.test_client()
        self.client.testing = True

    @patch('app.supabase')
    def test_get_unique_event_dates_success(self, mock_supabase):
        # Mock the Supabase client response for successful event date retrieval
        mock_supabase.table().select().execute.return_value = MagicMock(
            data=[{'date': '2024-10-15', 'description': 'Annual Meeting'},
                  {'date': '2024-11-20', 'description': 'Team Workshop'}]
        )
        
        # Simulate a GET request to /event-dates
        response = self.client.get('/event-dates')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct event dates and descriptions are in the response data
        self.assertIn(b'2024-10-15', response.data)
        self.assertIn(b'Annual Meeting', response.data)
        self.assertIn(b'2024-11-20', response.data)
        self.assertIn(b'Team Workshop', response.data)

    @patch('app.supabase')
    def test_get_unique_event_dates_no_data(self, mock_supabase):
        # Mock the Supabase client response when no event dates are found
        mock_supabase.table().select().execute.return_value = MagicMock(data=[])
        
        # Simulate a GET request to /event-dates
        response = self.client.get('/event-dates')
        
        # Assert that the status code is 404 Not Found
        self.assertEqual(response.status_code, 404)
        
        # Assert the proper error message is in the response
        self.assertIn(b'No event dates found', response.data)

    @patch('app.supabase')
    def test_get_unique_event_dates_internal_error(self, mock_supabase):
        # Mock the Supabase client response to raise an exception
        mock_supabase.table().select().execute.side_effect = Exception('Internal Server Error')
        
        # Simulate a GET request to /event-dates
        response = self.client.get('/event-dates')
        
        # Assert that the status code is 500 Internal Server Error
        self.assertEqual(response.status_code, 500)
        
        # Assert the error message is in the response
        self.assertIn(b'Internal Server Error', response.data)

class TestAllEventsDatetimesEndpoint(unittest.TestCase):
    
    def setUp(self):
        # Set up the test client for the Flask app
        self.client = app.test_client()
        self.client.testing = True

    @patch('app.supabase')
    def test_get_all_event_datetimes_success(self, mock_supabase):
        # Mock the Supabase client response for successful event date retrieval
        mock_supabase.table().select().execute.return_value = MagicMock(
            data=[{'date': '2024-10-15T10:00:00'},
                  {'date': '2024-11-20T15:30:00'}]
        )
        
        # Simulate a GET request to /all-events-datetimes
        response = self.client.get('/all-events-datetimes')
        
        # Assert that the status code is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check that the correct event dates are in the response data
        self.assertIn(b'2024-10-15T10:00:00', response.data)
        self.assertIn(b'2024-11-20T15:30:00', response.data)

    @patch('app.supabase')
    def test_get_all_event_datetimes_no_valid_dates(self, mock_supabase):
        # Mock the Supabase client response with null or invalid event dates
        mock_supabase.table().select().execute.return_value = MagicMock(
            data=[{'date': None}, {'date': None}]
        )
        
        # Simulate a GET request to /all-events-datetimes
        response = self.client.get('/all-events-datetimes')
        
        # Assert that the status code is 404 Not Found because there are no valid dates
        self.assertEqual(response.status_code, 404)
        
        # Assert the proper error message is in the response
        self.assertIn(b'No valid event dates found', response.data)

    @patch('app.supabase')
    def test_get_all_event_datetimes_no_data(self, mock_supabase):
        # Mock the Supabase client response when no events are found
        mock_supabase.table().select().execute.return_value = MagicMock(data=[])
        
        # Simulate a GET request to /all-events-datetimes
        response = self.client.get('/all-events-datetimes')
        
        # Assert that the status code is 404 Not Found
        self.assertEqual(response.status_code, 404)
        
        # Assert the proper error message is in the response
        self.assertIn(b'No events found', response.data)

    @patch('app.supabase')
    def test_get_all_event_datetimes_internal_error(self, mock_supabase):
        # Mock the Supabase client response to raise an exception
        mock_supabase.table().select().execute.side_effect = Exception('Internal Server Error')
        
        # Simulate a GET request to /all-events-datetimes
        response = self.client.get('/all-events-datetimes')
        
        # Assert that the status code is 500 Internal Server Error
        self.assertEqual(response.status_code, 500)
        
        # Assert the error message is in the response
        self.assertIn(b'Internal Server Error', response.data)

class TestCreateEventEndpoint(unittest.TestCase):
    
    def setUp(self):
        # Set up the test client for the Flask app
        self.client = app.test_client()
        self.client.testing = True

    # Test Case 1: Successful event creation with all valid data
    @patch('app.supabase')
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
    
    # Test Case 2: Missing date field
    @patch('app.supabase')
    def test_create_event_missing_date(self, mock_supabase):
        data = {
            'empId': 1,
            'creator': 2
        }
        
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 400 due to missing date
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing date, empId, or creator', response.data)
    
    # Test Case 3: Missing empId field
    @patch('app.supabase')
    def test_create_event_missing_empid(self, mock_supabase):
        data = {
            'date': '2024-10-15T10:00:00',
            'creator': 2
        }
        
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 400 due to missing empId
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing date, empId, or creator', response.data)

    # Test Case 4: Missing creator field
    @patch('app.supabase')
    def test_create_event_missing_creator(self, mock_supabase):
        data = {
            'date': '2024-10-15T10:00:00',
            'empId': 1
        }
        
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 400 due to missing creator
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing date, empId, or creator', response.data)
    
    # Test Case 5: Supabase event creation fails
    @patch('app.supabase')
    def test_create_event_event_creation_fails(self, mock_supabase):
        # Mock event creation failure (no data returned)
        mock_supabase.table().insert().execute.side_effect = [
            MagicMock(data=None, error='Event creation failed')
        ]
        
        data = {
            'date': '2024-10-15T10:00:00',
            'empId': 1,
            'creator': 2
        }
        
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 500 due to event creation failure
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Unknown error while inserting event', response.data)

    # Test Case 6: Supabase junction table insertion fails
    @patch('app.supabase')
    def test_create_event_junction_insertion_fails(self, mock_supabase):
        # Mock successful event creation but failed junction table insertion
        mock_supabase.table().insert().execute.side_effect = [
            MagicMock(data=[{'event_id': 1}]),  # Event creation success
            MagicMock(data=None, error='Junction table insertion failed')  # Junction table failure
        ]
        
        data = {
            'date': '2024-10-15T10:00:00',
            'empId': 1,
            'creator': 2
        }
        
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 500 due to junction table insertion failure
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Unknown error while inserting into employee_has_events', response.data)

    # Test Case 7: Supabase client is not initialized
    @patch('app.supabase', None)
    def test_create_event_supabase_not_initialized(self):
        data = {
            'date': '2024-10-15T10:00:00',
            'empId': 1,
            'creator': 2
        }
        
        response = self.client.post('/create-event', json=data)
        
        # Assert the response is 500 due to uninitialized Supabase client
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Supabase client not initialized', response.data)
    
    # Test Case 8: Generic internal server error (unhandled exception)
    @patch('app.supabase')
    def test_create_event_generic_error(self, mock_supabase):
        # Mock an exception being raised
        mock_supabase.table().insert().execute.side_effect = Exception('Unexpected error')

        data = {
            'date': '2024-10-15T10:00:00',
            'empId': 1,
            'creator': 2
        }

        response = self.client.post('/create-event', json=data)

        # Assert the response is 500 due to generic error
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Unexpected error', response.data)



if __name__ == '__main__':
    unittest.main()