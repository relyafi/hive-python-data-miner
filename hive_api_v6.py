import requests

base_url = 'https://api-prod.bgchprod.info:443/omnia'
standard_headers = {
    'Content-Type' : 'application/vnd.alertme.zoo-6.1+json',
    'Accept' : 'application/vnd.alertme.zoo-6.1+json',
    'X-Omnia-Client': 'Hive Web Dashboard'
}

# Provides low-level operations for accessing the Hive v6 API. On construction, authenticates
# with the supplied user name / password to get a session id and uses this for subsequent
# operations.
class HiveAPIConnectionV6:
    def __init__(self, username: str, password: str):
        request = requests.post(
            f'{base_url}/auth/sessions',
            headers = standard_headers,
            json = {
                'sessions': [{
                    'username': username,
                    'password': password,
                    'caller': 'WEB'
                }]
            }
        )

        request.raise_for_status()

        self.__authenticated_headers = {
            **standard_headers,
            **{'X-Omnia-Access-Token': request.json().get('sessions')[0].get('sessionId')}
        }

    def get_channel_definitions(self):
        request = requests.get(
            f'{base_url}/channels',
            headers = self.__authenticated_headers
        )

        request.raise_for_status()
        return request.json()

    def get_channel_data(self,
                         channel_ids: list,
                         start_time: int,
                         end_time: int,
                         rate: int,
                         time_unit: str,
                         operation: str):

        channel_id_str = ','.join(channel_ids)

        request = requests.get(
            f'{base_url}/channels/{channel_id_str}',
            headers = self.__authenticated_headers,
            params = {
                'start': start_time,
                'end': end_time,
                'rate': rate,
                'timeUnit': time_unit,
                'operation': operation
            }
        )

        request.raise_for_status()
        return request.json()
