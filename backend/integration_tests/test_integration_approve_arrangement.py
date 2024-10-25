# import unittest
# from unittest.mock import patch, MagicMock
# from api import create_app, db

# class ApproveArrangementIntegrationTest(unittest.TestCase):
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

#     def test_approve_arrangement_success(self):
#         arrangement_id = 1
#         # Mock arrangement data response from Supabase
#         mock_arrangement_data = {
#             "arrangement_id": arrangement_id,
#             "staff_id": 150065,
#             "status": 0  # Initially pending
#         }
#         self.mock_supabase.table('arrangement').select().eq().single().execute.return_value = MagicMock(data=mock_arrangement_data)
#         self.mock_supabase.table('arrangement').update().eq().execute.return_value = MagicMock(data={"status": 1})

#         # Mock employee data response for email notification
#         mock_employee_data = {
#             "email": "employee@example.com",
#             "staff_fname": "Noah"
#         }
#         self.mock_supabase.table('employee').select().eq().single().execute.return_value = MagicMock(data=mock_employee_data)

#         with patch('flask_mail.Mail.send') as mock_send:
#             response = self.client.put(f'/arrangement/approve/{arrangement_id}')
#             self.assertEqual(response.status_code, 200)
#             self.assertIn('message', response.json)
#             self.assertEqual(response.json['message'], "Arrangement approved successfully.")
#             mock_send.assert_called_once()  # Ensure email notification is sent

# if __name__ == '__main__':
#     unittest.main()