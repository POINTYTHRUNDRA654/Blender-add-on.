"""
Addon preferences for Fallout 4 Tutorial Helper.
Provides a single path field for the Havok2FBX toolkit so users can point to an
existing install instead of duplicating binaries.
"""

import os
import bpy


_DEFAULT_HAVOK2FBX_PATH = r"D:\Blender Foundation\havok2fbx_release_0.1a"


def _addon_name() -> str:
    """Return the add-on module name for preference lookup."""
    return __package__.split(".")[0]


def get_preferences():
    """Return the add-on preferences instance if registered, else None."""
    addon = bpy.context.preferences.addons.get(_addon_name())
    return addon.preferences if addon else None


def get_havok2fbx_path() -> str | None:
    """Return the configured Havok2FBX directory if set and exists."""
    prefs = get_preferences()
    if not prefs:
        return None
    path = bpy.path.abspath(prefs.havok2fbx_path)
    return path if path and os.path.isdir(path) else None


def is_havok2fbx_configured() -> bool:
    """True if the path is configured and points to an existing directory."""
    return get_havok2fbx_path() is not None


class FO4AddonPreferences(bpy.types.AddonPreferences):
    """Stores user-configurable add-on preferences."""

    bl_idname = _addon_name()

    havok2fbx_path: bpy.props.StringProperty(
        name="Havok2FBX Folder",
        subtype="DIR_PATH",
        default=_DEFAULT_HAVOK2FBX_PATH,
        description="Folder containing Havok2FBX binaries (existing install)",
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Havok2FBX", icon="FILE_FOLDER")
        box.prop(self, "havok2fbx_path", text="Folder")

        path = bpy.path.abspath(self.havok2fbx_path)
        if os.path.isdir(path):
            box.label(text=f"Configured: {path}", icon="CHECKMARK")
        else:
            box.label(text="Path not found. Set to your existing install.", icon="ERROR")


def register():
    bpy.utils.register_class(FO4AddonPreferences)


def unregister():
    bpy.utils.unregister_class(FO4AddonPreferences)
