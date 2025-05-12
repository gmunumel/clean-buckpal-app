from typing import Callable, Dict, List, Type

from src.application.domain.model.event import Event


class EventDispatcher:
    """
    Event Dispatcher
    This class is responsible for dispatching events to the appropriate handlers.
    It maintains a registry of subscribers for each event type and notifies them
    when an event is published.
    Attributes:
        _subscribers: A dictionary mapping event types to their respective handlers.
    """

    def __init__(self):
        self._subscribers: Dict[Type, List[Callable]] = {}

    def subscribe(self, handlers: Dict[Type[Event], List[Callable]]):
        handlers_dict_items = handlers.items()
        for event_type, handler_list in handlers_dict_items:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].extend(handler_list)

    def publish(self, event):
        for handler in self._subscribers.get(type(event), []):
            handler(event)
