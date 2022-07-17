# pydis

![[](./LICENSE)](https://img.shields.io/github/license/Zombie123456/pydis) ![PyPI-version](https://img.shields.io/pypi/v/pydictdis) ![Python-version](https://img.shields.io/badge/python-%3E%3D3.6-blue)

[English](./README.md) | 简体中文

Based on python's dict bottom layer, it implements management similar to redis interface

If you want to manage memory like redis, but don't want to introduce as many services as redis, you can use pydis,
Of course, pydis is completely implemented based on python's dict, and only has the basic functions of redis. Please evaluate this carefully before using it.

## 安装

```bash
pip install pydictdis
```

## 用例

params

- default_timeout : 全局的 timeout，如果在设置 key 没有指定 timeout 的话，就会应用该 timeout

### 简单用例

```python3
from pydis import Pydis
manager = Pydis()

manager.set("key1", "value1")
manager.get("key1")  # value1

manager.delete("key1")
manager.get("key1")  # None
```

### ttl 用例

```python3
from pydis import Pydis
manager = Pydis()
manager.set("key2", "value2", timeout=10)
print(manager.ttl("key2"))
# wait 10 seconds
manager.get("key2") # return None, because key2 already expired
```

### incr 和 decr 用例

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

### keys 用例

```python3
from pydis import Pydis
manager = Pydis()

manager.set("key1", "value1")
print(list(manager.keys()))  # ["key1"]
```

### set_nx 用例

```python3
from pydis import Pydis
manager = Pydis()

manager.set_nx('key1', 'value')
manager.set_nx('key1', 'value1')
manager.get('key1')  # value
```
