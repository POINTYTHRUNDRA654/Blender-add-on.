"""
UI Panels for the Fallout 4 Tutorial Add-on
"""

import bpy
from bpy.types import Panel
from . import hunyuan3d_helpers, gradio_helpers, hymotion_helpers, nvtt_helpers, rignet_helpers

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
        
        # Advanced mesh tools
        adv_box = layout.box()
        adv_box.label(text="Advanced Mesh Tools", icon='MODIFIER')
        adv_box.operator("fo4.analyze_mesh_quality", text="Analyze Quality", icon='INFO')
        adv_box.operator("fo4.auto_repair_mesh", text="Auto-Repair", icon='TOOL_SETTINGS')
        adv_box.operator("fo4.smart_decimate", text="Smart Decimate", icon='MOD_DECIM')
        adv_box.operator("fo4.generate_lod", text="Generate LOD Chain", icon='OUTLINER_OB_MESH')
        adv_box.operator("fo4.optimize_uvs", text="Optimize UVs", icon='UV')

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
        
        # ZoeDepth section
        from . import zoedepth_helpers
        available, _ = zoedepth_helpers.check_zoedepth_availability()
        
        depth_box = layout.box()
        depth_box.label(text="Depth Estimation (ZoeDepth)", icon='CAMERA_DATA')
        
        if available:
            depth_box.label(text="Status: Available ✓", icon='CHECKMARK')
        else:
            depth_box.label(text="Status: Not Installed ✗", icon='ERROR')
        
        row = depth_box.row()
        row.enabled = available
        row.operator("fo4.estimate_depth", text="Estimate Depth & Create Mesh", icon='MESH_GRID')
        
        depth_box.operator("fo4.show_zoedepth_info", text="Installation Info", icon='INFO')
        
        # Info box
        info_box = layout.box()
        info_box.label(text="Quick Guide:", icon='INFO')
        info_box.label(text="• Height Map: Grayscale images")
        info_box.label(text="• ZoeDepth: RGB images (AI depth)")
        info_box.label(text="• Formats: PNG, JPG, BMP, TIFF, TGA")
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
        
        # Gradio Web UI section
        gradio_available = gradio_helpers.GradioHelpers.is_available()
        server_running = gradio_helpers.GradioHelpers.is_server_running()
        
        layout.separator()
        web_box = layout.box()
        web_box.label(text="Web Interface (Gradio)", icon='URL')
        
        if gradio_available:
            if server_running:
                web_box.label(text="Server: Running ✓", icon='CHECKMARK')
                web_box.operator("fo4.stop_gradio_server", text="Stop Web UI", icon='CANCEL')
            else:
                web_box.label(text="Server: Stopped", icon='RADIOBUT_OFF')
                web_box.operator("fo4.start_gradio_server", text="Start Web UI", icon='PLAY')
        else:
            web_box.label(text="Gradio: Not Installed ✗", icon='ERROR')
        
        web_box.operator("fo4.show_gradio_info", text="Web UI Info", icon='INFO')
        
        if gradio_available:
            web_box.label(text="Open: http://localhost:7860")
        
        # HY-Motion-1.0 section
        hymotion_available = hymotion_helpers.HyMotionHelpers.is_available()
        
        layout.separator()
        motion_box = layout.box()
        motion_box.label(text="Motion Generation (HY-Motion)", icon='ANIM')
        
        if hymotion_available:
            motion_box.label(text="Status: Available ✓", icon='CHECKMARK')
            motion_box.operator("fo4.generate_motion_from_text", text="Generate Motion", icon='ANIM_DATA')
            motion_box.operator("fo4.import_motion_file", text="Import Motion File", icon='IMPORT')
        else:
            motion_box.label(text="Status: Not Installed ✗", icon='ERROR')
        
        motion_box.operator("fo4.show_hymotion_info", text="Motion Info", icon='INFO')


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

