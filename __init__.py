"""
Blender Fallout 4 Tutorial Add-on
A comprehensive tutorial and helper system for creating Fallout 4 mods in Blender
"""

bl_info = {
    "name": "Fallout 4 Tutorial Helper",
    "author": "Tutorial Team",
    "version": (2, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Fallout 4",
    "description": "Comprehensive tutorial system and helpers for creating Fallout 4 mods including quests, NPCs, items, and world building",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy
from . import ui_panels
from . import operators
from . import tutorial_system
from . import mesh_helpers
from . import advanced_mesh_helpers
from . import texture_helpers
from . import animation_helpers
from . import export_helpers
from . import notification_system
from . import image_to_mesh_helpers
from . import hunyuan3d_helpers
from . import zoedepth_helpers
from . import gradio_helpers
from . import hymotion_helpers
from . import nvtt_helpers
from . import realesrgan_helpers
from . import get3d_helpers
from . import stylegan2_helpers
from . import instantngp_helpers
from . import imageto3d_helpers
from . import rignet_helpers
from . import motion_generation_helpers
from . import quest_helpers
from . import npc_helpers
from . import world_building_helpers
from . import item_helpers
from . import preset_library
from . import automation_system
from . import addon_integration
from . import desktop_tutorial_client
from . import shap_e_helpers

modules = [
    tutorial_system,
    notification_system,
    mesh_helpers,
    advanced_mesh_helpers,
    texture_helpers,
    animation_helpers,
    rignet_helpers,
    motion_generation_helpers,
    quest_helpers,
    npc_helpers,
    world_building_helpers,
    item_helpers,
    preset_library,
    automation_system,
    addon_integration,
    desktop_tutorial_client,
    shap_e_helpers,
    export_helpers,
    image_to_mesh_helpers,
    hunyuan3d_helpers,
    zoedepth_helpers,
    gradio_helpers,
    hymotion_helpers,
    nvtt_helpers,
    realesrgan_helpers,
    get3d_helpers,
    stylegan2_helpers,
    instantngp_helpers,
    imageto3d_helpers,
    operators,
    ui_panels,
]

def register():
    """Register all add-on classes and handlers"""
    for module in modules:
        module.register()
    
    # Initialize the tutorial system
    tutorial_system.initialize_tutorials()
    
    print("Fallout 4 Tutorial Helper registered successfully")

def unregister():
    """Unregister all add-on classes and handlers"""
    for module in reversed(modules):
        module.unregister()
    
    print("Fallout 4 Tutorial Helper unregistered")

if __name__ == "__main__":
    register()
