import unittest
from unittest.mock import patch, MagicMock
from api import create_app, db

class CreateWFHRequestIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    def setUp(self):
        self.mock_supabase = patch('api.supabase').start()
        print("hi")

    def tearDown(self):
        patch.stopall()

    def test_create_wfh_request_success(self):
        # Mock Supabase response for employee data
        mock_employee_data = {
            "reporting_manager": 1001,
            "email": "noah.goh@company.com",
            "staff_fname": "Noah",
            "staff_lname": "Goh"
        }
        self.mock_supabase.table('employee').select().eq().single().execute.return_value = MagicMock(data=mock_employee_data)

        # WFH request data
        payload = {
            'staff_id': 150065,
            'date': '2024-12-01',
            'time': 'AM',
            'reason': 'Training',
            'requestType': 'Adhoc',
            'fileUrl': ''
        }

        response = self.client.post('/arrangement/submit', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], "WFH request submitted successfully and is now pending approval.")

if __name__ == '__main__':
    unittest.main()