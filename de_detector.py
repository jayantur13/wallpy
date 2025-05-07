import os

def detect_desktop_environment():
    desktop = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION")
    if desktop:
        desktop = desktop.lower()
        if "gnome" in desktop:
            return "gnome"
        elif "kde" in desktop:
            return "kde"
        elif "xfce" in desktop:
            return "xfce"
        elif "cinnamon" in desktop:
            return "cinnamon"
        elif "lxde" in desktop:
            return "lxde"
        elif "mate" in desktop:
            return "mate"
    return "unknown"