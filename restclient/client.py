
from requests import (session,JSONDecodeError)
import structlog
import uuid
import curlify

from restclient.configuration import Configuration


class RestClient:

     def __init__(
             self,
            configuration: Configuration
     ):
         self.host = configuration.host
         self.set_headers(configuration.headers)
         self.disable_log = configuration.disable_log
         self.session = session()
         self.log = structlog.getLogger(__name__).bind(service='api')


     def set_headers(self, headers):
         if headers:
             self.session.headers.update(headers)


     def post(
             self,
             path,
             **kwargs
     ):
         return self._send_request(method='POST', path=path, **kwargs)

     def get(
             self,
             path,
             **kwargs
     ):
         return self._send_request(method='GET', path=path, **kwargs)

     def put(
             self,
             path,
             **kwargs
     ):
         return self._send_request(method='PUT', path=path, **kwargs)

     def delete(
             self,
             path,
             **kwargs
     ):
         return self._send_request(method='DELETE', path=path, **kwargs)

     def _send_request(self, method, path, **kwargs):
         log = self.log.bind(event_id=str(uuid.uuid4()))
         full_url = self.host + path

         if self.disable_log:
             rest_responce = self.session.request(method=method, url=full_url, **kwargs)
             return rest_responce

         log.msg(
             event='Request',
             method=method,
             full_url=full_url,
             params=kwargs.get('params'),
             headers=kwargs.get('headers'),
             json=kwargs.get('json'),
             data=kwargs.get('data'),
         )
         rest_responce = self.session.request(method=method, url=full_url, **kwargs)

         curl= curlify.to_curl(rest_responce.request)
         print(curl)

         log.msg(
             event='Responce',
             status_code=rest_responce.status_code,
             headers=rest_responce.headers,
             json=self._get_json(rest_responce)
         )
         return rest_responce

     @staticmethod
     def _get_json(
             rest_responce
     ):
         try:
             return rest_responce.json()
         except JSONDecodeError:
             return {}
