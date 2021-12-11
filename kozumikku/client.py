from .http import HTTPClient, Route


class KozumikkuClient:
    def __init__(self, token: str):
        self.http = HTTPClient(token)

        # aliases
        self.computer_vision = self.cv

    # image endpoints
    async def image(
        self,
        endpoint: str,
        /,
        url: str,
        **kwargs
    ) -> bytes:
        """Request a /image/ endpoint.

        :param endpoint: A specific endpoint for the cv endpoint group. Example: flip
        :type endpoint: str
        :param url: The URL of the image you would like to request the endpoint with
        :type url: str
        :return: The manipulated image as raw bytes
        :rtype: bytes
        """

        endpoint = f"/image/{endpoint}?url={url}"
        # construct route
        route = Route(
            "GET", # image endpoints are always GET
            endpoint,
            **kwargs
        )

        image_bytes = await self.http.request(route)
        return image_bytes

    # computer vision endpoints
    async def cv(
        self,
        endpoint: str,
        /,
        url: str,
        **kwargs
    ) -> bytes:
        """Request a /cv/ endpoint.

        :param endpoint: A specific endpoint for the cv endpoint group. Example: edge-detect
        :type endpoint: str
        :param url: The URL of the image you would like to request the endpoint with
        :type url: str
        :return: The completed computer vision image as raw bytes
        :rtype: bytes
        """

        endpoint = f"/cv/{endpoint}?url={url}"
        # construct route
        route = Route(
            "GET", # CV endpoints are always GET
            endpoint,
            **kwargs
        )

        image_bytes = await self.http.request(route)
        return image_bytes

    # data endpoints
    async def data(
        self,
        endpoint: str,
        **kwargs
    ) -> dict:
        """Request a /data/ endpoint.

        :param endpoint: A specific endpoint for the data endpoint group. Example: joke
        :type endpoint: str
        :return: The JSON payload returned by the API
        :rtype: dict
        """

        endpoint = f"/data/{endpoint}"
        # construct route
        route = Route(
            "GET", # data endpoints are always GET
            endpoint,
            **kwargs
        )
        
        data = await self.http.request(route)
        return data

    async def close(self):
        await self.http.close()

    
