from unittest.mock import MagicMock

from aiobotocore.session import AioSession

from aioworkers_boto.core import Connector


def mocked_factory(*args, **kwargs):
    async def coro(*args, **kwargs):
        return mocked_factory()

    ctx = MagicMock(
        __aenter__=coro,
        __aexit__=coro,
    )
    return ctx


async def test_connector(mocker):
    c = Connector()
    mocker.patch.object(AioSession, "create_client", mocked_factory)
    await c.connect()
    assert c.client
    await c.disconnect()


async def test_disconnect(mocker):
    c = Connector()
    await c.disconnect()


async def test_async_contextmanager(mocker):
    mocker.patch.object(AioSession, "create_client", mocked_factory)
    c = Connector(endpoint_url="http://localhost/api/")
    async with c:
        assert c.client
