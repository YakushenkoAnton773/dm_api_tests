import os
from pathlib import Path
import time
from collections import namedtuple

import pytest
import structlog
from vyper import v
from datetime import datetime
from helpers.account_helper import AccountHelper
from packages.restclient.configuration import Configuration as MailhogConfiguration
from packages.restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from swagger_coverage_py.reporter import CoverageReporter

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
             # sort_keys=True
        )
    ]
)

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
    'telegram.chat_id',
    'telegram.token',
)


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host="http://5.63.153.31:5051")
    reporter.setup("/swagger/Account/swagger.json")
    yield
    reporter.generate_report()
    reporter.cleanup_input_files()


@pytest.fixture(scope="session", autouse=True)
def set_config(request):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))
    os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get("telegram.chat_id")
    os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get("telegram.token")
    request.config.stash['telegram-notifier-addfields']['environment'] = config_name
    request.config.stash['telegram-notifier-addfields']['report'] = "https://YakushenkoAnton773.github.io/dm_api_tests/"

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="stg", help="run stg")

    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)

@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get("service.mailhog"), disable_log=False)
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client

@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(
        host=v.get("service.dm_api_account"), disable_log=False
    )
    account = DMApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture(scope="session")
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture(scope="function")
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False
    )
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
        login=v.get("user.login"),
        password=v.get("user.password")

    )
    return account_helper

@pytest.fixture()
def prepare_user():
    time.sleep(1)
    now = datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f'henry12{data}'
    email = f'{login}@mail.ru'
    password = v.get("user.password")
    user = namedtuple("User", ["login", "password", "email"])
    user = user(login=login,password=password, email=email)
    return user