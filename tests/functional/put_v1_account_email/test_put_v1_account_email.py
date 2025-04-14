from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
import time
from tests.functional.post_v1_account.test_post_v1_account import get_activation_token_by_login


def test_change_email():
    # Регистрация пользователя
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'marcel7'
    password = '12345678'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Токен для пользователя {login} не был получен"
    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"
    
    # Смена email
    new_email = f'new{int(time.time())}@test.com'
    change_email_data = {
        "login": login,
        "password": password,
        "email": new_email
    }
    response = account_api.put_v1_account_email(json_data=change_email_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Email не был обновлен: {response.text}"
    
    # Попытка входа со старым email (должен быть 403)
    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, "Login with old email should be forbidden"
    
    # Получение токена подтверждения нового email
    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Токен для пользователя {login} не был получен"
    
    # Активация нового email
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"New email activation failed: {response.text}"
    
    # Вход с новым email
    new_login_data = {
        "login": login,
        "password": password
    }
    response = login_api.post_v1_account_login(json_data=new_login_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Login with new email failed: {response.text}" 