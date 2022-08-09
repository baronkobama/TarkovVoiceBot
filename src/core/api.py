"""TarkovBot's HTTP File for interacting with the tarkov.dev API"""

# Built-in Modules

# External Dependencies
import aiohttp

# Local Modules
from src.core.utils import get_asyncio_event_loop

__all__ = (
    "TarkovDevAPI",
)


class RequestError(Exception):
    def __init__(self,
                 status: int,
                 reason: str = None
                 ):
        self.status = status
        self.reason = reason


class TarkovDevAPI:
    def __init__(self):
        self._session = aiohttp.ClientSession()

    def __exit__(self, exc_type: str, exc_val: str, exc_tb: str):
        loop = get_asyncio_event_loop()
        loop.run_until_complete(self._session.close())
        loop.close()

    async def request(self, data: str) -> dict:
        async with self._session.post(
            "https://api.tarkov.dev/graphql",
            json={"query": data},
        ) as response:
            if response.status != 200:
                raise RequestError(response.status, response.reason)
            return await response.json()

    async def get_item_info(self, item_name: str) -> dict:
        query = f"""
        {{
            items(name: "{item_name}") {{
                name
                updated
                iconLink
                avg24hPrice
                link
                changeLast48hPercent
            }}
        }}
        """
        requested = await self.request(query)
        return requested
