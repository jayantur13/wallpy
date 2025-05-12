#!/usr/bin/env python3

import gi
import signal
import os

from autostart import enable_startup

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk, GLib, AppIndicator3

from wallpaper_changer import set_wallpaper
from config_manager import save_config, load_config


class WallpyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.wallpy.changer")
        self.window = None
        self.tray = None
        self.hidden_launch = False
    
    def run(self, argv, hidden=False):
        self.hidden_launch = hidden
        super().run(argv)
    
    def do_command_line(self, command_line):
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--hidden", action="store_true")
        args, _ = parser.parse_known_args(command_line.get_arguments()[1:])

        self.hidden = args.hidden
        self.activate()  # Triggers do_activate
        return 0


    def do_activate(self):
        if not self.window:
            self.window = Gtk.ApplicationWindow(application=self)
            self.window.set_title("Wallpy - Wallpaper Changer")
            try:
                self.window.set_icon_from_file("/mnt/sda3/software/wallpy/assets/wallpy.png")
            except:
                print("Warning: icon not found.")
            self.window.set_border_width(10)
            self.window.set_default_size(400, 200)

            self.window.connect("delete-event", self.on_window_close)
            self.build_ui()
            self.setup_tray()

        # Only show window if not hidden
        if not getattr(self, 'hidden', False) and not getattr(self, 'auto_started', False):
            GLib.idle_add(self.window.show_all)
            GLib.idle_add(self.window.present)


    def build_ui(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.window.add(vbox)

        self.folder_button = Gtk.FileChooserButton(title="Select Image Folder")
        self.folder_button.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        self.folder_button.connect("file-set", self.on_folder_selected)
        vbox.pack_start(self.folder_button, False, False, 0)

        self.intervals = {
            "30 seconds": 30,
            "1 minute": 60,
            "5 minutes": 300,
            "10 minutes": 600
        }

        self.interval_combo = Gtk.ComboBoxText()
        for label in self.intervals:
            self.interval_combo.append_text(label)
        self.interval_combo.set_active(1)
        self.interval_combo.connect("changed", self.on_interval_changed)
        vbox.pack_start(self.interval_combo, False, False, 0)

        self.autostart_checkbox = Gtk.CheckButton(label="Start on Login")
        self.autostart_checkbox.connect("toggled", self.on_autostart_toggled)
        vbox.pack_start(self.autostart_checkbox, False, False, 0)


        self.start_button = Gtk.Button(label="Start")
        self.start_button.connect("clicked", self.on_start_stop_clicked)
        vbox.pack_start(self.start_button, False, False, 0)

        self.log_label = Gtk.Label(label="")
        vbox.pack_start(self.log_label, False, False, 0)

        self.image_folder = None
        self.image_list = []
        self.interval_seconds = 60
        self.current_index = 0
        self.wallpaper_loop_id = None

        self.load_config()

    def setup_tray(self):
        self.tray = AppIndicator3.Indicator.new(
            "wallpy-tray",
            "/mnt/sda3/software/wallpy/assets/wallpy.png",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.tray.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        menu = Gtk.Menu()

        show_item = Gtk.MenuItem(label="Show")
        show_item.connect("activate", lambda _: self.reveal_window())
        menu.append(show_item)

        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", lambda _: self.quit())
        menu.append(quit_item)

        menu.show_all()
        self.tray.set_menu(menu)
    
    def reveal_window(self):
        self.window.show_all()
        self.window.present()


    def on_window_close(self, *args):
        self.window.hide()
        return True  # prevent app from quitting
    
    def on_autostart_toggled(self, checkbox):
        enabled = checkbox.get_active()
        config = load_config()
        config["autostart"] = enabled
        save_config(config)
        if enabled:
            enable_startup(os.path.abspath(__file__))
        else:
            self.disable_autostart()
        self.log(f"Autostart {'enabled' if enabled else 'disabled'}.")

    def disable_autostart(self):
        path = os.path.expanduser("~/.config/autostart/wallpy.desktop")
        if os.path.exists(path):
            os.remove(path)

    def load_config(self):
        config = load_config()
        autostart = config.get("autostart", False)
        self.autostart_checkbox.set_active(autostart)
        folder = config.get("image_folder")
        interval = config.get("interval", 60)
        self.interval_seconds = interval

        if folder and os.path.isdir(folder):
            self.image_folder = folder
            self.folder_button.set_filename(folder)
            self.image_list = self.load_images(folder)

        for label, secs in self.intervals.items():
            if secs == interval:
                self.interval_combo.set_active(list(self.intervals.keys()).index(label))
                break

        # ✅ Auto-start wallpaper loop if autostart is enabled and valid config
        if autostart and self.image_folder and self.image_list and self.interval_seconds:
            self.auto_started = True  # Flag to suppress window on activate
            self.start_wallpaper_loop()
        else:
            self.auto_started = False


    def on_folder_selected(self, widget):
        self.image_folder = widget.get_filename()
        self.image_list = self.load_images(self.image_folder)
        self.current_index = 0
        save_config({"image_folder": self.image_folder, "interval": self.interval_seconds})
        self.log("Folder selected.")

    def load_images(self, folder):
        exts = (".png", ".jpg", ".jpeg", ".bmp", ".webp")
        return [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]

    def on_interval_changed(self, widget):
        label = widget.get_active_text()
        self.interval_seconds = self.intervals.get(label, 60)
        save_config({"image_folder": self.image_folder, "interval": self.interval_seconds})
        self.log(f"Interval changed to {label}")
        if self.wallpaper_loop_id:
            self.restart_wallpaper_loop()

    def on_start_stop_clicked(self, button):
        if self.wallpaper_loop_id:
            self.stop_wallpaper_loop()
        else:
            self.start_wallpaper_loop()

    def start_wallpaper_loop(self):
        if not self.image_list:
            self.log("No images to start slideshow.")
            return
        self.wallpaper_loop_id = GLib.timeout_add_seconds(
            self.interval_seconds, self.change_wallpaper)
        self.start_button.set_label("Stop")
        self.log("Wallpaper loop started.")

    def stop_wallpaper_loop(self):
        if self.wallpaper_loop_id:
            GLib.source_remove(self.wallpaper_loop_id)
            self.wallpaper_loop_id = None
            self.start_button.set_label("Start")
            self.log("Wallpaper loop stopped.")

    def restart_wallpaper_loop(self):
        self.stop_wallpaper_loop()
        self.start_wallpaper_loop()

    def change_wallpaper(self):
        if not self.image_folder:
            self.log("No folder selected.")
            return False

        self.image_list = self.load_images(self.image_folder)  # 🔄 Refresh list
        if not self.image_list:
            self.log("No images found.")
            return False

        self.current_index %= len(self.image_list)  # Prevent index out of bounds
        image = self.image_list[self.current_index]
        success = set_wallpaper(image)
        self.current_index = (self.current_index + 1) % len(self.image_list)

        if success:
            self.log(f"Wallpaper set: {os.path.basename(image)}")
        else:
            self.log("Failed to set wallpaper.")
        return True


    def log(self, msg):
        self.log_label.set_text(msg)


import sys

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    hidden = "--hidden" in sys.argv
    app = WallpyApp()
    app.run(None, hidden=hidden)

if __name__ == "__main__":
    main()

