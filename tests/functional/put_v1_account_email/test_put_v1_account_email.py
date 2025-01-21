from heplers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
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


def test_put_v1_account_email():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'golovan109'
    password = '112233'
    email = f'{login}@mail.ru'

    # Регистрация нового пользователя. Получение токена активации и активация пользователя

    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация пользователя
    account_helper.user_login(login=login, password=password)

    # Смена email пользователя

    json_data = {
        'login': login,
        'password': password,
        'email': f'ant{login}@mail.ru',
    }

    response = account_helper.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
    assert response.status_code == 200, f'Не успешная попытка изменить email {response.json()}'

    # Авторизация пользователя после смены адреса почты

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = account_helper.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, f'Пользователь не авторизован {response.json()}'

    # Получение письма из почтового сервиса

    response = account_helper.mailhog.mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, 'Письма не были получены'

    # Получение нового токена активации

    token = account_helper.get_activation_token_by_login(login=login, response=response)
    assert token is not None, f'Токен для пользователя {login} не был получен'

    # Активация пользователя по новому токену

    response = account_helper.dm_account_api.account_api.put_v1_account_token(token)
    assert response.status_code == 200, 'Пользователь не был активирован'

    # Авторизация

    account_helper.user_login(login=login, password=password)
