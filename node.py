# double linked list

class Node:
    def __init__(self, value):
        self.val = value
        self.next = self
        self.prev = self

    def insert_after(self, value):
        new_node = Node(value)
        new_node.prev = self
        new_node.next = self.next
        self.next.prev = new_node
        self.next = new_node
        return new_node

    def remove(self):
        node_after = self.next
        node_after.prev = self.prev
        self.prev.next = node_after
        del self
        return node_after
