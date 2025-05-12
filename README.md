<p align="center">
  <img src="https://iili.io/3NbbEOb.th.png" alt="Wallpy logo"/>
</p>

<h3 align="center">Wallpy - Wallpaper Changer for Linux 🖼️</h3>
<h4 align="center"><b>Wallpy is a lightweight, GTK-based wallpaper changer for Linux desktops...</b></h4>

<p align="center">
  <a href="#-features">Features</a> • 
  <a href="#%EF%B8%8F-supported-desktops">Supported Desktops</a> • 
  <a href="#-installation">Installation</a> • 
  <a href="#-binary-size-notice">Size Notice</a> • 
  <a href="#-usage">Usage</a> • 
  <a href="#%EF%B8%8F-development">Development</a>
</p>

## ✨ Features

- Automatically changes wallpaper at user-defined intervals
- Select any directory of images (supports most formats)
- Light/Dark mode wallpapers (planned via directory structure)
- Runs in the background
- Autostart on login (requires checkbox,checked)
- Supports multiple desktop environments (MATE, GNOME, XFCE)

## 🖥️ Supported Desktops

- ✅ MATE
- ✅ GNOME
- ✅ XFCE
- ✅ KDE

## 📦 Installation

Download from the [Releases](https://github.com/jayantur13/wallpy/releases) section:

```bash
# For Debian/Ubuntu
sudo dpkg -i wallpy.deb

# For Fedora/RedHat
sudo rpm -i wallpy.rpm

# For all Linux (portable)
chmod +x Wallpy.AppImage
./Wallpy.AppImage
```

### 📁 Binary Size Notice

Wallpy uses PyInstaller to bundle all required GTK and Python dependencies into a single standalone binary. This ensures that:

- ✅ Wallpy works out-of-the-box on most Linux systems
- ✅ No need to install Python or GTK manually

> Because of this, the size of each package is ~105 MB (AppImage/.deb/.rpm), and the full release directory is ~350 MB.
>
> > 🧪 Advanced users may clone the repo and run Wallpy from source (Python 3.12+ & PyGObject required) to avoid the bundled binary size. See <a href="#-development">Development</a>.

### 💡 Usage

1. Launch Wallpy from your Applications menu/Desktop or via terminal:

```
gtk-launch Wallpy
```

2. Select an image directory.
3. Choose an interval and hit "Start".
4. Minimize to tray — it keeps running in background.
   > Note: Other than gtk-launch,there are other ways,find them on internet.
   >
   > > App Note:
   > >
   > > - If you rename directory of selected wallpapers,you need to select it again.
   > > - Start on login,only works if wallpaper directory and interval is set.

## 🛠️ Development

```java
git clone https://github.com/jayantur13/wallpy.git
cd wallpy
pip install -r requirements.txt
python3 -m wallpy.main
```

## Issue/Contributing

- Before filing an issue make sure to search issues,after that make a new issue with full information of what you were doing and details about your linux distro.
- You're welcome to contribute on open issues,feature requests,enhancements etc.
- Read the [Guide](https://github.com/jayantur13/wallpy/blob/main/CONTRIBUTING.md "Guide") for more information.

## Changelog

Read about all the updates in [Changelog](https://github.com/jayantur13/wallpy/blob/main/Changelog.md "Changelog").

## 📜 License

Licensed under the MIT License. See [License](https://github.com/jayantur13/wallpy/blob/main/LICENSE "License") for details.

## 👤 Author

Made with ❤️ by Jayant Navrange

## 📄 LICENSE (MIT)

```text
MIT License

Copyright (c) 2025 Jayant Navrange aka jayantur13

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
