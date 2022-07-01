# pydis
Based on python's dict bottom layer, it implements management similar to redis interface

## Usage
```python3
from pydis import Pydis
manager = Pydis()

# simple use
manager.set("key1", "value1")
manager.get("key1")

# ttl use
manager.set("key2", "value2", timeout=10)
print(manager.ttl("key2"))
# wait 10 seconds
manager.get("key2") # return None, because key2 already expired

# incr  decr 
manager.set("key3", 0)
manager.incr("key3")
manager.incr("key3")
manager.incr("key3")
print(manager.get("key3"))  # 3

manager.decr("key3")

print(manager.get("key3"))  # 2

# keys
manager = Pydis()
manager.set("key1", "value1")
print(list(manager.keys()))  # ["keys"]

```