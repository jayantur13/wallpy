#!/bin/bash

set -e  # Exit on any error

APP_NAME="wallpy"
VERSION="1.0.0"
ARCH="amd64"
AUTHOR="Jayant Navrange"
EMAIL="vu.vcareforu@gmail.com"
URL="https://github.com/jayantur13/wallpy"
LICENSE_TYPE="MIT"

RELEASE_DIR="release"

# Clean previous builds
echo "🧹 Cleaning old build artifacts..."
rm -rf dist build *.deb *.rpm AppDir Wallpy.AppImage *.spec "$RELEASE_DIR"

# Set PYTHONPATH to include potential locations of 'gi'
export PYTHONPATH="/usr/lib/python3/dist-packages:/usr/lib/python3/site-packages:$PYTHONPATH"

# 1. Create PyInstaller executable
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller not found. Install it with: pip install pyinstaller"
    exit 1
fi
echo "📦 Building executable with PyInstaller..."
pyinstaller --hidden-import=gi.repository.Gtk main.py --onefile --name $APP_NAME --log-level DEBUG

# 2. Prepare AppDir for AppImage
echo "📂 Preparing AppDir for AppImage..."
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

cp dist/$APP_NAME AppDir/usr/bin/$APP_NAME
cp wallpy.desktop AppDir/usr/share/applications/
cp assets/wallpy.png AppDir/usr/share/icons/hicolor/256x256/apps/
cp assets/wallpy.png AppDir/wallpy.png
cp wallpy.desktop AppDir/wallpy.desktop   # ✅ REQUIRED FOR AppImage

# Make binary executable
chmod +x AppDir/usr/bin/$APP_NAME

# Required for AppImage: AppRun entry point
ln -sf usr/bin/$APP_NAME AppDir/AppRun
chmod +x AppDir/AppRun

# 3. Build AppImage
echo "🖼️ Creating AppImage..."
if ! command -v appimagetool &> /dev/null; then
    echo "❌ appimagetool not found. Please install it first."
    exit 1
fi
appimagetool AppDir Wallpy.AppImage

if ! command -v fpm &> /dev/null; then
    echo "❌ fpm not found. Please install it with: gem install --no-document fpm"
    exit 1
fi
# 4. Build .deb
echo "🧩 Creating .deb package..."
fpm -s dir -t deb \
    -n $APP_NAME \
    -v $VERSION \
    --license "$LICENSE_TYPE" \
    --maintainer "$AUTHOR <$EMAIL>" \
    --vendor "$AUTHOR" \
    --url "$URL" \
    --architecture $ARCH \
    --category "utility" \
    --description "Wallpy is a GTK-based wallpaper changer that updates your desktop background at intervals." \
    --after-install postinstall.sh \
    dist/$APP_NAME=/usr/bin/$APP_NAME \
    wallpy.desktop=/usr/share/applications/wallpy.desktop \
    assets/wallpy.png=/usr/share/icons/hicolor/256x256/apps/wallpy.png

# 5. Build .rpm
echo "📦 Creating .rpm package..."
fpm -s dir -t rpm \
    -n $APP_NAME \
    -v $VERSION \
    --license "$LICENSE_TYPE" \
    --maintainer "$AUTHOR <$EMAIL>" \
    --vendor "$AUTHOR" \
    --url "$URL" \
    --architecture $ARCH \
    --category "utility" \
    --description "Wallpy is a GTK-based wallpaper changer that updates your desktop background at intervals." \
    --after-install postinstall.sh \
    dist/$APP_NAME=/usr/bin/$APP_NAME \
    wallpy.desktop=/usr/share/applications/wallpy.desktop \
    assets/wallpy.png=/usr/share/icons/hicolor/256x256/apps/wallpy.png

# 6. Move output to release directory
echo "📁 Organizing release files..."
mkdir -p "$RELEASE_DIR"
mv *.deb *.rpm Wallpy.AppImage "$RELEASE_DIR/"

echo "✅ All packages built and moved to $RELEASE_DIR/:"
ls -lh "$RELEASE_DIR"
