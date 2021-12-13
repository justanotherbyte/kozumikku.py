from __future__ import annotations

from urllib.parse import urlencode as _urlencode
from typing import Optional, TYPE_CHECKING

from .http import HTTPClient, Route
from .image import ImageEndpoint, Image
from .genshin import GenshinCharacter

if TYPE_CHECKING:
    import aiohttp


class KozumikkuClient:
    def __init__(
        self,
        token: str,
        *,
        session: Optional[aiohttp.ClientSession] = None
    ):
        self.http = HTTPClient(token, session=session)
    
    # data endpoints
    async def random_joke(self) -> str:
        route = Route(
            "GET",
            "/data/joke"
        )
        response = await self.http.request(route)
        joke = response["joke"]
        return joke
    
    async def random_fact(self) -> str:
        route = Route(
            "GET",
            "/data/fact"
        )
        response = await self.http.request(route)
        fact = response["fact"]
        return fact
    
    # image endpoints
    async def image_endpoint(
        self,
        endpoint: ImageEndpoint,
        *,
        url: str
    ) -> Image:
        path = "/image/" + endpoint.endpoint

        parameters = {
            "url": url,
            **endpoint.options
        }

        encoded_parameters = _urlencode(parameters)

        route = Route(
            "GET",
            f"{path}?{encoded_parameters}"
        )

        data, response = await self.http.request(route, want_response=True)
        content_type = response.headers.get("Content-Type")
        image = Image(data, content_type)
        return image

    # genshin
    async def genshin_character(self, name: str) -> Optional[GenshinCharacter]:
        name = name.lower().strip()
        route = Route(
            "GET",
            "/genshin/character/{name}",
            name=name
        )

        data = await self.http.request(route)
        exists = data["exists"]

        if exists is False:
            return None

        character = GenshinCharacter(data)
        return character

    # cleanup
    async def close(self):
        await self.http.close()
