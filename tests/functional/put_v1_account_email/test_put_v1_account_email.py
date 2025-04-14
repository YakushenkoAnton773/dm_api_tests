from datetime import datetime
import structlog
from helpers.account_helper import AccountHelper
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
import time
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True)
    ]
)


def test_change_email():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025' )
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f'henry3{data}'
    email = f'{login}@mail.ru'
    password = '123456789'
    account_helper.register_new_user(login=login,password=password, email=email)
    account_helper.user_login(login=login, password=password)
    new_email = f'new{int(time.time())}@test.com'
    account_helper.change_email(login=login,password=password,new_email=new_email)
    # Попытка входа со старым email (должен быть 403)
    account_helper.forbidden_login(login=login,password=password)
    # Получение токена подтверждения нового email
    # Получить активационный токен
    # Активация нового email
    account_helper.activate_token(login=login)
    account_helper.user_login(login=login, password=password)
