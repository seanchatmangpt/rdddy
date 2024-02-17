import pytest

from practice.lru_cache import LRUCache


def test_cache_hit():
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1, "Cache hit should return the correct value"


def test_cache_miss():
    lru = LRUCache(2)
    lru.put(1, 1)
    assert lru.get(3) is None, "Cache miss should return -1"


def test_capacity_limit():
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    lru.put(3, 3)  # This should evict key 1
    assert lru.get(1) == None, "Least recently used item should be evicted"


def test_update_existing_key():
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(1, 10)
    assert lru.get(1) == 10, "Updating an existing key should overwrite its value"


def test_recently_used_eviction_policy():
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    lru.get(1)  # This should make key 1 the most recently used
    lru.put(3, 3)  # This should evict key 2, not key 1
    assert (
        lru.get(2) == None and lru.get(1) == 1
    ), "LRU eviction policy should evict the least recently used item"


@pytest.mark.parametrize("key,value", [(4, 4), (5, 5)])
def test_put_with_parametrize(key, value):
    lru = LRUCache(3)
    lru.put(key, value)
    assert lru.get(key) == value, f"Cache should return {value} for key {key}"
