import time

def test_change_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_email = f'new{int(time.time())}@test.com'
    account_helper.register_new_user(login=login,password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_email(login=login, password=password, new_email=new_email)

    # Пытаемся войти, получаем 403
    json_data = {
        'login': login,
        'password': password,
        'remember_me': True,
    }
    response = account_helper.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, "Пользователь авторизован"


    token = account_helper.get_activation_token_by_login(login=login)
    assert token is not None, f"Токен для пользователя {login} не был получен"
    # Активируем этот токен
    account_helper.activation_token(token=token)
    # Логинимся
    account_helper.user_login(login=login, password=password)