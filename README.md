# Ray-Virus Window Manager

Let your chat display early 2000s ad pop-ups on your stream using channel redeems!  
~ 20 different wacky wonderful windows that will definitely annoy you on stream!


## Features
🔥 Integration with streamerbot for twitch channel redeems  
🔥 20 different wacky fake popup windows  
🔥 Randomized and toggleable windows  

## Installation


## Building From Source
-- Tested with python v3.14.6 --
1. clone the repository
```
git clone https://github.com/Meeecoh/ray-virus.git
cd ray-virus
```
2. Create virtual environment
```
python -m venv .venv 

# activate (macOS/Linux)
source .venv/bin/activate

# activate (windows)
.venv/Scripts/activate.bat
```
3. Install Dependencies
```
pip install -r requirments.txt
```
3. Run build script
```
# windows
./make_build.ps1

# (macOS/Linux)
./make_build.sh
```

## Usage
### Enabling or Disabling popups
It's recommended to enable/disable the channel redeem itself through streamerbot instead of disabling the popups.
In a case where you'd wanna do that, you can toggle "Enabled" through the system icon tray or from the config menu `icon tray>Config>Toggle enable`.

### Setting Websocket address and Password
You can set the address in the Config menu accessed through the Icon tray


## License
This repository is licensed under the [MIT LICENSE](LICENSE)

