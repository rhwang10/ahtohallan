import requests
import os
from requests.auth import HTTPBasicAuth
from app.services.requests import AsyncNLUService


class WatsonNLUService(AsyncNLUService):

    def __init__(self):
        endpoint = os.environ.get("IBM_NLU_ENDPOINT")
        self.key = os.environ.get("IBM_NLU_API_KEY")
        super().__init__(endpoint)

    async def getSentiment(self, text):

        data = {
            "text": text
        }

        request = self._asyncCallable(requests.post,
                                      data,
                                      HTTPBasicAuth("apikey", self.key),
                                      withEmotion=True,
                                      withSentiment=True)

        try:
            resp = await self._call(request)
            return resp
        except Exception as err:
            raise Exception(err)