class FO4_PT_RigNetPanel(Panel):
    """RigNet auto-rigging panel"""
    bl_label = "Auto-Rigging (RigNet)"
    bl_idname = "FO4_PT_rignet_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # Check if RigNet is available
        is_available, message = rignet_helpers.RigNetHelpers.check_rignet_available()
        
        # Check if libigl is available
        libigl_available, libigl_message = rignet_helpers.RigNetHelpers.check_libigl_available()
        
        # Status box for RigNet
        status_box = layout.box()
        status_box.label(text="RigNet Status:", icon='INFO')
        if is_available:
            status_box.label(text="✓ RigNet Available", icon='CHECKMARK')
            # Show just the directory name
            import os
            rignet_dir = os.path.basename(message)
            status_box.label(text=f"  {rignet_dir}", icon='FILE_FOLDER')
        else:
            status_box.label(text="✗ RigNet Not Installed", icon='ERROR')
        
        status_box.operator("fo4.check_rignet", text="Check RigNet", icon='INFO')
        
        # Status box for libigl
        libigl_box = layout.box()
        libigl_box.label(text="libigl Status:", icon='INFO')
        if libigl_available:
            libigl_box.label(text="✓ libigl Available", icon='CHECKMARK')
            if "pip" in libigl_message:
                libigl_box.label(text="  Installed via pip", icon='PACKAGE')
            else:
                import os
                libigl_dir = os.path.basename(libigl_message.split("at ")[-1]) if "at " in libigl_message else "libigl"
                libigl_box.label(text=f"  {libigl_dir}", icon='FILE_FOLDER')
        else:
            libigl_box.label(text="✗ libigl Not Installed", icon='ERROR')
        
        libigl_box.operator("fo4.check_libigl", text="Check libigl", icon='INFO')
        
        layout.operator("fo4.show_rignet_info", text="Installation Guide", icon='QUESTION')
        
        # Auto-rigging operators (RigNet)
        rignet_box = layout.box()
        rignet_box.label(text="RigNet (Full Auto-Rigging)", icon='ARMATURE_DATA')
        
        row = rignet_box.row()
        row.operator("fo4.prepare_for_rignet", text="1. Prepare Mesh", icon='MODIFIER')
        
        row = rignet_box.row()
        row.enabled = is_available
        row.operator("fo4.auto_rig_mesh", text="2. Auto-Rig", icon='ARMATURE_DATA')
        
        row = rignet_box.row()
        row.operator("fo4.export_for_rignet", text="Export for External RigNet", icon='EXPORT')
        
        # BBW skinning operators (libigl)
        libigl_op_box = layout.box()
        libigl_op_box.label(text="libigl (BBW Skinning)", icon='MOD_SKIN')
        
        row = libigl_op_box.row()
        row.enabled = libigl_available
        row.operator("fo4.compute_bbw_skinning", text="Compute BBW Weights", icon='WPAINT_HLT')
        
        libigl_op_box.label(text="(Requires existing armature)", icon='INFO')
        
        # Info box
        info_box = layout.box()
        info_box.label(text="About Auto-Rigging:", icon='INFO')
        info_box.label(text="• RigNet: Full auto-rigging")
        info_box.label(text="  - AI predicts skeleton")
        info_box.label(text="  - Best for humanoid/animals")
        info_box.label(text="• libigl: BBW skinning only")
        info_box.label(text="  - Needs existing skeleton")
        info_box.label(text="  - Fast & reliable weights")
        
        if not is_available and not libigl_available:
            info_box.separator()
            info_box.label(text="Quick Install:", icon='DOWNLOAD')
            info_box.label(text="RigNet:")
            info_box.label(text="  gh repo clone govindjoshi12/")
            info_box.label(text="    rignet-gj")
            info_box.label(text="libigl:")
            info_box.label(text="  pip install libigl")
            info_box.label(text="OR gh repo clone libigl/")
            info_box.label(text="  libigl-python-bindings")

class FO4_PT_NVTTPanel(Panel):
    """NVIDIA Texture Tools panel"""
    bl_label = "Texture Conversion (NVTT)"
    bl_idname = "FO4_PT_nvtt_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # Check if NVTT is available
        is_available = nvtt_helpers.NVTTHelpers.is_nvtt_available()
        
        # Status box
        status_box = layout.box()
        if is_available:
            status_box.label(text="NVTT: Available ✓", icon='CHECKMARK')
            nvtt_path = nvtt_helpers.NVTTHelpers.get_nvtt_path()
            if nvtt_path:
                # Show just the filename, not full path
                import os
                status_box.label(text=f"Path: {os.path.dirname(nvtt_path)}", icon='FILE_FOLDER')
        else:
            status_box.label(text="NVTT: Not Installed ✗", icon='ERROR')
        
        status_box.operator("fo4.check_nvtt_installation", text="Check Installation", icon='INFO')
        
        # Conversion operators
        box = layout.box()
        box.label(text="Convert to DDS for FO4", icon='FILE_IMAGE')
        
        row = box.row()
        row.enabled = is_available
        row.operator("fo4.convert_texture_to_dds", text="Convert Single Texture", icon='IMAGE_DATA')
        
        row = box.row()
        row.enabled = is_available
        row.operator("fo4.convert_object_textures_to_dds", text="Convert Object Textures", icon='MATERIAL')
        
        # Info box
        info_box = layout.box()
        info_box.label(text="About DDS Conversion:", icon='INFO')
        info_box.label(text="• DDS is required for FO4")
        info_box.label(text="• BC1 (DXT1): Diffuse textures")
        info_box.label(text="• BC5 (ATI2): Normal maps")
        info_box.label(text="• BC3 (DXT5): Alpha textures")
        
        if not is_available:
            info_box.separator()
            info_box.label(text="Install NVTT:", icon='DOWNLOAD')
            info_box.label(text="gh repo clone castano/")
            info_box.label(text="  nvidia-texture-tools")

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


