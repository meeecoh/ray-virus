#!/bin/bash

pyinstaller \
    --distpath ./dist \
    --onedir \
    --noconsole \
    --paths src \
    --hidden-import ray_virus \
    --add-data src/assets:assets \
    --noconfirm \
    src/main.py