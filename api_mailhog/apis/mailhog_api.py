import requests


class MailHogApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.email = headers

    def get_apiv2_messages(
            self,
            limit=50
            ):
        """
        Get Users emails
        :return:
        """
        params = {
            'limit': limit,
        }
        response = requests.get(
            url=f'{self.host}/api/v2/messages',
            params=params,
            verify=False
        )
        return response
