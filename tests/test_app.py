import unittest
from app import app
import os

os.environ["TESTING"] = "true"


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200

        html = response.get_data(as_text=True)
        assert "<title>Priya Hariharan</title>" in html

        # TODO Add more tests relating to index

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json

        json = response.get_json()
        assert len(json["timeline_posts"]) == 0

        # TODO Add more tests relating to GET and POST /api/timeline_post
        # TODO Add more tests relating to /timeline
