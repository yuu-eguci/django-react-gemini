from unittest import mock

from django.test import SimpleTestCase


class FooViewTests(SimpleTestCase):
    def test_get(self):
        response = self.client.get("/api/app/foo")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "This endpoint is GET foo.")

    def test_post(self):
        response = self.client.post("/api/app/foo", {"value": "foo"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "This endpoint is POST foo.")

    def test_request_id_is_attached(self):
        request_id = self.client.get("/api/app/foo").json()["requestId"]
        self.assertRegex(request_id, r"^[0-9a-f]{8}$")


class BarViewTests(SimpleTestCase):
    def test_post(self):
        response = self.client.post("/api/app/bar", {"value": "bar"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "This endpoint is POST bar.")

    def test_get_returns_json_500_via_custom_exception_handler(self):
        with self.assertLogs("shared.exception_handlers", level="ERROR"):
            response = self.client.get("/api/app/bar")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"message": "Internal Server Error"})


class BazViewTests(SimpleTestCase):
    def test_post(self):
        with mock.patch("app.views.asyncio.sleep", new=mock.AsyncMock()) as sleep:
            response = self.client.post("/api/app/baz", {"value": "baz"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "This endpoint is POST baz for testing async view.")
        self.assertEqual(sleep.await_count, 3)


class CorsTests(SimpleTestCase):
    def test_react_dev_server_origin_is_allowed(self):
        response = self.client.get("/api/app/foo", headers={"Origin": "http://localhost:5001"})
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "http://localhost:5001")
