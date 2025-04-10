import requests


class LoginApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.email = headers

    def post_v1_account_login(
            self,
            json_data
    ):
        response = requests.post(
            url=f'{self.host}/v1/account/login',
            json=json_data
        )
        return response
