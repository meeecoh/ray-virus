import threading
from collections.abc import Callable
from dataclasses import dataclass, replace
from enum import Enum, auto


class ConnectionState(Enum):
    DISCONNECTED = auto()
    CONNECTING = auto()
    CONNECTED = auto()


@dataclass(frozen=True)
class AppState:
    connection: ConnectionState = ConnectionState.DISCONNECTED
    running: bool = True
    streamerbot_address : str = ""
    streamerbot_pw : str = ""
    redeems_enabled: bool = False
    redeem_name: str = None
    auto_start_socket : bool = False
    target_monitor_idx : int = 0

class AppStore:
    def __init__(self):
        self._state = AppState()
        self._subscribers : list[Callable[[AppState], None]] = []
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
    
    def subscribe(self, callback: Callable[[AppState], None]):
        with self._lock:
            self._subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable[[AppState], None]):
        with self._lock:
            self._subscribers.remove(callback)