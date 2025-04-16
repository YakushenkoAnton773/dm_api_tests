import json
import time
from json import JSONDecodeError
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from retrying import retry

def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None

def retrier(
        function
):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f"Попытка получения токена номер {count}")
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток получения активационного токена!")
            if token:
                return token
            time.sleep(1)
    return wrapper

class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str,
    ):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={"login": login, "password": password}
        )
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, "Пользователь не был создан"

        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login} не был получен"
        response = self.activation_token(token=token)
        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "Пользователь не смог авторизоваться"
        return response

    def change_email(
            self,
            login: str,
            password: str,
            new_email: str,
    ):
        change_email_data = {
            "login": login,
            "password": password,
            "email": new_email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=change_email_data)
        assert response.status_code == 200, f"Email не был обновлен: {response.text}"

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        for item in response.json()['items']:
            try:
                user_data = json.loads(item['Content']['Body'])
            except (JSONDecodeError, KeyError):
                continue
            user_login = user_data.get('Login')
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                print(token)
        return token

    def activation_token(
            self,
            token
    ):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"
        return response