class FO4_PT_BatchProcessingPanel(Panel):
    """Batch processing panel for multiple objects"""
    bl_label = "Batch Processing"
    bl_idname = "FO4_PT_batch_processing_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # Info box
        info_box = layout.box()
        info_box.label(text="Select multiple meshes", icon='INFO')
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        info_box.label(text=f"Selected: {len(selected_meshes)} meshes")
        
        # Batch operations
        box = layout.box()
        box.label(text="Batch Operations", icon='MODIFIER')
        
        row = box.row()
        row.enabled = len(selected_meshes) > 0
        row.operator("fo4.batch_optimize_meshes", text="Batch Optimize", icon='MOD_DECIM')
        
        row = box.row()
        row.enabled = len(selected_meshes) > 0
        row.operator("fo4.batch_validate_meshes", text="Batch Validate", icon='CHECKMARK')
        
        row = box.row()
        row.enabled = len(selected_meshes) > 0
        row.operator("fo4.batch_export_meshes", text="Batch Export", icon='EXPORT')
        
        # Tips
        tips_box = layout.box()
        tips_box.label(text="Tips:", icon='HELP')
        tips_box.label(text="• Select meshes with Shift+Click")
        tips_box.label(text="• Use Box Select (B key)")
        tips_box.label(text="• Processing is sequential")


class FO4_PT_PresetsPanel(Panel):
    """Smart presets panel for quick object creation"""
    bl_label = "Smart Presets"
    bl_idname = "FO4_PT_presets_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # Weapon presets
        box = layout.box()
        box.label(text="Weapon Presets", icon='MOD_ARMATURE')
        box.operator("fo4.create_weapon_preset", text="Create Weapon", icon='MESH_CUBE')
        
        # Armor presets
        box = layout.box()
        box.label(text="Armor Presets", icon='MESH_UVSPHERE')
        box.operator("fo4.create_armor_preset", text="Create Armor", icon='MESH_CUBE')
        
        # Prop presets
        box = layout.box()
        box.label(text="Prop Presets", icon='OBJECT_DATA')
        box.operator("fo4.create_prop_preset", text="Create Prop", icon='MESH_CUBE')
        
        # Info
        info_box = layout.box()
        info_box.label(text="About Presets:", icon='INFO')
        info_box.label(text="• Pre-configured for FO4")
        info_box.label(text="• Optimal scale & settings")
        info_box.label(text="• Materials already setup")
        info_box.label(text="• Ready to customize")


class FO4_PT_AutomationPanel(Panel):
    """Automation and quick tools panel"""
    bl_label = "Automation & Quick Tools"
    bl_idname = "FO4_PT_automation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        
        # Quick prepare
        box = layout.box()
        box.label(text="One-Click Preparation", icon='TOOL_SETTINGS')
        row = box.row()
        row.enabled = obj and obj.type == 'MESH'
        row.operator("fo4.quick_prepare_export", text="Quick Prepare for Export", icon='CHECKMARK')
        row.scale_y = 1.5
        
        # Auto-fix
        box = layout.box()
        box.label(text="Auto-Fix Issues", icon='MODIFIER')
        row = box.row()
        row.enabled = obj and obj.type == 'MESH'
        row.operator("fo4.auto_fix_issues", text="Auto-Fix Common Issues", icon='TOOL_SETTINGS')
        
        # Collision mesh
        box = layout.box()
        box.label(text="Collision Mesh", icon='MESH_ICOSPHERE')
        row = box.row()
        row.enabled = obj and obj.type == 'MESH'
        row.operator("fo4.generate_collision_mesh", text="Generate Collision", icon='MESH_DATA')
        
        # Smart material
        box = layout.box()
        box.label(text="Smart Material", icon='MATERIAL')
        row = box.row()
        row.enabled = obj and obj.type == 'MESH'
        row.operator("fo4.smart_material_setup", text="Auto-Load Textures", icon='FILE_FOLDER')
        
        # What it does
        info_box = layout.box()
        info_box.label(text="Quick Prepare includes:", icon='INFO')
        info_box.label(text="1. Mesh optimization")
        info_box.label(text="2. Material setup")
        info_box.label(text="3. Validation checks")
        info_box.label(text="4. Texture validation")


