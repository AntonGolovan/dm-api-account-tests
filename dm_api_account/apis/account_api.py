from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient
from dm_api_account.models.registration import Registration

class AccountApi(RestClient):

    def post_v1_account(self, registration: Registration):
        """
         Register new user
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def post_v1_account_password(
            self,
            reset_password : ResetPassword,
            validate_response = True,
            **kwargs
    ):
        """
        Reset registered user password
        """
        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response = True,
            **kwargs
    ):
        """
        Change registered user password
        """
        response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response


    def get_v1_account(
            self,
            validate_response=True,
            **kwargs
    ):
        """
        Get current user
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        if validate_response:
           return UserDetailsEnvelope(**response.json())
        return response


    def put_v1_account_token(
            self,
            token,
            validate_response=True
    ):
        """
         Activate registered user
        """
        headers = {'accept': 'text/plain',}
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        if validate_response:
           return UserEnvelope(**response.json())
        return response


    def put_v1_account_email(
            self,
            change_email: ChangeEmail
    ):
        """
         Reset registered user email
        """
        response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def delete_v1_account_login(
            self,
            **kwargs
    ):
        """
        Logout as current user
        :return:
        """
        self.delete(
            path=f'/v1/account/login',
            **kwargs
        )


    def delete_v1_account_login_all(
            self,
            **kwargs
    ):
        """
        Logout from every device
        :return:
        """
        self.delete(
            path=f'/v1/account/login/all',
            **kwargs
        )