from ..models import UserManager


def test_missing_email_error_msg():
    """
    Tests UserManager creation error message with missing email
    """

    with pytest.raises(ValueError) as e_info:
        UserManager().create_user("")
    assert e_info.value.args[0] == "Users must have an email address"
