import unittest
from unittest.mock import patch, MagicMock
from api import create_app, db  

class ArrangementTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    def setUp(self):
        # Start patching Supabase client
        self.mock_supabase = patch('api.supabase').start()

    def tearDown(self):
        # Stop patching after each test
        patch.stopall()

    def test_create_wfh_arrangement_success(self):
        # Mock Supabase response for employee data retrieval
        mock_employee_data = {
            'reporting_manager': 1001,
            'email': 'noah.goh@company.com',
            'staff_fname': 'Noah',
            'staff_lname': 'Goh'
        }
        self.mock_supabase.table().select().eq().single().execute.return_value = MagicMock(data=mock_employee_data)

        # Define payload for successful WFH request
        payload = {
            'staff_id': 150065,
            'date': '2024-12-01',
            'time': 'AM',
            'reason': 'Training',
            'requestType': 'Adhoc',
            'fileUrl': ''
        }

        # Make the request and check response
        response = self.client.post('/arrangement/submit', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], "WFH request submitted successfully and is now pending approval.")

    def test_create_wfh_arrangement_missing_fields(self):
        # Define payload with missing required fields
        payload = {'staff_id': 150065}

        # Make the request and check response for missing fields error
        response = self.client.post('/arrangement/submit', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "Missing required fields: staff_id, date, or time.")

if __name__ == '__main__':
    unittest.main()
