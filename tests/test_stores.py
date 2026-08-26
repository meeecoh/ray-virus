from ray_virus.stores import AppStore, AppState, ConnectionState
import pytest
from dataclasses import FrozenInstanceError

    
def test_sub():
    """Check if sub actually adds subscriber"""
    def sub_func(new_state: AppState):
        pass
    store = AppStore()
    store.subscribe(sub_func)
    assert len(store._subscribers) == 1
    
def test_unsub():
    """Check if unsub actually removes subscriber"""
    def sub_func(new_state: AppState):
            pass
    store = AppStore()
    store.subscribe(sub_func)
    store.unsubscribe(sub_func)

def test_mutate_state():
    """Mutating the returned object should raise FrozenInstanceError"""
    with pytest.raises(FrozenInstanceError):
        def mutate_test(new_state: AppState):
            new_state.enabled = False
        store = AppStore()
        store.subscribe(mutate_test)
        store.update(enabled=True)

def test_update_identical():
    """Check if setting identical state calls subscribers"""
    ctr = 0
    def add_to_ctr(new_state: AppState):
        nonlocal ctr
        ctr += 1
    
    store = AppStore()
    store.subscribe(add_to_ctr)
    store.update(connection=ConnectionState.CONNECTED)
    store.update(connection=ConnectionState.CONNECTED)
    
    #counter should only be added once
    assert ctr == 1
    
def test_receive_state():
    """Test if subscribers actually receive AppState type"""
    def receive_state(new_state: AppState):
        assert isinstance(new_state, AppState)
    store = AppStore()
    store.subscribe(receive_state)
    store.update(connection=ConnectionState.CONNECTED)

