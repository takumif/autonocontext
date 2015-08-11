from linked_list_queue import LinkedListQueue

class EarliestUsageCache(object):
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.size = 0
        self.keyQueue = LinkedListQueue()
        self.cache = dict()
        
    def add(self, key, value):
        if (not self.contains(key)):
            if (self.isFull()):
                self.__evict()
            
            self.keyQueue.enqueue(key)
            self.size += 1
        
        self.cache[key] = value
        
    def get(self, key):
        if (not self.contains(key)):
            raise ValueError("%s is not a key in this cache" % key)
        
        return self.cache[key]
        
    def contains(self, key):
        return key in self.cache
        
    def isFull(self):
        return self.size == self.capacity
    
    def clear(self):
        self.size = 0
        self.keyQueue = LinkedListQueue()
        self.cache = dict()
        
    def __evict(self):
        key = self.keyQueue.dequeue()
        self.cache.pop(key)
        self.size -= 1