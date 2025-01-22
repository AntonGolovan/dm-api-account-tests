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

    login = 'golovan151'
    password = '112233'
    email = f'{login}@mail.ru'

    # Регистрация нового пользователя. Получение токена активации и активация пользователя

    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация пользователя
    account_helper.user_login(login=login, password=password)

    # Смена email пользователя

    account_helper.change_email_user(login=login, password=password, email=email)

    # Авторизация пользователя после смены адреса почты

    account_helper.verify_login_failure_for_email_change(login=login, password=password)

    # Получение нового токена активации из письма в почтовом сервисе

    token = account_helper.fetch_activation_token(login=login)

    # Активация пользователя по новому токену

    account_helper.activate_user(token=token)

    # Авторизация пользователя

    account_helper.user_login(login=login, password=password)