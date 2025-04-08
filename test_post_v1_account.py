import requests


def test_post_v1_account():
    # Регистрация пользователя


    login = 'janmes'
    password = '12345678'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)


    # Получить письма из почтового сервера



    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params,  verify=False)
    print(response.status_code)
    print(response.text)
    # Получить активационный токен
    ...
    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://5.63.153.31:5051/v1/account/bbc94440-2a57-4ffc-bea7-17e3c3d8e508', headers=headers)
    print(response.status_code)
    print(response.text)
    # Авторизоваться

    json_data = {
        'login': 'janmes2',
        'password': '12345678',
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)