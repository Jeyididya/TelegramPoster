import requests

from decouple import Config, RepositoryEnv
# config = Config()

import os
API_KEY = os.environ.get("CLI_API")
# = config('CLI_API')


class IMAGE:
    def __init__(self):
        self.api = ""

    def get_image(self, prompt):
        r = requests.post('https://clipdrop-api.co/text-to-image/v1',
                          files={
                              'prompt': (None, f'{prompt}', 'text/plain')
                          },
                          headers={'x-api-key': API_KEY}
                          )
        if (r.ok):
            image_bytes = r.content
            return image_bytes
        else:
            r.raise_for_status()
