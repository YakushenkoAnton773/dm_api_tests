import allure
from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from clients.http.dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import RestClient


class AccountApi(RestClient):

    @allure.step("Зарегистрировать нового пользователя")
    def post_v1_account(
            self,
            registration: Registration
    ):
        response = self.post(
            path='/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    @allure.step("Получить данные пользователя")
    def get_v1_account(
            self,
            validate_response: bool = True,
            **kwargs
    ):
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step("Активировать пользователя")
    def put_v1_account_token(
            self,
            token: str,
            validate_response: bool = True
    ):
        # для активации возвращается plain‑text, поэтому Accept=text/plain
        response = self.put(
            path=f'/v1/account/{token}',
            headers={'accept': 'text/plain'}
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Сбросить пароль зарегистрированного пользователя")
    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response: bool = True
    ):
        response = self.post(
            path='/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Сменить почту зарегистрированного пользователя")
    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            validate_response: bool = True
    ):
        response = self.put(
            path='/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Сменить пароль зарегистрированного пользователя")
    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response: bool = True
    ):
        response = self.put(
            path='/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response
