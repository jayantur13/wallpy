import subprocess
from de_detector import detect_desktop_environment

def set_wallpaper(image_path):
    try:
        de = detect_desktop_environment()
        #print(f"[DEBUG] Detected DE: {de}")

        if de == "mate":
            subprocess.run([
                "gsettings", "set", "org.mate.background",
                "picture-filename", image_path
            ], check=True)
            return True
        elif de == "gnome" or de == "cinnamon":
            uri = f"file://{image_path}"
            subprocess.run([
                "gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri
            ], check=True)
            subprocess.run([
                "gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri
            ], check=True)
            return True
        elif de == "xfce":
            subprocess.run([
                "xfconf-query",
                "--channel", "xfce4-desktop",
                "--property", "/backdrop/screen0/monitor0/image-path",
                "--set", image_path
            ], check=True)

        elif de == "kde":
            js_script = f'''
                var allDesktops = desktops();
                for (i=0;i<allDesktops.length;i++) {{
                    d = allDesktops[i];
                    d.wallpaperPlugin = "org.kde.image";
                    d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                    d.writeConfig("Image", "file://{image_path}");
                }}
            '''
            subprocess.run([
                "qdbus-qt5",
                "org.kde.plasmashell",
                "/PlasmaShell",
                "org.kde.PlasmaShell.evaluateScript",
                js_script
            ], check=True)
        else:
            print("Unsupported DE")
            return False

        return True

    except Exception as e:
        print(f"[Wallpaper Error] {e}")
        return False
