import unittest
import os

os.environ["TESTING"] = "true"

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200

        html = response.get_data(as_text=True)
        assert "<title>Priya Hariharan</title>" in html
        assert "Hey, I'm Priya Hariharan!" in html

    # def test_timeline(self):
    #     response = self.client.get("/api/timeline_post")
    #     assert response.status_code == 200
    #     assert response.is_json

    #     json = response.get_json()
    #     assert len(json["timeline_posts"]) == 0

    #     response = self.client.get("/timeline")
    #     assert response.status_code == 200
    #     html = response.get_data(as_text=True)

    #     assert "Create Post" in html
    #     assert "Timeline Posts" in html

    #     data = {
    #         "name": "John Doe",
    #         "email": "john@mail.com",
    #         "content": "Hello world, I'm John!",
    #     }
    #     response = self.client.post("/api/timeline_post", data=data)
    #     assert response.status_code == 200
    #     assert response.is_json

    #     response = self.client.get("/api/timeline_post")
    #     assert response.status_code == 200
    #     assert response.is_json

    #     json = response.get_json()
    #     assert len(json["timeline_posts"]) == 1

    # def test_malformed_timeline_post(self):
    #     response = self.client.post(
    #         "/api/timeline_post",
    #         data={"email": "john@example.com", "content": "Hello world, I'm John!"},
    #     )
    #     assert response.status_code == 400
    #     html = response.get_data(as_text=True)
    #     assert "Invalid name" in html

    #     response = self.client.post(
    #         "/api/timeline_post",
    #         data={
    #             "name": "John Doe",
    #             "email": "john@example.com",
    #         },
    #     )
    #     assert response.status_code == 400
    #     html = response.get_data(as_text=True)
    #     assert "Invalid content" in html

    #     response = self.client.post(
    #         "/api/timeline_post",
    #         data={
    #             "name": "John Doe",
    #             "content": "Hello world, I'm John!",
    #         },
    #     )
    #     assert response.status_code == 400
    #     html = response.get_data(as_text=True)
    #     assert "Invalid email" in html
