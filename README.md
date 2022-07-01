# pydis
Based on python's dict bottom layer, it implements management similar to redis interface

## Usage

params

- default_timeout : 全局的timeout，如果在设置key没有指定timeout的话，就会应用该timeout


### simple usage
```python3
from pydis import Pydis
manager = Pydis()

manager.set("key1", "value1")
manager.get("key1")
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

manager = Pydis()
manager.set("key1", "value1")
print(list(manager.keys()))  # ["keys"]
```