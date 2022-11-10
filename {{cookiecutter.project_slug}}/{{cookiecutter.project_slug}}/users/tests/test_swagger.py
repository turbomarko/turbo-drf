from django.urls import reverse


def test_swagger_accessible_by_admin(admin_client):
    url = reverse("api:api-docs")
    response = admin_client.get(url)
    assert response.status_code == 200


def test_api_schema_generated_successfully(admin_client):
    url = reverse("api:schema")
    response = admin_client.get(url)
    assert response.status_code == 200
