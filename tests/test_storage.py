from unittest.mock import MagicMock

import pytest
from aioworkers.core.config import ValueExtractor

from aioworkers_boto.storage import Storage


async def mocked_client_factory(data):
    resp = MagicMock()

    async def get_resp(**kwargs):
        return resp

    async def read():
        return data

    class AsyncContextManager:
        def __init__(self, *args):
            self._body = MagicMock(read=read)

        async def __aenter__(self):
            return self._body

        async def __aexit__(self, exc_type, exc, tb):
            pass

    client = MagicMock(
        get_object=get_resp,
        put_object=get_resp,
        delete_object=get_resp,
    )
    resp.__getitem__ = AsyncContextManager
    return client


@pytest.mark.parametrize(
    "kw,data",
    [
        (dict(format="json"), {"a": "b"}),
        (dict(path="p"), b"1234"),
        (dict(), "1234"),
    ],
)
async def test_set_get(mocker, kw, data):
    s3 = Storage(bucket="b", **kw)
    mocked_client = await mocked_client_factory(s3.encode(data))
    mocker.patch.object(s3, "_client", mocked_client)

    key = "1"
    await s3.set(key, data)
    d = await s3.get(key)
    await s3.set(key, None)
    assert d == data


async def test_set_get_bucket(mocker):
    s3 = Storage()
    bucket = "123"
    data = b"123"
    mocked_client = await mocked_client_factory(s3.encode(data))
    mocker.patch.object(s3, "_client", mocked_client)

    key = "1"
    await s3.set(key, data, bucket=bucket)
    d = await s3.get(key, bucket=bucket)
    await s3.set(key, None, bucket=bucket)
    assert d == data


async def test_empty_bucket_set():
    with pytest.raises(RuntimeError):
        await Storage().set("a", "")


async def test_empty_bucket_get():
    with pytest.raises(RuntimeError):
        await Storage().get("a")


@pytest.mark.parametrize(
    "path,key,result",
    [
        ("", "b", "b"),
        ("/a", "b", "/a/b"),
        ("a", "b", "a/b"),
        ("a/c", "b", "a/c/b"),
        ("a/c", "/b", "a/c/b"),
    ],
)
def test_raw_key(path, key, result):
    s = Storage(path=path)
    assert str(s.raw_key(key)) == result


@pytest.mark.parametrize(
    "path,key",
    [
        ("a/c", "../b"),
        ("a/b/c", "../b"),
    ],
)
def test_bad_key(path, key):
    s = Storage(path=path)
    with pytest.raises(ValueError):
        assert s.raw_key(key)


def test_set_cfg():
    s = Storage(path="a")
    assert s._path == "a/"
    s.set_config(ValueExtractor(dict(path="b", name="n")))
    assert s._path == "b/"
