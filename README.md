# pydis

![[](./LICENSE)](https://img.shields.io/github/license/Zombie123456/pydis) ![PyPI-version](https://img.shields.io/pypi/v/pydictdis) ![Python-version](https://img.shields.io/badge/python-%3E%3D3.6-blue)

English | [简体中文](./README.zh.md)

Based on python's dict bottom layer, it implements management similar to redis interface

If you want to manage memory like redis, but don't want to introduce as many services as redis, you can use pydis,
Of course, pydis is completely implemented based on python's dict, and only has the basic functions of redis. Please evaluate this carefully before using it.

## install

```bash
pip install pydictdis
```

## Usage

### config

```python3
from pydis import Pydis

manager = Pydis()

manager.set_config("default_timeout", 50) # set default timeout is 50 seconds
```

### simple usage

```python3
from pydis import Pydis

manager = Pydis()

manager.set("key1", "value1")
manager.get("key1")  # value1

manager.delete("key1")
manager.get("key1")  # None
```

### ttl usage

```python3
from pydis import Pydis


manager = Pydis()
manager.set("key2", "value2", timeout=10)
print(manager.ttl("key2"))
# wait 10 seconds
manager.get("key2") # return None, because key2 already expired
```

### incr and decr usage

```python3
from pydis import Pydis


manager = Pydis()

manager.set("key3", 0)
manager.incr("key3")
manager.incr("key3")
manager.incr("key3")
print(manager.get("key3"))  # 3

manager.decr("key3")
print(manager.get("key3"))  # 2
```

### keys usage

```python3
from pydis import Pydis


manager = Pydis()

manager.set("key1", "value1")
print(list(manager.keys()))  # ["key1"]
```

### set_nx

```python3
from pydis import Pydis


manager = Pydis()

manager.set_nx('key1', 'value')
manager.set_nx('key1', 'value1')
manager.get('key1')  # value
```

### clean

```python3
from pydis import Pydis


manager = Pydis()

manager.set('key', 'value')
manager.set('key1', 'value1', timeout=1)
# after one seconds
manager.clean() # only have key in pydis, key1 already deleted

```

### force_clean

```python3
from pydis import Pydis


manager = Pydis()
manager.set('key', 'value')
manager.set('key1', 'value1', timeout=1)
manager.force_clean()  # will delete all key
```
