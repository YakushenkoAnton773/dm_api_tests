import allure

from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import RestClient


class LoginApi(RestClient):

    @allure.step("Авторизация пользователя")
    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials,
            validate_response=True
    ):
        """
        Authenticate via credentials
        :return:
        """
        response = self.post(
            path='/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True,by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Отправить запрос DELETE /v1/account/login")
    def delete_v1_account_login(
            self
    ):
        """
        Logout as current user
        :return:
        """
        response = self.delete(
            path='/v1/account/login'
        )
        return response

    @allure.step("Отправить запрос DELETE /v1/account/login/all")
    def delete_v1_account_login_all(
            self
    ):
        """
        Logout from every device
        :return:
        """
        response = self.delete(
            path='/v1/account/login/all'
        )
        return response