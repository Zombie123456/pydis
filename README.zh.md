# pydis

![[](./LICENSE)](https://img.shields.io/github/license/Zombie123456/pydis) ![PyPI-version](https://img.shields.io/pypi/v/pydictdis) ![Python-version](https://img.shields.io/badge/python-%3E%3D3.6-blue)

[English](./README.md) | 简体中文

基于 python 的字典实现了部分的 redis 接口

如果你想像 redis 一样管理内存，但是不想引入 redis 那么重的服务，就可以使用 pydis
开箱即用，不用依赖任何服务，python3.6+ 安装即可使用

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
