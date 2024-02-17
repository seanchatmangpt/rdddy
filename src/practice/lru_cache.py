class ListNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = ListNode()
        self.tail = ListNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def remove_node(self, node: ListNode):
        prev = node.prev
        nxt = node.next
        prev.next, nxt.prev = nxt, prev

    def add_node_to_head(self, node: ListNode):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def move_node_to_head(self, node: ListNode):
        self.remove_node(node)
        self.add_node_to_head(node)

    def pop_tail(self):
        res = self.tail.prev
        self.remove_node(res)
        return res

    def get(self, key):
        node = self.cache.get(key)
        if not node:
            return None
        self.move_node_to_head(node)
        return node.value

    def put(self, key, value):
        node = self.cache.get(key)
        if not node:
            newNode = ListNode(key, value)
            self.cache[key] = newNode
            self.add_node_to_head(newNode)
            if len(self.cache) > self.capacity:
                tail = self.pop_tail()
                del self.cache[tail.key]
        else:
            node.value = value
            self.move_node_to_head(node)
