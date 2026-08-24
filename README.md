TODO:

1. Refactor websocket client to use event loop
2. Create multiple window types
3. Register multiple window types

manager class
- registers windows
- handles + counts how many windows are open
- handles placement of windows
- closing the manager closes all other windows

- disables redeem

icon
- displays status of connection
- opens tkinter window with config options

config window
- change server addresses
- change 

window
- different window types (10 different ones at least)


streamerbot client
- open websocket
- listen for events

event class
event_name