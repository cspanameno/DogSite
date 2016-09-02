import json
from unittest import TestCase
from pet_model import User, Pet,UserPet, Breed, BreedPet, connect_to_db, db, example_data
from server import app
import server


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Welcome", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testpetsdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_register_form(self):
        """Test register page."""

        result = self.client.get("/register")
        self.assertIn("Register", result.data)


    def test_login_form(self):
        """Test login page."""

        result = self.client.get("/login")
        self.assertIn("email", result.data)


    # def test_login(self):
    #     """Test login page."""

    #     result = self.client.post("/login", 
    #                               data={"user_id": "cindy@gmail.com", "password": "baba123"},
    #                               follow_redirects=True)
    #     self.assertIn("You are a valued user", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    # def test_search_page(self):
    #     """Test search page."""

    #     result = self.client.get("/search_form")
    #     self.assertIn("Breed", result.data)

    # def test_favorites_page(self):
    #     """Test favorites page."""

    #     result = self.client.get("/search_form")
    #     self.assertIn("favorites", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    # def test_important_page(self):
    #     """Test that user can't see important page when logged out."""

    #     result = self.client.get("/important", follow_redirects=True)
    #     self.assertNotIn("You are a valued user", result.data)
    #     self.assertIn("You must be logged in", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
