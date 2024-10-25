import unittest
from unittest.mock import patch, MagicMock
from api import create_app, db  

class EmployeeTestCase(unittest.TestCase):
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

    def test_get_employee_success(self):
        # Mock Supabase response for a found employee
        mock_data = [{
            "staff_id": 150065,
            "staff_fname": "Noah",
            "staff_lname": "Goh",
            "dept": "Engineering",
            "email": "noah.goh@company.com"
        }]
        self.mock_supabase.table().select().eq().eq().execute.return_value = MagicMock(data=mock_data)

        # Request the employee info
        response = self.client.get('/employee/150065')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['staff_fname'], "Noah")

    def test_get_employee_not_found(self):
        # Mock Supabase response for a not found employee
        self.mock_supabase.table().select().eq().eq().execute.return_value = MagicMock(data=[])

        # Request a non-existent employee
        response = self.client.get('/employee/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)
        self.assertEqual(response.json['error'], "Employee not found or not authorized to log in from this location.")

if __name__ == '__main__':
    unittest.main()
