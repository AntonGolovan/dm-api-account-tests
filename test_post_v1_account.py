import requests
import pprint


def test_post_v1_account():
    # Регистрация пользователя

    login = 'golovan4'
    password = '112233'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)

    print(response.status_code)
    print(response.text)

    # Получить письмо из почтового сервиса

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)

    print(response.status_code)
    print(response.text)

    # Получить токен из почтового сервиса

    ...
    # Активация пользователя

    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://5.63.153.31:5051/v1/account/c7094bcc-6329-4c56-b372-94e2eac37f25', headers=headers)

    print(response.status_code)
    print(response.text)

    # Авторизация пользователя

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)

    print(response.status_code)
    print(response.text)
