from json import (loads,JSONDecodeError)
import time

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)

def test_post_v1_account():
    # Регистрация пользователя
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')

    account_api= AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    login = 'golovan125'
    password = '112233'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)

    assert response.status_code == 201, f'Пользователь не создан {response.json()}'

    # Получить письмо из почтового сервиса

    response = mailhog_api.get_api_v2_messages()

    assert response.status_code == 200, 'Письма не были получены'
    time.sleep(1)

    # Получить токен из почтового сервиса
    token = get_activation_token_by_login(login=login, response=response)

    assert token is not None, f'Токен для пользователя {login} не был получен'

    # Активация пользователя

    response = account_api.put_v1_account_token(token=token)

    assert response.status_code == 200, 'Пользователь не был активирован'

    # Авторизация пользователя

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, 'Пользователь не был авторизован'


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        try:
            user_data = loads(item['Content']['Body'])
        except (JSONDecodeError, KeyError):
            print('Не верный формат')
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token
