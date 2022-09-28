from unittest.mock import MagicMock

import pytest

from aioworkers_boto.storage import Storage

pytestmark = pytest.mark.asyncio


async def mocked_client_factory(data):
    resp = MagicMock()

    async def get_resp(**kwargs):
        return resp

    async def read():
        return data

    async def get_stream(*args, **kwargs):
        return MagicMock(read=read)

    client = MagicMock(
        get_object=get_resp,
        put_object=get_resp,
        delete_object=get_resp,
    )
    body = resp["Body"]
    body.__aenter__ = get_stream
    body.__aexit__ = get_stream
    return client


@pytest.mark.parametrize(
    "kw,data",
    [
        (dict(format='json'), {'a': 'b'}),
        (dict(bucket="b", path="p"), b"1234"),
        (dict(), "1234"),
    ],
)
async def test_set_get(mocker, kw, data):
    s3 = Storage(**kw)
    mocked_client = await mocked_client_factory(s3.encode(data))
    mocker.patch.object(s3, "_client", mocked_client)

    key = "1"
    await s3.set(key, data)
    d = await s3.get(key)
    await s3.set(key, None)
    assert d == data
