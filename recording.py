import requests

class Recording:

    def __init__(self, dict):
        self._dict = dict

    @property
    def url(self):
        return self._dict['url']

    @property
    def id(self):
        return self._dict['id']

    @property
    def label(self):
        return self._dict['label']

    @property
    def camera(self):
        #TODO link this to the relevant Camera object
        return self._dict['camera']

    @property
    def description(self):
        return self._dict['description']

    @property
    def timestamp(self):
        return self._dict['timestamp']

    @property
    def duration(self):
        return self._dict['duration']

    @property
    def status(self):
        return self._dict['status']

    @property
    def m3u8(self):
        return self._dict['m3u8']

    @property
    def thumbnails(self):
        # TODO These are probably objects
        return self._dict['thumbnails']

    @property
    def classification(self):
        return self._dict['classification']

    @property
    def created_at(self):
        return self._dict['created_at']

    @property
    def updated_at(self):
        return self._dict['updated_at']

    @property
    def mp4(self):
        return self._dict['mp4']

    def download(self, filename=None):
        if filename is None:
            filename = f"{self.camera['serial_number']}-{self.label}.mp4"
        headers = {'Authorization': f"Token {self._dict['token']}"}
        response = requests.get(self.mp4, headers=headers, allow_redirects=True)
        open(filename, 'wb').write(response.content)

class Recordings:

    def __init__(self, dict):
        self._dict = dict

    def __iter__(self):
        return RecordingsIterator(self)


class RecordingsIterator:

    def __init__(self, page):
        self._page = page
        self._index = 0

    def __next__(self):
        if 'results' in self._page._dict.keys() and self._page._dict['results']:
            data = self._page._dict['results'].pop()
            data['token'] = self._page._dict['token']
            return Recording(data)
        elif 'next' in self._page._dict.keys() and self._page._dict['next']:
            headers = {'Authorization': f"Token {self._page._dict['token']}"}
            response = requests.get(self._page._dict['next'], headers=headers)
            data = response.json()
            data['token'] = self._page._dict['token']
            self._page._dict = data
            if 'results' in self._page._dict.keys() and self._page._dict['results']:
                data = self._page._dict['results'].pop()
                data['token'] = self._page._dict['token']
                return Recording(data)
        raise StopIteration
