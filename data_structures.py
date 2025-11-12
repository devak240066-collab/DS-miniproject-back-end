"""
Data Structures Implementation
Linked List, Stack, and Queue implementations for the Product Inventory System
"""


class Node:
    """Node class for Linked List implementation"""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Singly Linked List implementation"""
    def __init__(self):
        self.head = None
        self.size = 0
    
    def is_empty(self):
        """Check if the linked list is empty"""
        return self.head is None
    
    def append(self, data):
        """Add an element to the end of the linked list"""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def prepend(self, data):
        """Add an element to the beginning of the linked list"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert_at(self, index, data):
        """Insert an element at a specific index"""
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")
        
        if index == 0:
            self.prepend(data)
            return
        
        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self.size += 1
    
    def delete(self, data):
        """Delete the first occurrence of data"""
        if self.is_empty():
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        
        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def search(self, data):
        """Search for an element in the linked list"""
        current = self.head
        index = 0
        while current is not None:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1
    
    def get(self, index):
        """Get element at a specific index"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data
    
    def display(self):
        """Display all elements in the linked list"""
        elements = []
        current = self.head
        while current is not None:
            elements.append(str(current.data))
            current = current.next
        return elements
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        return " -> ".join(self.display()) if not self.is_empty() else "Empty"


class Stack:
    """Stack implementation using a list"""
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        """Check if the stack is empty"""
        return len(self.items) == 0
    
    def push(self, item):
        """Add an element to the top of the stack"""
        self.items.append(item)
    
    def pop(self):
        """Remove and return the top element from the stack"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        """Return the top element without removing it"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def size(self):
        """Return the size of the stack"""
        return len(self.items)
    
    def display(self):
        """Display all elements in the stack"""
        return self.items.copy()
    
    def __str__(self):
        return str(self.items)
    
    def __len__(self):
        return len(self.items)


class Queue:
    """Queue implementation using a list"""
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        """Check if the queue is empty"""
        return len(self.items) == 0
    
    def enqueue(self, item):
        """Add an element to the rear of the queue"""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return the front element from the queue"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.pop(0)
    
    def front(self):
        """Return the front element without removing it"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]
    
    def rear(self):
        """Return the rear element without removing it"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[-1]
    
    def size(self):
        """Return the size of the queue"""
        return len(self.items)
    
    def display(self):
        """Display all elements in the queue"""
        return self.items.copy()
    
    def __str__(self):
        return str(self.items)
    
    def __len__(self):
        return len(self.items)









