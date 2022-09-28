from aioworkers.core.formatter import FormattedEntity
from aioworkers.storage.base import AbstractStorage

from aioworkers_boto.core import Connector


class Storage(AbstractStorage, FormattedEntity, Connector):
    def __init__(self, *args, **kwargs):
        kwargs["service_name"] = "s3"
        super().__init__(*args, **kwargs)

    def raw_key(self, key):
        path = self.config.get("path")
        if path:
            key = f"{path}/{key}"
        return key

    async def get(self, key):
        kwargs = {"Key": self.raw_key(key)}
        bucket = self.config.get("bucket")
        if bucket:
            kwargs["Bucket"] = bucket
        response = await self._client.get_object(**kwargs)
        async with response["Body"] as stream:
            return self.decode(await stream.read())

    async def set(self, key, value):
        kwargs = {"Key": self.raw_key(key)}
        bucket = self.config.get("bucket")
        if bucket:
            kwargs["Bucket"] = bucket
        if value is None:
            await self._client.delete_object(**kwargs)
        else:
            kwargs["Body"] = self.encode(value)
            await self._client.put_object(**kwargs)
