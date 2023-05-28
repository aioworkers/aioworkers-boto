aioworkers-boto
===============

.. image:: https://img.shields.io/pypi/v/aioworkers-boto.svg
  :target: https://pypi.org/project/aioworkers-boto

.. image:: https://github.com/aioworkers/aioworkers-boto/workflows/Tests/badge.svg
  :target: https://github.com/aioworkers/aioworkers-boto/actions?query=workflow%3ATests

.. image:: https://codecov.io/gh/aioworkers/aioworkers-boto/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/aioworkers/aioworkers-boto

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json
  :target: https://github.com/charliermarsh/ruff

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://github.com/psf/black
  :alt: Code style: black

.. image:: https://img.shields.io/badge/types-Mypy-blue.svg
  :target: https://github.com/python/mypy

.. image:: https://readthedocs.org/projects/aioworkers-boto/badge/?version=latest
  :target: https://aioworkers-boto.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/aioworkers-boto.svg
  :target: https://pypi.org/project/aioworkers-boto

.. image:: https://img.shields.io/pypi/dm/aioworkers-boto.svg
  :target: https://pypi.org/project/aioworkers-boto

.. image:: https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg
  :alt: Hatch project
  :target: https://github.com/pypa/hatch

Use
---

.. code-block:: yaml

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


.. code-block:: python

    await context.s3.set(key, data)  # save data
    d = await context.s3.get(key)  # get data
    await context.s3.set(key, None)  # delete


Development
-----------

Check code:

.. code-block:: shell

    hatch run lint:all


Format code:

.. code-block:: shell

    hatch run lint:fmt


Run tests:

.. code-block:: shell

    hatch run pytest


Run tests with coverage:

.. code-block:: shell

    hatch run cov
