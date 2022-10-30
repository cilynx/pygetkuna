import requests

from .camera import Camera

api_url = "https://server.kunasystems.com/api/v1"

class Kuna:

    def __init__(self, email, password):

        auth_url = f'{api_url}/account/auth/'
        params = {'email': email, 'password': password}
        response = requests.post(auth_url, json=params)
        self._token = response.json()['token']

    @property
    def cameras(self):
        if hasattr(self, '_cameras'):
            return self._cameras
        cam_url = f'{api_url}/user/cameras/'
        headers = {'Authorization': f'Token {self._token}'}
        response = requests.get(cam_url, headers=headers)
        results = response.json()['results']
        cameras = []
        for result in results:
            result['token'] = self._token
            cameras.append(Camera(result))
        return cameras
