"""
UI Panels for the Fallout 4 Tutorial Add-on
"""

import bpy
from bpy.types import Panel
from . import hunyuan3d_helpers

class FO4_PT_MainPanel(Panel):
    """Main tutorial panel in the 3D View sidebar"""
    bl_label = "Fallout 4 Tutorial"
    bl_idname = "FO4_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Tutorial section
        box = layout.box()
        box.label(text="Tutorial System", icon='HELP')
        box.operator("fo4.start_tutorial", text="Start Tutorial", icon='PLAY')
        box.operator("fo4.show_help", text="Show Help", icon='QUESTION')
        
        # Notifications
        if hasattr(scene, 'fo4_notifications') and scene.fo4_notifications:
            notif_box = layout.box()
            notif_box.label(text="Notifications", icon='INFO')
            for notif in scene.fo4_notifications[-3:]:  # Show last 3
                notif_box.label(text=notif, icon='DOT')

class FO4_PT_MeshPanel(Panel):
    """Mesh creation helpers panel"""
    bl_label = "Mesh Helpers"
    bl_idname = "FO4_PT_mesh_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Mesh Creation", icon='MESH_CUBE')
        box.operator("fo4.create_base_mesh", text="Create Base Mesh", icon='MESH_DATA')
        box.operator("fo4.optimize_mesh", text="Optimize for FO4", icon='MOD_DECIM')
        box.operator("fo4.validate_mesh", text="Validate Mesh", icon='CHECKMARK')

class FO4_PT_TexturePanel(Panel):
    """Texture installation helpers panel"""
    bl_label = "Texture Helpers"
    bl_idname = "FO4_PT_texture_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Texture Setup", icon='TEXTURE')
        box.operator("fo4.setup_textures", text="Setup FO4 Materials", icon='MATERIAL')
        box.operator("fo4.install_texture", text="Install Texture", icon='FILE_IMAGE')
        box.operator("fo4.validate_textures", text="Validate Textures", icon='CHECKMARK')

class FO4_PT_ImageToMeshPanel(Panel):
    """Image to Mesh helpers panel"""
    bl_label = "Image to Mesh"
    bl_idname = "FO4_PT_image_to_mesh_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Create Mesh from Image", icon='IMAGE_DATA')
        box.operator("fo4.image_to_mesh", text="Image to Mesh (Height Map)", icon='MESH_GRID')
        
        box = layout.box()
        box.label(text="Displacement Map", icon='MOD_DISPLACE')
        box.operator("fo4.apply_displacement_map", text="Apply Displacement Map", icon='TEXTURE')
        
        # Info box
        info_box = layout.box()
        info_box.label(text="Quick Guide:", icon='INFO')
        info_box.label(text="• Formats: PNG, JPG, BMP, TIFF, TGA")
        info_box.label(text="• Grayscale: Bright=high, Dark=low")
        info_box.label(text="• Requires: PIL/Pillow & NumPy")
        info_box.label(text="• See README for install instructions")

class FO4_PT_AIGenerationPanel(Panel):
    """AI-powered mesh generation panel (Hunyuan3D-2)"""
    bl_label = "AI Generation (Optional)"
    bl_idname = "FO4_PT_ai_generation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # Check if Hunyuan3D is available
        is_available = hunyuan3d_helpers.Hunyuan3DHelpers.is_available()
        
        # Status box
        status_box = layout.box()
        if is_available:
            status_box.label(text="Status: Available ✓", icon='CHECKMARK')
        else:
            status_box.label(text="Status: Not Installed ✗", icon='ERROR')
        
        status_box.operator("fo4.show_hunyuan3d_info", text="Installation Info", icon='INFO')
        
        # AI Generation operators (enabled only if available)
        box = layout.box()
        box.label(text="Text to 3D", icon='FILE_TEXT')
        row = box.row()
        row.enabled = is_available
        row.operator("fo4.generate_mesh_from_text", text="Generate from Text", icon='OUTLINER_OB_FONT')
        
        box = layout.box()
        box.label(text="Image to 3D (Full Model)", icon='IMAGE_DATA')
        row = box.row()
        row.enabled = is_available
        row.operator("fo4.generate_mesh_from_image_ai", text="Generate from Image (AI)", icon='MESH_ICOSPHERE')
        
        # Info box
        info_box = layout.box()
        info_box.label(text="About AI Generation:", icon='INFO')
        info_box.label(text="• Uses Hunyuan3D-2 AI model")
        info_box.label(text="• Generates full 3D meshes")
        info_box.label(text="• Requires GPU & model download")
        info_box.label(text="• Completely optional feature")

class FO4_PT_AnimationPanel(Panel):
    """Animation helpers panel"""
    bl_label = "Animation Helpers"
    bl_idname = "FO4_PT_animation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Animation Setup", icon='ANIM')
        box.operator("fo4.setup_armature", text="Setup FO4 Armature", icon='ARMATURE_DATA')
        box.operator("fo4.validate_animation", text="Validate Animation", icon='CHECKMARK')

class FO4_PT_ExportPanel(Panel):
    """Export panel for Fallout 4"""
    bl_label = "Export to FO4"
    bl_idname = "FO4_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Export Options", icon='EXPORT')
        box.operator("fo4.export_mesh", text="Export Mesh (.nif)", icon='MESH_DATA')
        box.operator("fo4.export_all", text="Export Complete Mod", icon='PACKAGE')
        box.operator("fo4.validate_export", text="Validate Before Export", icon='CHECKMARK')

classes = (
    FO4_PT_MainPanel,
    FO4_PT_MeshPanel,
    FO4_PT_TexturePanel,
    FO4_PT_ImageToMeshPanel,
    FO4_PT_AIGenerationPanel,
    FO4_PT_AnimationPanel,
    FO4_PT_ExportPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
