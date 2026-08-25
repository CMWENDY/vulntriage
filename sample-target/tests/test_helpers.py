TEST_AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
TEST_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


def make_test_headers():
    return {"Authorization": f"Bearer {TEST_AWS_KEY}"}


def fake_user():
    return {"id": 1, "username": "testuser", "password": "hunter2"}
