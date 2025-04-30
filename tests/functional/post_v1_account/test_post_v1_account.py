import allure
import pytest
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account

@allure.suite("Тесты на проверку метода POST v1/account")
@allure.sub_suite("Позитивные тесты")
class TestPostV1Account:
    @allure.title("Проверка регистрации нового пользователя")
    def test_post_v1_account(self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1Account.check_response_values(response)

@allure.suite("Тесты на проверку метода POST v1/account")
@allure.sub_suite("Негативные тесты")
@allure.title("Проверка регистрации нового пользователя c невалидными данными")
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
         account_helper.register_new_user(login=login, password=password, email=email,with_activate= False )
