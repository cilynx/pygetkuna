import requests

from .recording import Recordings

class Camera:

    def __init__(self, dict):
        self._dict = dict

    @property
    def url(self):
        return self._dict['url'].rstrip('/')

    @property
    def serial_number(self):
        return self._dict['serial_number']

    @property
    def recordings(self):
        recording_url = f'{self.url}/recordings/'
        headers = {'Authorization': f"Token {self._dict['token']}"}
        response = requests.get(recording_url, headers=headers)
        data = response.json()
        data['token'] = self._dict['token']
        return Recordings(data)
