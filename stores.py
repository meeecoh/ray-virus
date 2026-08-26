from enum import Enum, auto
from typing import Callable
import threading
    
from dataclasses import dataclass, replace


class ConnectionState(Enum):
    DISCONNECTED = auto()
    CONNECTING = auto()
    CONNECTED = auto()


@dataclass(frozen=True)
class AppState:
    connection: ConnectionState = ConnectionState.DISCONNECTED
    enabled: bool = False
    running: bool = True

class AppStore:
    def __init__(self):
        self._state = AppState()
        self._subscribers : list[Callable[[ConnectionState], None]] = []
        self._lock = threading.Lock()
        
    @property
    def state(self) -> AppState:
        with self._lock:
            return self._state
    
    def update(self, **changes) -> None:
        with self._lock:
            new_state = replace(self._state, **changes)
            if new_state == self._state:
                return
            self._state = new_state
            subscribers = list(self._subscribers)
        for callback in subscribers:
                callback(new_state)
    
    def subscribe(self, callback: Callable[[ConnectionState], None]):
        with self._lock:
            self._subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable[[ConnectionState], None]):
        with self._lock:
            self._subscribers.remove(callback)