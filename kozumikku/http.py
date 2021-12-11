import sys
import json
import asyncio
import datetime
from typing import (
    Optional,
    Union,
    Tuple
)

import aiohttp

from . import __version__
from .errors import (
    HTTPException,
    Ratelimited,
    Forbidden,
    KozumikkuServerError,
    NotFound
)


class Route:
    BASE = "https://api.kozumikku.tech"
    def __init__(self, method: str, path: str, **kwargs):
        self.method = method
        self.path = path
        self.url = self.BASE + path.format(**kwargs)

async def parse_response(response: aiohttp.ClientResponse) -> Union[bytes, dict]:
    content = await response.read()
    data = None

    try:
        data = json.loads(content)
    except (
        json.JSONDecodeError,
        UnicodeDecodeError
    ):
        # if the parse into json failed
        # it means its an image endpoint 
        # where raw bytes are returned
        # we'll just return the raw bytes
        data = content
    
    return data

def _parse_ratelimit_information(response: aiohttp.ClientResponse) -> Tuple[Optional[int], Optional[datetime.datetime], bool]:
    headers = response.headers
    remaining = headers.get("X-Ratelimit-Remaining")
    reset = headers.get("X-Ratelimit-Reset")
    blocked = False

    if reset:
        # we've been blocked
        blocked = True
        dt = datetime.datetime.strptime(reset, "%Y-%m-%d %H:%M:%S.%f")
        reset = dt
    
    if remaining:
        remaining = int(remaining)

    return (remaining, reset, blocked)


class HTTPClient:
    """
    Represents a client sending requests
    to the Kozumikku API.
    """

    def __init__(self, token: str):
        self.__session: Optional[aiohttp.ClientSession] = None # filled in the first request

        user_agent = "HTTPClient (https://github.com/justanotherbyte/kozumikku.py {}) Python/{} aiohttp/{}"
        self.user_agent = user_agent.format(__version__, sys.version, aiohttp.__version__)
        self.token = token

    def _require_session(self):
        if self.__session is None or self.__session.closed is True:
            self.__session = aiohttp.ClientSession()

    async def request(self, route: Route, **kwargs) -> Union[bytes, dict]:
        method = route.method
        url = route.url

        # Headers creation
        headers = {
            "User-Agent": self.user_agent,
            "Authorization": self.token
        }
        kwargs["headers"] = headers

        self._require_session()

        async with self.__session.request(method, url, **kwargs) as resp:
            data = await parse_response(resp)

            _, _, blocked = _parse_ratelimit_information(resp)

            if blocked:
                raise Ratelimited(data, resp)

            if resp.ok:
                return data # everything is fine, return the json/bytes

            if resp.status >= 500:
                raise KozumikkuServerError(data, resp)
            elif resp.status == 403:
                raise Forbidden(data, resp)
            elif resp.status == 404:
                raise NotFound(data, resp)
            else:
                raise HTTPException(data, resp)
            

    async def close(self):
        if self.__session:
            await self.__session.close()
