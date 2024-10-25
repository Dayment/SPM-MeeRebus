# import unittest
# from unittest.mock import patch, MagicMock
# from api import create_app, db

# class CancelArrangementIntegrationTest(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
#         cls.client = cls.app.test_client()
#         with cls.app.app_context():
#             db.create_all()

#     def setUp(self):
#         self.mock_supabase = patch('api.supabase').start()

#     def tearDown(self):
#         patch.stopall()

#     def test_cancel_arrangement_success(self):
#         arrangement_id = 1
#         # Mock the arrangement data for a valid cancellation
#         mock_arrangement_data = {
#             "arrangement_id": arrangement_id,
#             "staff_id": 150065,
#             "status": 0  # Pending or Approved before cancellation
#         }
#         self.mock_supabase.table('arrangement').select().eq().single().execute.return_value = MagicMock(data=mock_arrangement_data)
#         self.mock_supabase.table('arrangement').update().eq().execute.return_value = MagicMock(data={"status": 3})

#         # Mock employee data for email notification
#         mock_employee_data = {
#             "email": "employee@example.com",
#             "staff_fname": "Noah"
#         }
#         self.mock_supabase.table('employee').select().eq().single().execute.return_value = MagicMock(data=mock_employee_data)

#         with patch('flask_mail.Mail.send') as mock_send:
#             response = self.client.put(f'/arrangement/cancel/{arrangement_id}')
#             self.assertEqual(response.status_code, 200)
#             self.assertIn('message', response.json)
#             self.assertEqual(response.json['message'], "Arrangement cancelled successfully.")
#             mock_send.assert_called_once()  # Verify email notification is sent

# if __name__ == '__main__':
#     unittest.main()