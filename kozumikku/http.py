import sys
import json
from typing import (
    Optional,
    Union,
    Tuple
)

import aiohttp

from . import __version__
from .errors import (
    KozumikkuServerError,
    Forbidden,
    NotFound,
    HTTPException,
    Ratelimited,
    Unauthorized
)


async def parse_response(resp: aiohttp.ClientResponse) -> Union[dict, bytes]:
    content = await resp.read()
    data = None

    try:
        data = json.loads(content)
    except (
        UnicodeDecodeError,
        json.JSONDecodeError
    ):
        data = content

    return data

class Route:
    BASE = "https://api.kozumikku.tech"
    def __init__(self, method: str, path: str, **parameters):
        self.method = method
        self.path = path.format(**parameters)
        self.raw_path = path
        self.url = self.BASE + self.path

class HTTPClient:
    def __init__(
        self,
        token: str,
        *,
        session: Optional[aiohttp.ClientSession] = None
    ):
        self.token = token
        user_agent = "HTTPClient (https://github.com/justanotherbyte/kozumikku.py {}) Python/{} aiohttp/{}"
        self.user_agent = user_agent.format(__version__, sys.version, aiohttp.__version__)

        self.__session = session # None or a valid aiohttp.ClientSession

    def _require_session(self) -> Optional[aiohttp.ClientSession]:
        if self.__session is None or self.__session.closed:
            session = aiohttp.ClientSession()
            self.__session = session
            return session
        
        return None

    async def request(self, route: Route, **kwargs) -> Union[Tuple[Union[bytes, dict], aiohttp.ClientResponse], Union[bytes, dict]]:
        method = route.method
        url = route.url
        want_response = kwargs.pop("want_response", False)

        headers = {
            "User-Agent": self.user_agent,
            "Authorization": self.token
        }
        kwargs["headers"] = headers

        self._require_session()

        async with self.__session.request(method, url, **kwargs) as resp:
            data = await parse_response(resp)

            if resp.ok:
                # everything is fine
                # just return the data
                if want_response:
                    return (data, resp)
                else:
                    return data

            if resp.status == 404:
                raise NotFound(data, resp)
            elif resp.status >= 500:
                raise KozumikkuServerError(data, resp)
            elif resp.status == 403:
                raise Forbidden(data, resp)
            elif resp.status == 429:
                raise Ratelimited(data, resp)
            elif resp.status == 401:
                raise Unauthorized(data, resp)
            else:
                # everything else
                raise HTTPException(data, resp)

    async def close(self):
        if self.__session and not self.__session.closed:
            await self.__session.close()