class FO4_PT_VegetationPanel(Panel):
    """Vegetation and landscaping panel"""
    bl_label = "Vegetation & Landscaping"
    bl_idname = "FO4_PT_vegetation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        selected_meshes = [o for o in context.selected_objects if o.type == 'MESH']
        
        # Create vegetation
        box = layout.box()
        box.label(text="Create Vegetation", icon='OUTLINER_OB_FORCE_FIELD')
        box.operator("fo4.create_vegetation_preset", text="Create Vegetation", icon='ADD')
        
        # Scatter vegetation
        box = layout.box()
        box.label(text="Scatter & Distribute", icon='PARTICLE_DATA')
        row = box.row()
        row.enabled = obj and obj.type == 'MESH'
        row.operator("fo4.scatter_vegetation", text="Scatter Vegetation", icon='PARTICLES')
        
        # Combine meshes
        box = layout.box()
        box.label(text="Combine for Performance", icon='MESH_DATA')
        box.label(text=f"Selected: {len(selected_meshes)} meshes")
        row = box.row()
        row.enabled = len(selected_meshes) >= 2
        row.operator("fo4.combine_vegetation_meshes", text="Combine Selected", icon='AUTOMERGE_ON')
        
        # Optimization
        box = layout.box()
        box.label(text="FPS Optimization", icon='SORTTIME')
        row = box.row()
        row.enabled = obj and obj.type == 'MESH'
        row.operator("fo4.optimize_vegetation_fps", text="Optimize for FPS", icon='TIME')
        
        # LOD generation
        box = layout.box()
        box.label(text="LOD System", icon='OUTLINER_OB_MESH')
        row = box.row()
        row.enabled = obj and obj.type == 'MESH'
        row.operator("fo4.create_vegetation_lod_chain", text="Create LOD Chain", icon='MESH_GRID')
        
        # Baking
        box = layout.box()
        box.label(text="Baking", icon='RENDER_STILL')
        row = box.row()
        row.enabled = obj and obj.type == 'MESH'
        row.operator("fo4.bake_vegetation_ao", text="Setup AO Bake", icon='SHADING_RENDERED')
        
        # Tips
        tips_box = layout.box()
        tips_box.label(text="Workflow Tips:", icon='INFO')
        tips_box.label(text="1. Create vegetation types")
        tips_box.label(text="2. Scatter across area")
        tips_box.label(text="3. Combine for FPS boost")
        tips_box.label(text="4. Generate LODs")
        tips_box.label(text="5. Export as single mesh")


class FO4_PT_QuestPanel(Panel):
    """Quest creation panel"""
    bl_label = "Quest Creation"
    bl_idname = "FO4_PT_quest_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # Quest template
        box = layout.box()
        box.label(text="Quest Setup", icon='BOOKMARKS')
        box.operator("fo4.create_quest_template", text="Create Quest Template", icon='ADD')
        box.operator("fo4.export_quest_data", text="Export Quest Data", icon='EXPORT')
        
        # Papyrus script
        box = layout.box()
        box.label(text="Scripting", icon='SCRIPT')
        box.operator("fo4.generate_papyrus_script", text="Generate Papyrus Script", icon='FILE_SCRIPT')
        
        # Info
        info_box = layout.box()
        info_box.label(text="Quest Workflow:", icon='INFO')
        info_box.label(text="1. Create quest template")
        info_box.label(text="2. Define stages & objectives")
        info_box.label(text="3. Generate Papyrus script")
        info_box.label(text="4. Export for Creation Kit")


