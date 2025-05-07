import os

def enable_startup(script_path):
    autostart_dir = os.path.expanduser("~/.config/autostart")
    os.makedirs(autostart_dir, exist_ok=True)

    # Use --hidden to prevent showing window at startup
    desktop_entry = f"""[Desktop Entry]
    Type=Application
    Exec=python3 {script_path} --hidden
    Hidden=false
    NoDisplay=false
    X-GNOME-Autostart-enabled=true
    Name=Wallpy
    Comment=Auto wallpaper changer
    """

    desktop_path = os.path.join(autostart_dir, "wallpy.desktop")
    with open(desktop_path, "w") as f:
        f.write(desktop_entry)
