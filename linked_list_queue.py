from linked_list_node import LinkedListNode

class LinkedListQueue(object):
    def __init__(self):
        self.size = 0
        self.first = None
        self.last = None
            
    def __len__(self):
        return self.size
        
    def enqueue(self, value):
        newNode = LinkedListNode(value)
        
        if (len(self) == 0):
            self.first = newNode
            self.last = newNode
        else:
            self.last.next = newNode
            newNode.prev = self.last
            self.last = newNode
        
        self.size += 1
            
    def dequeue(self):
        if (len(self) == 0):
            raise "Cannot dequeue from an empty queue"
            
        value = self.first.value
        
        if (len(self) == 1):
            self.first = None
            self.last = None
        else:
            self.first = self.first.next
            self.first.prev = None
            
        self.size -= 1
        return value