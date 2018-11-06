from enum import Enum


class MessageType(Enum):
    UPDATE = 0
    ADD = 1
    DELETE = 2


class Message:
    def __init__(self, type, **kwargs):
        self.type = type
        self.data = kwargs


class Observer:
    def __init__(self, func, observer_list):
        self.observer_list = observer_list
        self.func = func

    def notify(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def delete(self):
        self.observer_list.remove(self)
