from typing import Optional

from aiobotocore.client import AioBaseClient
from aiobotocore.session import AioSession, ClientCreatorContext
from aioworkers.core.base import AbstractConnector


class Connector(AbstractConnector):
    _client: Optional[AioBaseClient] = None
    _client_context: Optional[ClientCreatorContext] = None

    @property
    def client(self) -> AioBaseClient:
        assert self._client is not None
        return self._client

    async def connect(self):
        session = AioSession()
        service_name = self.config.get("service_name")
        cfg = self.config.get("connection") or {}
        self._client_context = session.create_client(service_name, **cfg)
        self._client = await self._client_context.__aenter__()

    async def disconnect(self):
        client_ctx = self._client_context
        if client_ctx is not None:
            await client_ctx.__aexit__(None, None, None)
            self._client = None
            self._client_context = None