class FO4_PT_NPCPanel(Panel):
    """NPC and creature creation panel"""
    bl_label = "NPCs & Creatures"
    bl_idname = "FO4_PT_npc_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # NPC creation
        box = layout.box()
        box.label(text="Create NPC", icon='ARMATURE_DATA')
        box.operator("fo4.create_npc", text="Create NPC", icon='ADD')
        
        # Creature creation
        box = layout.box()
        box.label(text="Create Creature", icon='MOD_ARMATURE')
        box.operator("fo4.create_creature", text="Create Creature", icon='ADD')
        
        # Tips
        tips_box = layout.box()
        tips_box.label(text="Tips:", icon='INFO')
        tips_box.label(text="• Customize base mesh")
        tips_box.label(text="• Add armature for animation")
        tips_box.label(text="• Setup materials & textures")
        tips_box.label(text="• Export as FBX for import")


class FO4_PT_WorldBuildingPanel(Panel):
    """World building and cells panel"""
    bl_label = "World Building"
    bl_idname = "FO4_PT_world_building_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # Interior cells
        box = layout.box()
        box.label(text="Interior Cells", icon='HOME')
        box.operator("fo4.create_interior_cell", text="Create Interior Cell", icon='ADD')
        box.operator("fo4.create_door_frame", text="Add Door Frame", icon='MESH_PLANE')
        
        # Workshop objects
        box = layout.box()
        box.label(text="Workshop/Settlement", icon='TOOL_SETTINGS')
        box.operator("fo4.create_workshop_object", text="Create Workshop Object", icon='ADD')
        
        # Navigation
        box = layout.box()
        box.label(text="Navigation", icon='ORIENTATION_NORMAL')
        box.operator("fo4.create_navmesh", text="Create NavMesh Helper", icon='MESH_GRID')
        
        # Lighting
        box = layout.box()
        box.label(text="Lighting Presets", icon='LIGHT')
        box.operator("fo4.create_lighting_preset", text="Create Lighting Preset", icon='ADD')
        
        # Info
        info_box = layout.box()
        info_box.label(text="World Building:", icon='INFO')
        info_box.label(text="• Start with cell template")
        info_box.label(text="• Add doors & windows")
        info_box.label(text="• Place workshop objects")
        info_box.label(text="• Setup lighting")
        info_box.label(text="• Create navmesh last")


class FO4_PT_ItemCreationPanel(Panel):
    """Item creation panel"""
    bl_label = "Item Creation"
    bl_idname = "FO4_PT_item_creation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fallout 4'
    bl_parent_id = "FO4_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # Weapons
        box = layout.box()
        box.label(text="Weapons", icon='MOD_ARMATURE')
        box.operator("fo4.create_weapon_item", text="Create Weapon", icon='ADD')
        
        # Armor
        box = layout.box()
        box.label(text="Armor", icon='MESH_UVSPHERE')
        box.operator("fo4.create_armor_item", text="Create Armor", icon='ADD')
        box.operator("fo4.create_power_armor_piece", text="Create Power Armor", icon='ADD')
        
        # Consumables
        box = layout.box()
        box.label(text="Consumables", icon='FORCE_LENNARDJONES')
        box.operator("fo4.create_consumable", text="Create Consumable", icon='ADD')
        
        # Misc items
        box = layout.box()
        box.label(text="Misc Items", icon='OBJECT_DATA')
        box.operator("fo4.create_misc_item", text="Create Misc Item", icon='ADD')
        
        # Clutter
        box = layout.box()
        box.label(text="Clutter/Decoration", icon='PROP_OFF')
        box.operator("fo4.create_clutter_object", text="Create Clutter", icon='ADD')
        
        # Info
        info_box = layout.box()
        info_box.label(text="Item Workflow:", icon='INFO')
        info_box.label(text="1. Create item base")
        info_box.label(text="2. Model details")
        info_box.label(text="3. Setup textures")
        info_box.label(text="4. Optimize & validate")
        info_box.label(text="5. Export as FBX")


classes = (
    FO4_PT_MainPanel,
    FO4_PT_MeshPanel,
    FO4_PT_TexturePanel,
    FO4_PT_ImageToMeshPanel,
    FO4_PT_AIGenerationPanel,
    FO4_PT_AnimationPanel,
    FO4_PT_RigNetPanel,
    FO4_PT_NVTTPanel,
    FO4_PT_ExportPanel,
    # New panels for enhancements
    FO4_PT_BatchProcessingPanel,
    FO4_PT_PresetsPanel,
    FO4_PT_AutomationPanel,
    FO4_PT_VegetationPanel,
    # New panels for comprehensive mod creation
    FO4_PT_QuestPanel,
    FO4_PT_NPCPanel,
    FO4_PT_WorldBuildingPanel,
    FO4_PT_ItemCreationPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
