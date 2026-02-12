# Installation Guide

## Prerequisites

- Blender 3.0 or higher
- Basic knowledge of Blender interface
- Understanding of Fallout 4 modding basics (helpful but not required)

## Installation Steps

### Method 1: Install from ZIP

1. Download the add-on as a ZIP file
2. Open Blender
3. Go to `Edit > Preferences` (or `Blender > Preferences` on macOS)
4. Navigate to the "Add-ons" section
5. Click the "Install..." button at the top
6. Browse to the downloaded ZIP file and select it
7. The add-on will be installed
8. Find "Fallout 4 Tutorial Helper" in the add-ons list
9. Check the checkbox to enable it

### Method 2: Install from Folder

1. Download or clone the add-on folder
2. Locate your Blender add-ons directory:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\<version>\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/<version>/scripts/addons/`
   - **Linux**: `~/.config/blender/<version>/scripts/addons/`
3. Copy the entire add-on folder into the addons directory
4. Restart Blender
5. Go to `Edit > Preferences > Add-ons`
6. Search for "Fallout 4 Tutorial Helper"
7. Enable the add-on by checking its checkbox

## Verification

After installation, verify the add-on is working:

1. Open Blender
2. In the 3D Viewport, press `N` to open the sidebar
3. Look for a "Fallout 4" tab
4. Click on the tab to see the add-on panels
5. You should see:
   - Fallout 4 Tutorial (main panel)
   - Mesh Helpers
   - Texture Helpers
   - Animation Helpers
   - Export to FO4

## Troubleshooting Installation

### Add-on doesn't appear in the list
- Make sure you're using Blender 3.0 or higher
- Check that all Python files are in the correct directory
- Restart Blender completely

### Add-on appears but can't be enabled
- Check the Blender console (Window > Toggle System Console on Windows)
- Look for error messages
- Ensure all required files are present:
  - `__init__.py`
  - `ui_panels.py`
  - `operators.py`
  - `tutorial_system.py`
  - `notification_system.py`
  - `mesh_helpers.py`
  - `texture_helpers.py`
  - `animation_helpers.py`
  - `export_helpers.py`

### Tab doesn't appear in sidebar
- Press `N` to toggle the sidebar visibility
- Make sure the add-on is enabled in preferences
- Try switching to a different workspace and back

## Updating the Add-on

To update to a newer version:

1. Disable the current version in Add-ons preferences
2. Remove the old add-on files
3. Install the new version using either method above
4. Enable the new version

## Uninstallation

To remove the add-on:

1. Go to `Edit > Preferences > Add-ons`
2. Find "Fallout 4 Tutorial Helper"
3. Click the remove button (trash icon)
4. Restart Blender

Alternatively, manually delete the add-on folder from the Blender addons directory.
