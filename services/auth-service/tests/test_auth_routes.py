
def test_register_route(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "api@test.com",
            "password": "password123",
            "name": "API Test",
            "role": "staff",
            "department_id": "55555555-5555-5555-5555-555555555555"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "api@test.com"


def test_login_route(client):
    client.post(
        "/auth/register",
        json={
            "email": "api_login@test.com",
            "password": "password123",
            "name": "API Login",
            "role": "staff",
            "department_id": "66666666-6666-6666-6666-666666666666"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "api_login@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
