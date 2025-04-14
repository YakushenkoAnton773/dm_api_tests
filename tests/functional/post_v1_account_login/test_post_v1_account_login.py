from datetime import datetime

from helpers.account_helper import AccountHelper

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True)
    ]
)

def test_post_v1_account_login():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025' )
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f'henry2{data}'
    email = f'{login}@mail.ru'
    password = '123456789'
    account_helper.register_new_user(login=login, email=email, password=password)
    account_helper.user_login(login=login, password=password)