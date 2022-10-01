# Aioworkers Boto

[![PyPI - Version](https://img.shields.io/pypi/v/aioworkers-boto.svg)](https://pypi.org/project/aioworkers-boto)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioworkers-boto.svg)](https://pypi.org/project/aioworkers-boto)

-----

**Table of Contents**

- [Installation](#installation)
- [Use](#use)
- [License](#license)

## Installation

```console
pip install aioworkers-boto
```

## Use

```yaml
s3:
  cls: aioworkers_boto.storage.Storage
  bucket: mybucket
  path: subdir/subsubdir
  connection:
    endpoint_url: https://...
    aws_secret_access_key: '&124323453456789'
    aws_access_key_id: key-id
    region_name: us-east-1
  format: json
```

```python
await context.s3.set(key, data)  # save data
d = await context.s3.get(key)  # get data
await context.s3.set(key, None)  # delete
```

## License

`aioworkers-boto` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
