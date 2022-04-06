import os
import requests
import functools
import asyncio
import json

from datetime import date

class AsyncNLUService:

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.header = {'Content-Type': 'application/json'}

    def _asyncCallable(self,
                       func,
                       data,
                       auth,
                       language="en",
                       withEmotion=False,
                       withSentiment=False):
        data["features"] = {}

        if withEmotion:
            data["features"].update({"emotion": {}})

        if withSentiment:
            data["features"].update({"sentiment": {}})

        data["language"] = language

        return functools.partial(
            func,
            self.endpoint + date.today().strftime("%Y-%m-%d"),
            data=json.dumps(data),
            headers=self.header,
            auth=auth
        )

    async def _call(self, callable):
        loop = asyncio.get_event_loop()

        try:
            resp = await loop.run_in_executor(None, callable)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as err:
            raise Exception(err)
        except Exception as err:
            raise Exception(err)
