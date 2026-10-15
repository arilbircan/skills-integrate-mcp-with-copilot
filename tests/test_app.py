import unittest

from fastapi import HTTPException

from src.app import activities, signup_for_activity


class SignupCapacityTests(unittest.TestCase):
    def setUp(self):
        self.activity_name = "Chess Club"
        self.activity = activities[self.activity_name]
        self.original_participants = self.activity["participants"][:]
        self.original_max_participants = self.activity["max_participants"]

    def tearDown(self):
        self.activity["participants"] = self.original_participants
        self.activity["max_participants"] = self.original_max_participants

    def test_signup_succeeds_when_capacity_is_available(self):
        self.activity["max_participants"] = len(self.activity["participants"]) + 1

        result = signup_for_activity(self.activity_name, "student@mergington.edu")

        self.assertEqual(result["message"], "Signed up student@mergington.edu for Chess Club")
        self.assertIn("student@mergington.edu", self.activity["participants"])

    def test_signup_is_rejected_when_activity_is_full(self):
        self.activity["max_participants"] = len(self.activity["participants"])

        with self.assertRaises(HTTPException) as error:
            signup_for_activity(self.activity_name, "student@mergington.edu")

        self.assertEqual(error.exception.status_code, 400)
        self.assertEqual(error.exception.detail, "Activity is full")
        self.assertEqual(self.activity["participants"], self.original_participants)

    def test_signup_is_rejected_when_participants_exceed_capacity(self):
        self.activity["max_participants"] = len(self.activity["participants"]) - 1

        with self.assertRaises(HTTPException) as error:
            signup_for_activity(self.activity_name, "student@mergington.edu")

        self.assertEqual(error.exception.status_code, 400)
        self.assertEqual(error.exception.detail, "Activity is full")
        self.assertEqual(self.activity["participants"], self.original_participants)


if __name__ == "__main__":
    unittest.main()
