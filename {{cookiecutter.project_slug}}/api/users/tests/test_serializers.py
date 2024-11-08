import pytest

from api.users.serializers import UserSerializer


@pytest.mark.django_db
def test_user_serializer_email_lowercase():
    """
    Test that the email is converted to lowercase in UserSerializer.
    """
    data = {"email": "TESTUSER@EXAMPLE.COM"}
    serializer = UserSerializer(data=data)
    
    # Validate the data
    assert serializer.is_valid()
    
    # Check that email is in lowercase after validation
    assert serializer.validated_data["email"] == "testuser@example.com"
