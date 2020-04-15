"""Modulo node."""

class Node:
    """Gerencia items da fila."""
    
    def __init__(self, data):
        self.data = data
        self.next = None