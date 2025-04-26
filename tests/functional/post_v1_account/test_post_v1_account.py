from datetime import datetime
import pytest
from checkers.http_ckeckers import check_status_code_http
from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to,
)



def test_post_v1_account(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    assert_that(
        response, all_of(
             has_property('resource', has_property('login', starts_with("henry"))),
             has_property('resource', has_property('registration', instance_of(datetime))),
             has_property(
                'resource', has_properties(
                    {
                        'rating': has_properties(

                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            )
        )
    )



@pytest.mark.parametrize(
    "login, email, password, error_message, expected_status_code",
    [
        # 1. Невалидный пароль
        ("valid_login", "validemail@example.com", "12345", "Validation failed", 400),

        # 2. Невалидный email
        ("valid_login", "invalidemail.com", "valid_password123", "Validation failed", 400),

        # 3. Невалидный логин
        ("k", "validemail@example.com", "valid_password123", "Validation failed", 400),
    ]
)
def test_post_v1_account_invalid_credentials(
        account_helper,
        login,
        email,
        password,
        error_message,
        expected_status_code
):
    with check_status_code_http(expected_status_code=expected_status_code, expected_message=error_message):
         account_helper.register_user_without_activate(login=login, password=password, email=email)