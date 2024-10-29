import unittest
from unittest.mock import patch, MagicMock
from api import create_app, db

class CreateEventIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    def setUp(self):
        self.mock_supabase = patch('api.supabase').start()

    def tearDown(self):
        patch.stopall()

    def test_create_event_success(self):
        # Test data
        event_data = {
            'date': '2024-12-01',
            'empId': '150065',
            'creator': '150065',
            'description': 'Team Building Event'
        }

        # Mock Supabase responses for event creation
        self.mock_supabase.table('events').insert().execute.return_value = MagicMock(
            data=[{'event_id': 1}]
        )
        
        self.mock_supabase.table('employee_has_events').insert().execute.return_value = MagicMock(
            data=[{'event_id': 1}]
        )

        # Make the request
        response = self.client.post('/create-event', json=event_data)
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['event_id'], 1)

    def test_create_event_missing_fields(self):
        # Test with missing required fields
        incomplete_data = {
            'date': '2024-12-01',
            # Missing empId and creator
            'description': 'Team Building Event'
        }

        response = self.client.post('/create-event', json=incomplete_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Missing date, empId, or creator')

if __name__ == '__main__':
    unittest.main()
