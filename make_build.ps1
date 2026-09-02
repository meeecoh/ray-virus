pyinstaller `
    --distpath ./dist `
    --onefile `
    --noconsole `
    --noconfirm `
    --paths src `
    --hidden-import ray_virus `
    --add-data src/assets:assets `
    --name "ray-virus" `
    src/main.py
