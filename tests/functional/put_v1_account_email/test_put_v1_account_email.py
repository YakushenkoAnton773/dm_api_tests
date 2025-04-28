import time

def test_put_v1_account_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_email = f'new{int(time.time())}@test.com'

    account_helper.user_login(login=login, password=password, validate_response=True)
    account_helper.change_email(login=login, password=password, new_email=new_email)

    account_helper.user_login(login=login, password=password, validate_headers=False)

    token = account_helper.get_activation_token_by_login(login=login)
    assert token is not None, f"Токен для пользователя {login} не был получен"
    # Активируем этот токен
    account_helper.activation_token(token=token)
    # Логинимся
    account_helper.user_login(login=login, password=password)