"""
Operators for the Fallout 4 Tutorial Add-on
"""

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, EnumProperty, IntProperty, FloatProperty, BoolProperty
from . import tutorial_system, mesh_helpers, texture_helpers, animation_helpers, export_helpers, notification_system, image_to_mesh_helpers, hunyuan3d_helpers, gradio_helpers, hymotion_helpers, nvtt_helpers, realesrgan_helpers, get3d_helpers, stylegan2_helpers, instantngp_helpers, imageto3d_helpers, advanced_mesh_helpers

# Tutorial Operators

class FO4_OT_StartTutorial(Operator):
    """Start a tutorial"""
    bl_idname = "fo4.start_tutorial"
    bl_label = "Start Tutorial"
    bl_options = {'REGISTER', 'UNDO'}
    
    tutorial_type: EnumProperty(
        name="Tutorial",
        items=[
            ('basic_mesh', "Basic Mesh", "Learn to create basic meshes"),
            ('textures', "Textures", "Learn to setup textures"),
            ('animation', "Animation", "Learn to create animations"),
        ]
    )
    
    def execute(self, context):
        context.scene.fo4_current_tutorial = self.tutorial_type
        context.scene.fo4_tutorial_step = 0
        
        tutorial = tutorial_system.get_current_tutorial(context)
        if tutorial:
            step = tutorial.get_current_step()
            self.report({'INFO'}, f"Tutorial started: {tutorial.name}")
            self.report({'INFO'}, f"Step 1: {step.title}")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class FO4_OT_ShowHelp(Operator):
    """Show help information"""
    bl_idname = "fo4.show_help"
    bl_label = "Show Help"
    
    def execute(self, context):
        self.report({'INFO'}, "Fallout 4 Tutorial Add-on Help")
        self.report({'INFO'}, "Use the tutorial buttons to learn mod creation")
        return {'FINISHED'}

class FO4_OT_ShowMessage(Operator):
    """Show a message to the user"""
    bl_idname = "fo4.show_message"
    bl_label = "Message"
    
    message: StringProperty(name="Message")
    icon: StringProperty(name="Icon", default='INFO')
    
    def execute(self, context):
        self.report({'INFO'}, self.message)
        return {'FINISHED'}

# Mesh Operators

class FO4_OT_CreateBaseMesh(Operator):
    """Create a base mesh for Fallout 4"""
    bl_idname = "fo4.create_base_mesh"
    bl_label = "Create Base Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            obj = mesh_helpers.MeshHelpers.create_base_mesh()
            self.report({'INFO'}, f"Created base mesh: {obj.name}")
            notification_system.FO4_NotificationSystem.notify(
                f"Created base mesh: {obj.name}", 'INFO'
            )
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create mesh: {str(e)}")
            notification_system.FO4_NotificationSystem.notify(
                f"Error creating mesh: {str(e)}", 'ERROR'
            )
            return {'CANCELLED'}
        
        return {'FINISHED'}

class FO4_OT_OptimizeMesh(Operator):
    """Optimize mesh for Fallout 4"""
    bl_idname = "fo4.optimize_mesh"
    bl_label = "Optimize Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}
        
        success, message = mesh_helpers.MeshHelpers.optimize_mesh(obj)
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'INFO')
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}

class FO4_OT_ValidateMesh(Operator):
    """Validate mesh for Fallout 4 compatibility"""
    bl_idname = "fo4.validate_mesh"
    bl_label = "Validate Mesh"
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}
        
        success, issues = mesh_helpers.MeshHelpers.validate_mesh(obj)
        
        if success:
            self.report({'INFO'}, "Mesh is valid for Fallout 4!")
            notification_system.FO4_NotificationSystem.notify(
                "Mesh validation passed!", 'INFO'
            )
        else:
            self.report({'WARNING'}, "Mesh validation found issues:")
            for issue in issues:
                self.report({'WARNING'}, f"  - {issue}")
                notification_system.FO4_NotificationSystem.notify(issue, 'WARNING')
        
        return {'FINISHED'}

# Texture Operators

class FO4_OT_SetupTextures(Operator):
    """Setup Fallout 4 materials"""
    bl_idname = "fo4.setup_textures"
    bl_label = "Setup FO4 Materials"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}
        
        try:
            mat = texture_helpers.TextureHelpers.setup_fo4_material(obj)
            self.report({'INFO'}, f"Created FO4 material: {mat.name}")
            notification_system.FO4_NotificationSystem.notify(
                f"Material created: {mat.name}", 'INFO'
            )
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create material: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}

class FO4_OT_InstallTexture(Operator):
    """Install texture into material"""
    bl_idname = "fo4.install_texture"
    bl_label = "Install Texture"
    bl_options = {'REGISTER'}
    
    filepath: StringProperty(subtype='FILE_PATH')
    
    texture_type: EnumProperty(
        name="Texture Type",
        items=[
            ('DIFFUSE', "Diffuse", "Color texture"),
            ('NORMAL', "Normal", "Normal map"),
            ('SPECULAR', "Specular", "Specular map"),
        ]
    )
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}
        
        success, message = texture_helpers.TextureHelpers.install_texture(
            obj, self.filepath, self.texture_type
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'INFO')
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class FO4_OT_ValidateTextures(Operator):
    """Validate textures for Fallout 4"""
    bl_idname = "fo4.validate_textures"
    bl_label = "Validate Textures"
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}
        
        success, issues = texture_helpers.TextureHelpers.validate_textures(obj)
        
        if success:
            self.report({'INFO'}, "Textures are valid for Fallout 4!")
            notification_system.FO4_NotificationSystem.notify(
                "Texture validation passed!", 'INFO'
            )
        else:
            self.report({'WARNING'}, "Texture validation found issues:")
            for issue in issues:
                self.report({'WARNING'}, f"  - {issue}")
                notification_system.FO4_NotificationSystem.notify(issue, 'WARNING')
        
        return {'FINISHED'}

# Animation Operators

class FO4_OT_SetupArmature(Operator):
    """Setup Fallout 4 armature"""
    bl_idname = "fo4.setup_armature"
    bl_label = "Setup FO4 Armature"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            armature = animation_helpers.AnimationHelpers.setup_fo4_armature()
            self.report({'INFO'}, f"Created FO4 armature: {armature.name}")
            notification_system.FO4_NotificationSystem.notify(
                f"Armature created: {armature.name}", 'INFO'
            )
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create armature: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}

class FO4_OT_ValidateAnimation(Operator):
    """Validate animation for Fallout 4"""
    bl_idname = "fo4.validate_animation"
    bl_label = "Validate Animation"
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}
        
        success, issues = animation_helpers.AnimationHelpers.validate_animation(obj)
        
        if success:
            self.report({'INFO'}, "Animation is valid for Fallout 4!")
            notification_system.FO4_NotificationSystem.notify(
                "Animation validation passed!", 'INFO'
            )
        else:
            self.report({'WARNING'}, "Animation validation found issues:")
            for issue in issues:
                self.report({'WARNING'}, f"  - {issue}")
                notification_system.FO4_NotificationSystem.notify(issue, 'WARNING')
        
        return {'FINISHED'}

# Export Operators

class FO4_OT_ExportMesh(Operator):
    """Export mesh to NIF format"""
    bl_idname = "fo4.export_mesh"
    bl_label = "Export Mesh"
    
    filepath: StringProperty(subtype='FILE_PATH')
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}
        
        success, message = export_helpers.ExportHelpers.export_mesh_to_nif(
            obj, self.filepath
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'INFO')
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class FO4_OT_ExportAll(Operator):
    """Export complete mod"""
    bl_idname = "fo4.export_all"
    bl_label = "Export Complete Mod"
    
    directory: StringProperty(subtype='DIR_PATH')
    
    def execute(self, context):
        success, results = export_helpers.ExportHelpers.export_complete_mod(
            context.scene, self.directory
        )
        
        if success:
            self.report({'INFO'}, f"Exported {len(results['meshes'])} meshes")
            notification_system.FO4_NotificationSystem.notify(
                "Mod exported successfully!", 'INFO'
            )
        else:
            self.report({'ERROR'}, "Export failed")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class FO4_OT_ValidateExport(Operator):
    """Validate before export"""
    bl_idname = "fo4.validate_export"
    bl_label = "Validate Before Export"
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        success, issues = export_helpers.ExportHelpers.validate_before_export(obj)
        
        if success:
            self.report({'INFO'}, "Object is ready for export!")
            notification_system.FO4_NotificationSystem.notify(
                "Validation passed! Ready to export.", 'INFO'
            )
        else:
            self.report({'WARNING'}, "Validation found issues:")
            for issue in issues:
                self.report({'WARNING'}, f"  - {issue}")
                notification_system.FO4_NotificationSystem.notify(issue, 'WARNING')
        
        return {'FINISHED'}

# Image to Mesh Operators

class FO4_OT_ImageToMesh(Operator):
    """Create a mesh from an image using height map"""
    bl_idname = "fo4.image_to_mesh"
    bl_label = "Image to Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype='FILE_PATH')
    
    mesh_width: bpy.props.FloatProperty(
        name="Mesh Width",
        description="Physical width of the mesh",
        default=2.0,
        min=0.1,
        max=100.0
    )
    
    mesh_height: bpy.props.FloatProperty(
        name="Mesh Height", 
        description="Physical height of the mesh",
        default=2.0,
        min=0.1,
        max=100.0
    )
    
    displacement_strength: bpy.props.FloatProperty(
        name="Displacement Strength",
        description="Strength of the height displacement",
        default=0.5,
        min=0.0,
        max=10.0
    )
    
    subdivisions: bpy.props.IntProperty(
        name="Subdivisions",
        description="Number of subdivisions (0 = auto based on image, max 256)",
        default=0,
        min=0,
        max=256
    )
    
    def execute(self, context):
        # Validate file
        if not image_to_mesh_helpers.ImageToMeshHelpers.validate_image_file(self.filepath):
            self.report({'ERROR'}, "Unsupported image format. Use PNG, JPG, BMP, TIFF, or TGA")
            return {'CANCELLED'}
        
        # Load image as height map
        success, data, width, height = image_to_mesh_helpers.load_image_as_heightmap(self.filepath)
        
        if not success:
            self.report({'ERROR'}, data)  # data contains error message
            notification_system.FO4_NotificationSystem.notify(data, 'ERROR')
            return {'CANCELLED'}
        
        # Get object name from file
        import os
        obj_name = os.path.splitext(os.path.basename(self.filepath))[0]
        
        # Determine subdivisions
        subdivs = self.subdivisions if self.subdivisions > 0 else None
        
        # Create mesh
        success, result = image_to_mesh_helpers.create_mesh_from_heightmap(
            obj_name,
            data,
            width,
            height,
            self.mesh_width,
            self.mesh_height,
            self.displacement_strength,
            subdivs
        )
        
        if success:
            self.report({'INFO'}, f"Created mesh from image: {result.name}")
            notification_system.FO4_NotificationSystem.notify(
                f"Created mesh from {os.path.basename(self.filepath)}", 'INFO'
            )
        else:
            self.report({'ERROR'}, result)  # result contains error message
            notification_system.FO4_NotificationSystem.notify(result, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class FO4_OT_ApplyDisplacementMap(Operator):
    """Apply a displacement/height map to an existing mesh"""
    bl_idname = "fo4.apply_displacement_map"
    bl_label = "Apply Displacement Map"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype='FILE_PATH')
    
    strength: bpy.props.FloatProperty(
        name="Strength",
        description="Displacement strength",
        default=0.5,
        min=0.0,
        max=10.0
    )
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "No mesh object selected")
            return {'CANCELLED'}
        
        # Validate file
        if not image_to_mesh_helpers.ImageToMeshHelpers.validate_image_file(self.filepath):
            self.report({'ERROR'}, "Unsupported image format. Use PNG, JPG, BMP, TIFF, or TGA")
            return {'CANCELLED'}
        
        # Apply displacement
        success, message = image_to_mesh_helpers.apply_displacement_to_mesh(
            obj, self.filepath, self.strength
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'INFO')
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# AI Generation Operators (Hunyuan3D-2)

class FO4_OT_GenerateMeshFromText(Operator):
    """Generate a 3D mesh from text description using Hunyuan3D-2 AI"""
    bl_idname = "fo4.generate_mesh_from_text"
    bl_label = "Generate from Text (AI)"
    bl_options = {'REGISTER', 'UNDO'}
    
    prompt: StringProperty(
        name="Description",
        description="Text description of the 3D model to generate",
        default="A medieval sword with a golden hilt"
    )
    
    resolution: IntProperty(
        name="Resolution",
        description="Resolution of the generated mesh",
        default=256,
        min=128,
        max=512
    )
    
    def execute(self, context):
        # Check if Hunyuan3D is available
        if not hunyuan3d_helpers.Hunyuan3DHelpers.is_available():
            self.report({'ERROR'}, "Hunyuan3D-2 not available")
            self.report({'INFO'}, hunyuan3d_helpers.Hunyuan3DHelpers.get_status_message())
            notification_system.FO4_NotificationSystem.notify(
                "Hunyuan3D-2 not installed. See documentation.", 'ERROR'
            )
            return {'CANCELLED'}
        
        if not self.prompt.strip():
            self.report({'ERROR'}, "Please enter a description")
            return {'CANCELLED'}
        
        # Generate mesh from text
        success, result = hunyuan3d_helpers.generate_mesh_from_text(
            self.prompt,
            resolution=self.resolution
        )
        
        if success:
            self.report({'INFO'}, f"Generated mesh: {result.name}")
            notification_system.FO4_NotificationSystem.notify(
                f"AI generated: {result.name}", 'INFO'
            )
        else:
            self.report({'WARNING'}, result)  # result contains error message
            notification_system.FO4_NotificationSystem.notify(result, 'WARNING')
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "prompt")
        layout.prop(self, "resolution")


class FO4_OT_GenerateMeshFromImageAI(Operator):
    """Generate a full 3D mesh from an image using Hunyuan3D-2 AI"""
    bl_idname = "fo4.generate_mesh_from_image_ai"
    bl_label = "Generate from Image (AI)"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype='FILE_PATH')
    
    resolution: IntProperty(
        name="Resolution",
        description="Resolution of the generated mesh",
        default=256,
        min=128,
        max=512
    )
    
    def execute(self, context):
        # Check if Hunyuan3D is available
        if not hunyuan3d_helpers.Hunyuan3DHelpers.is_available():
            self.report({'ERROR'}, "Hunyuan3D-2 not available")
            self.report({'INFO'}, hunyuan3d_helpers.Hunyuan3DHelpers.get_status_message())
            notification_system.FO4_NotificationSystem.notify(
                "Hunyuan3D-2 not installed. See documentation.", 'ERROR'
            )
            return {'CANCELLED'}
        
        # Generate full 3D mesh from image
        success, result = hunyuan3d_helpers.generate_mesh_from_image(
            self.filepath,
            resolution=self.resolution
        )
        
        if success:
            self.report({'INFO'}, f"Generated 3D model: {result.name}")
            notification_system.FO4_NotificationSystem.notify(
                f"AI generated 3D model from image", 'INFO'
            )
        else:
            self.report({'WARNING'}, result)  # result contains error message
            notification_system.FO4_NotificationSystem.notify(result, 'WARNING')
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FO4_OT_ShowHunyuan3DInfo(Operator):
    """Show information about Hunyuan3D-2 AI integration"""
    bl_idname = "fo4.show_hunyuan3d_info"
    bl_label = "About Hunyuan3D-2"
    
    def execute(self, context):
        status = hunyuan3d_helpers.Hunyuan3DHelpers.get_status_message()
        self.report({'INFO'}, status)
        
        if not hunyuan3d_helpers.Hunyuan3DHelpers.is_available():
            instructions = hunyuan3d_helpers.Hunyuan3DHelpers.get_installation_instructions()
            print("\n" + "="*70)
            print("HUNYUAN3D-2 INSTALLATION INSTRUCTIONS")
            print("="*70)
            print(instructions)
            print("="*70)
            self.report({'INFO'}, "Installation instructions printed to console")
        
        return {'FINISHED'}

# Gradio Web Interface Operators

class FO4_OT_StartGradioServer(Operator):
    """Start Gradio web interface for AI generation"""
    bl_idname = "fo4.start_gradio_server"
    bl_label = "Start Web UI"
    bl_options = {'REGISTER'}
    
    share: bpy.props.BoolProperty(
        name="Create Public Link",
        description="Create a shareable public link (optional)",
        default=False
    )
    
    port: IntProperty(
        name="Port",
        description="Port to run the server on",
        default=7860,
        min=1024,
        max=65535
    )
    
    def execute(self, context):
        # Check if Gradio is available
        if not gradio_helpers.GradioHelpers.is_available():
            self.report({'ERROR'}, "Gradio not installed")
            self.report({'INFO'}, "Install with: pip install gradio")
            notification_system.FO4_NotificationSystem.notify(
                "Gradio not installed. See console for instructions.", 'ERROR'
            )
            return {'CANCELLED'}
        
        # Check if server already running
        if gradio_helpers.GradioHelpers.is_server_running():
            self.report({'WARNING'}, "Gradio server is already running")
            return {'CANCELLED'}
        
        # Start server
        success, message = gradio_helpers.start_gradio_server(
            share=self.share,
            port=self.port
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                "Gradio web UI started. Check console for URL.", 'INFO'
            )
            print("\n" + "="*70)
            print("GRADIO WEB INTERFACE")
            print("="*70)
            print(message)
            print("\nOpen your browser and visit the URL above.")
            print("="*70 + "\n")
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "port")
        layout.prop(self, "share")
        if self.share:
            layout.label(text="⚠️ Public link will be accessible by anyone", icon='ERROR')


class FO4_OT_StopGradioServer(Operator):
    """Stop Gradio web interface"""
    bl_idname = "fo4.stop_gradio_server"
    bl_label = "Stop Web UI"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        if not gradio_helpers.GradioHelpers.is_server_running():
            self.report({'WARNING'}, "Gradio server is not running")
            return {'CANCELLED'}
        
        success, message = gradio_helpers.stop_gradio_server()
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                "Gradio web UI stopped.", 'INFO'
            )
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}


class FO4_OT_ShowGradioInfo(Operator):
    """Show information about Gradio web interface"""
    bl_idname = "fo4.show_gradio_info"
    bl_label = "About Gradio Web UI"
    
    def execute(self, context):
        status = gradio_helpers.GradioHelpers.get_status_message()
        self.report({'INFO'}, status)
        
        if not gradio_helpers.GradioHelpers.is_available():
            instructions = gradio_helpers.GradioHelpers.get_installation_instructions()
            print("\n" + "="*70)
            print("GRADIO INSTALLATION INSTRUCTIONS")
            print("="*70)
            print(instructions)
            print("="*70)
            self.report({'INFO'}, "Installation instructions printed to console")
        else:
            print("\n" + "="*70)
            print("GRADIO WEB INTERFACE")
            print("="*70)
            print("Gradio is installed and ready to use!")
            print("\nTo start the web interface:")
            print("1. Click 'Start Web UI' button")
            print("2. Wait for the server to start")
            print("3. Open your browser to http://localhost:7860")
            print("\nThe web interface provides:")
            print("- Easy text-to-3D generation")
            print("- Simple image-to-3D generation")
            print("- User-friendly browser interface")
            print("- No command-line knowledge required")
            print("="*70 + "\n")
        
        return {'FINISHED'}

# HY-Motion-1.0 Operators

class FO4_OT_GenerateMotionFromText(Operator):
    """Generate character animation from text using HY-Motion-1.0"""
    bl_idname = "fo4.generate_motion_from_text"
    bl_label = "Generate Motion (AI)"
    bl_options = {'REGISTER', 'UNDO'}
    
    prompt: StringProperty(
        name="Motion Description",
        description="Text description of the motion/animation",
        default="character walking forward"
    )
    
    duration: bpy.props.FloatProperty(
        name="Duration (seconds)",
        description="Length of the animation",
        default=5.0,
        min=0.5,
        max=60.0
    )
    
    fps: IntProperty(
        name="FPS",
        description="Frames per second",
        default=30,
        min=24,
        max=60
    )
    
    def execute(self, context):
        # Check if HY-Motion is available
        if not hymotion_helpers.HyMotionHelpers.is_available():
            self.report({'ERROR'}, "HY-Motion-1.0 not available")
            self.report({'INFO'}, hymotion_helpers.HyMotionHelpers.get_status_message())
            notification_system.FO4_NotificationSystem.notify(
                "HY-Motion-1.0 not installed. See documentation.", 'ERROR'
            )
            return {'CANCELLED'}
        
        if not self.prompt.strip():
            self.report({'ERROR'}, "Please enter a motion description")
            return {'CANCELLED'}
        
        # Generate motion from text
        success, result = hymotion_helpers.generate_motion_from_text(
            self.prompt,
            duration=self.duration,
            fps=self.fps
        )
        
        if success:
            self.report({'INFO'}, f"Generated motion: {result}")
            notification_system.FO4_NotificationSystem.notify(
                "Motion generated successfully", 'INFO'
            )
        else:
            self.report({'WARNING'}, result)
            notification_system.FO4_NotificationSystem.notify(result, 'WARNING')
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "prompt")
        layout.prop(self, "duration")
        layout.prop(self, "fps")


class FO4_OT_ImportMotionFile(Operator):
    """Import motion file from HY-Motion-1.0"""
    bl_idname = "fo4.import_motion_file"
    bl_label = "Import Motion File"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype='FILE_PATH')
    
    filter_glob: StringProperty(
        default="*.bvh;*.fbx",
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        # Import motion file
        success, message = hymotion_helpers.import_motion_file(self.filepath)
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'INFO')
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FO4_OT_ShowHyMotionInfo(Operator):
    """Show information about HY-Motion-1.0 integration"""
    bl_idname = "fo4.show_hymotion_info"
    bl_label = "About HY-Motion-1.0"
    
    def execute(self, context):
        status = hymotion_helpers.HyMotionHelpers.get_status_message()
        self.report({'INFO'}, status)
        
        if not hymotion_helpers.HyMotionHelpers.is_available():
            instructions = hymotion_helpers.HyMotionHelpers.get_installation_instructions()
            print("\n" + "="*70)
            print("HY-MOTION-1.0 INSTALLATION INSTRUCTIONS")
            print("="*70)
            print(instructions)
            print("="*70)
            self.report({'INFO'}, "Installation instructions printed to console")
        else:
            print("\n" + "="*70)
            print("HY-MOTION-1.0 STATUS")
            print("="*70)
            print("HY-Motion-1.0 is installed and ready!")
            print("\nUse 'Generate Motion (AI)' to create animations from text.")
            print("Or use 'Import Motion File' to load .bvh or .fbx animations.")
            print("="*70 + "\n")
        
        return {'FINISHED'}

# NVIDIA Texture Tools Operators

class FO4_OT_ConvertTextureToDDS(Operator):
    """Convert a texture to DDS format using NVIDIA Texture Tools"""
    bl_idname = "fo4.convert_texture_to_dds"
    bl_label = "Convert Texture to DDS"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(
        name="Texture File",
        description="Path to the texture file to convert",
        subtype='FILE_PATH'
    )
    
    output_path: StringProperty(
        name="Output Path",
        description="Path for the output DDS file (optional)",
        subtype='FILE_PATH',
        default=""
    )
    
    compression: EnumProperty(
        name="Compression",
        description="DDS compression format",
        items=[
            ('bc1', "BC1 (DXT1)", "For diffuse textures without alpha"),
            ('bc3', "BC3 (DXT5)", "For textures with alpha channel"),
            ('bc5', "BC5 (ATI2)", "For normal maps"),
        ],
        default='bc1'
    )
    
    quality: EnumProperty(
        name="Quality",
        description="Compression quality",
        items=[
            ('fastest', "Fastest", "Fastest compression"),
            ('normal', "Normal", "Normal quality"),
            ('production', "Production", "Production quality"),
            ('highest', "Highest", "Highest quality (slowest)"),
        ],
        default='production'
    )
    
    def execute(self, context):
        # Check if NVTT is available
        if not nvtt_helpers.NVTTHelpers.is_nvtt_available():
            success, message = nvtt_helpers.NVTTHelpers.check_nvtt_installation()
            self.report({'ERROR'}, "NVIDIA Texture Tools not found")
            print("\n" + "="*70)
            print("NVIDIA TEXTURE TOOLS INSTALLATION")
            print("="*70)
            print(message)
            print("="*70 + "\n")
            notification_system.FO4_NotificationSystem.notify(
                "NVIDIA Texture Tools not installed", 'ERROR'
            )
            return {'CANCELLED'}
        
        if not self.filepath:
            self.report({'ERROR'}, "No texture file selected")
            return {'CANCELLED'}
        
        # Convert texture
        output = self.output_path if self.output_path else None
        success, message = nvtt_helpers.NVTTHelpers.convert_to_dds(
            self.filepath,
            output,
            self.compression,
            self.quality
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                "Texture converted to DDS successfully", 'INFO'
            )
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FO4_OT_ConvertObjectTexturesToDDS(Operator):
    """Convert all textures from selected object to DDS format"""
    bl_idname = "fo4.convert_object_textures_to_dds"
    bl_label = "Convert Object Textures to DDS"
    bl_options = {'REGISTER', 'UNDO'}
    
    output_dir: StringProperty(
        name="Output Directory",
        description="Directory to save converted DDS files",
        subtype='DIR_PATH'
    )
    
    def execute(self, context):
        # Check if NVTT is available
        if not nvtt_helpers.NVTTHelpers.is_nvtt_available():
            success, message = nvtt_helpers.NVTTHelpers.check_nvtt_installation()
            self.report({'ERROR'}, "NVIDIA Texture Tools not found")
            print("\n" + "="*70)
            print("NVIDIA TEXTURE TOOLS INSTALLATION")
            print("="*70)
            print(message)
            print("="*70 + "\n")
            notification_system.FO4_NotificationSystem.notify(
                "NVIDIA Texture Tools not installed", 'ERROR'
            )
            return {'CANCELLED'}
        
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        if not self.output_dir:
            self.report({'ERROR'}, "No output directory selected")
            return {'CANCELLED'}
        
        # Convert textures
        success, message, converted_files = nvtt_helpers.NVTTHelpers.convert_object_textures(
            obj,
            self.output_dir
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'INFO')
            
            # Print details
            print("\n" + "="*70)
            print("TEXTURE CONVERSION RESULTS")
            print("="*70)
            print(f"Object: {obj.name}")
            print(f"Converted files:")
            for filepath in converted_files:
                print(f"  - {filepath}")
            print("="*70 + "\n")
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FO4_OT_CheckNVTTInstallation(Operator):
    """Check if NVIDIA Texture Tools is installed"""
    bl_idname = "fo4.check_nvtt_installation"
    bl_label = "Check NVTT Installation"
    
    def execute(self, context):
        success, message = nvtt_helpers.NVTTHelpers.check_nvtt_installation()
        
        if success:
            self.report({'INFO'}, message)
            print("\n" + "="*70)
            print("NVIDIA TEXTURE TOOLS STATUS")
            print("="*70)
            print("✅ NVIDIA Texture Tools is installed and ready!")
            print(message)
            print("\nYou can now convert textures to DDS format for Fallout 4.")
            print("="*70 + "\n")
        else:
            self.report({'WARNING'}, "NVIDIA Texture Tools not found")
            print("\n" + "="*70)
            print("NVIDIA TEXTURE TOOLS INSTALLATION")
            print("="*70)
            print(message)
            print("\nFor detailed instructions, see NVIDIA_RESOURCES.md")
            print("="*70 + "\n")
        
        return {'FINISHED'}

# Real-ESRGAN Operators

class FO4_OT_UpscaleTexture(Operator):
    """Upscale a texture using Real-ESRGAN AI"""
    bl_idname = "fo4.upscale_texture"
    bl_label = "Upscale Texture with AI"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(
        name="Texture File",
        description="Path to the texture file to upscale",
        subtype='FILE_PATH'
    )
    
    output_path: StringProperty(
        name="Output Path",
        description="Path for the upscaled texture (optional)",
        subtype='FILE_PATH',
        default=""
    )
    
    scale: EnumProperty(
        name="Upscale Factor",
        description="How much to upscale the texture",
        items=[
            ('2', "2x", "Double the resolution"),
            ('4', "4x", "Quadruple the resolution"),
        ],
        default='4'
    )
    
    def execute(self, context):
        # Check if Real-ESRGAN is available
        if not realesrgan_helpers.RealESRGANHelpers.is_realesrgan_available():
            success, message = realesrgan_helpers.RealESRGANHelpers.check_realesrgan_installation()
            self.report({'ERROR'}, "Real-ESRGAN not found")
            print("\n" + "="*70)
            print("REAL-ESRGAN INSTALLATION")
            print("="*70)
            print(message)
            print("="*70 + "\n")
            notification_system.FO4_NotificationSystem.notify(
                "Real-ESRGAN not installed", 'ERROR'
            )
            return {'CANCELLED'}
        
        if not self.filepath:
            self.report({'ERROR'}, "No texture file selected")
            return {'CANCELLED'}
        
        # Upscale texture
        output = self.output_path if self.output_path else None
        scale_int = int(self.scale)
        
        success, message = realesrgan_helpers.RealESRGANHelpers.upscale_texture(
            self.filepath,
            output,
            scale_int
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                f"Texture upscaled {scale_int}x successfully", 'INFO'
            )
        else:
            self.report({'WARNING'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'WARNING')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FO4_OT_UpscaleObjectTextures(Operator):
    """Upscale all textures from selected object using Real-ESRGAN AI"""
    bl_idname = "fo4.upscale_object_textures"
    bl_label = "Upscale Object Textures with AI"
    bl_options = {'REGISTER', 'UNDO'}
    
    output_dir: StringProperty(
        name="Output Directory",
        description="Directory to save upscaled textures",
        subtype='DIR_PATH'
    )
    
    scale: EnumProperty(
        name="Upscale Factor",
        description="How much to upscale the textures",
        items=[
            ('2', "2x", "Double the resolution"),
            ('4', "4x", "Quadruple the resolution"),
        ],
        default='4'
    )
    
    def execute(self, context):
        # Check if Real-ESRGAN is available
        if not realesrgan_helpers.RealESRGANHelpers.is_realesrgan_available():
            success, message = realesrgan_helpers.RealESRGANHelpers.check_realesrgan_installation()
            self.report({'ERROR'}, "Real-ESRGAN not found")
            print("\n" + "="*70)
            print("REAL-ESRGAN INSTALLATION")
            print("="*70)
            print(message)
            print("="*70 + "\n")
            notification_system.FO4_NotificationSystem.notify(
                "Real-ESRGAN not installed", 'ERROR'
            )
            return {'CANCELLED'}
        
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        if not self.output_dir:
            self.report({'ERROR'}, "No output directory selected")
            return {'CANCELLED'}
        
        scale_int = int(self.scale)
        
        # Upscale textures
        success, message, upscaled_files = realesrgan_helpers.RealESRGANHelpers.upscale_object_textures(
            obj,
            self.output_dir,
            scale_int
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'INFO')
            
            # Print details
            print("\n" + "="*70)
            print("TEXTURE UPSCALING RESULTS")
            print("="*70)
            print(f"Object: {obj.name}")
            print(f"Scale: {scale_int}x")
            print(f"Upscaled files:")
            for filepath in upscaled_files:
                print(f"  - {filepath}")
            print("="*70 + "\n")
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FO4_OT_CheckRealESRGANInstallation(Operator):
    """Check if Real-ESRGAN is installed"""
    bl_idname = "fo4.check_realesrgan_installation"
    bl_label = "Check Real-ESRGAN Installation"
    
    def execute(self, context):
        success, message = realesrgan_helpers.RealESRGANHelpers.check_realesrgan_installation()
        
        if success:
            self.report({'INFO'}, message)
            print("\n" + "="*70)
            print("REAL-ESRGAN STATUS")
            print("="*70)
            print("✅ Real-ESRGAN is installed and ready!")
            print(message)
            print("\nYou can now upscale textures using AI.")
            print("Recommended for:")
            print("  - Enhancing low-resolution textures")
            print("  - Improving texture quality for FO4 mods")
            print("  - Upscaling 512x512 to 2048x2048 or 4096x4096")
            print("="*70 + "\n")
        else:
            self.report({'WARNING'}, "Real-ESRGAN not found")
            print("\n" + "="*70)
            print("REAL-ESRGAN INSTALLATION")
            print("="*70)
            print(message)
            print("\nFor detailed instructions, see NVIDIA_RESOURCES.md")
            print("="*70 + "\n")
        
        return {'FINISHED'}

# NVIDIA GET3D Operators

class FO4_OT_ImportGET3DMesh(Operator):
    """Import a mesh generated by NVIDIA GET3D"""
    bl_idname = "fo4.import_get3d_mesh"
    bl_label = "Import GET3D Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(
        name="GET3D Mesh File",
        description="Path to .obj file generated by GET3D",
        subtype='FILE_PATH'
    )
    
    filter_glob: StringProperty(
        default="*.obj",
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        if not self.filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}
        
        # Import GET3D mesh
        success, message, imported_obj = get3d_helpers.GET3DHelpers.import_get3d_mesh(
            self.filepath
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                f"GET3D mesh imported: {imported_obj.name}", 'INFO'
            )
            
            print("\n" + "="*70)
            print("GET3D MESH IMPORTED")
            print("="*70)
            print(f"Mesh: {imported_obj.name}")
            print(f"File: {self.filepath}")
            print("\nNext steps:")
            print("1. Use 'Optimize GET3D Mesh' to prepare for FO4")
            print("2. Add textures with 'Setup FO4 Materials'")
            print("3. Validate and export")
            print("="*70 + "\n")
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FO4_OT_OptimizeGET3DMesh(Operator):
    """Optimize a GET3D mesh for Fallout 4"""
    bl_idname = "fo4.optimize_get3d_mesh"
    bl_label = "Optimize GET3D Mesh for FO4"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        if obj.type != 'MESH':
            self.report({'ERROR'}, "Selected object is not a mesh")
            return {'CANCELLED'}
        
        # Optimize mesh for FO4
        success, message = get3d_helpers.GET3DHelpers.optimize_get3d_mesh_for_fo4(obj)
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                "GET3D mesh optimized for Fallout 4", 'INFO'
            )
        else:
            self.report({'WARNING'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'WARNING')
        
        return {'FINISHED'}


class FO4_OT_ShowGET3DInfo(Operator):
    """Show information about NVIDIA GET3D"""
    bl_idname = "fo4.show_get3d_info"
    bl_label = "About GET3D"
    
    def execute(self, context):
        success, message = get3d_helpers.GET3DHelpers.check_get3d_installation()
        
        if success:
            self.report({'INFO'}, "GET3D is available")
            print("\n" + "="*70)
            print("NVIDIA GET3D STATUS")
            print("="*70)
            print(message)
            print("\nAvailable models:")
            models = get3d_helpers.GET3DHelpers.list_available_models()
            if models:
                for model in models:
                    print(f"  - {os.path.basename(model)}")
            else:
                print("  No models found. Download pre-trained models from NVIDIA.")
            print("="*70 + "\n")
        else:
            self.report({'WARNING'}, "GET3D not found")
            print("\n" + "="*70)
            print("NVIDIA GET3D INSTALLATION")
            print("="*70)
            print(message)
            print("\nFor detailed instructions, see NVIDIA_RESOURCES.md")
            print("="*70 + "\n")
        
        # Show workflow guide
        guide = get3d_helpers.GET3DHelpers.create_simple_workflow_guide()
        print("\n" + guide)
        
        return {'FINISHED'}


class FO4_OT_CheckGET3DInstallation(Operator):
    """Check if NVIDIA GET3D is installed"""
    bl_idname = "fo4.check_get3d_installation"
    bl_label = "Check GET3D Installation"
    
    def execute(self, context):
        success, message = get3d_helpers.GET3DHelpers.check_get3d_installation()
        
        if success:
            self.report({'INFO'}, message)
            print("\n" + "="*70)
            print("NVIDIA GET3D STATUS")
            print("="*70)
            print("✅ GET3D is installed and ready!")
            print(message)
            print("\nYou can now:")
            print("  - Generate 3D meshes with AI")
            print("  - Import GET3D generated models")
            print("  - Optimize for Fallout 4")
            print("\nNote: Mesh generation runs outside Blender")
            print("Use 'About GET3D' for workflow guide")
            print("="*70 + "\n")
        else:
            self.report({'WARNING'}, "GET3D not found")
            print("\n" + "="*70)
            print("NVIDIA GET3D INSTALLATION")
            print("="*70)
            print(message)
            print("\nFor detailed instructions, see NVIDIA_RESOURCES.md")
            print("="*70 + "\n")
        
        return {'FINISHED'}

# StyleGAN2 Operators

class FO4_OT_GenerateTextureStyleGAN2(Operator):
    """Generate texture using StyleGAN2 AI"""
    bl_idname = "fo4.generate_texture_stylegan2"
    bl_label = "Generate Texture (StyleGAN2)"
    bl_options = {'REGISTER', 'UNDO'}
    
    output_dir: StringProperty(
        name="Output Directory",
        description="Directory to save generated textures",
        subtype='DIR_PATH'
    )
    
    num_textures: IntProperty(
        name="Number of Textures",
        description="How many textures to generate",
        default=5,
        min=1,
        max=100
    )
    
    seed_start: IntProperty(
        name="Seed Start",
        description="Starting seed for texture generation",
        default=0,
        min=0
    )
    
    def execute(self, context):
        # Check if StyleGAN2 is available
        if not stylegan2_helpers.StyleGAN2Helpers.is_stylegan2_available():
            success, message = stylegan2_helpers.StyleGAN2Helpers.check_stylegan2_installation()
            self.report({'ERROR'}, "StyleGAN2 not found")
            print("\n" + "="*70)
            print("STYLEGAN2 INSTALLATION")
            print("="*70)
            print(message)
            print("="*70 + "\n")
            notification_system.FO4_NotificationSystem.notify(
                "StyleGAN2 not installed", 'ERROR'
            )
            return {'CANCELLED'}
        
        if not self.output_dir:
            self.report({'ERROR'}, "No output directory selected")
            return {'CANCELLED'}
        
        # Generate textures (returns instructions)
        success, message = stylegan2_helpers.StyleGAN2Helpers.batch_generate_textures(
            self.output_dir,
            self.num_textures,
            self.seed_start
        )
        
        self.report({'INFO'}, "See console for generation instructions")
        print("\n" + "="*70)
        print("STYLEGAN2 TEXTURE GENERATION")
        print("="*70)
        print(message)
        print("="*70 + "\n")
        
        notification_system.FO4_NotificationSystem.notify(
            "StyleGAN2 generation instructions printed to console", 'INFO'
        )
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "output_dir")
        layout.prop(self, "num_textures")
        layout.prop(self, "seed_start")


class FO4_OT_ImportStyleGAN2Texture(Operator):
    """Import a StyleGAN2 generated texture to object material"""
    bl_idname = "fo4.import_stylegan2_texture"
    bl_label = "Import StyleGAN2 Texture"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(
        name="Texture File",
        description="Path to StyleGAN2 generated texture",
        subtype='FILE_PATH'
    )
    
    filter_glob: StringProperty(
        default="*.png;*.jpg;*.jpeg",
        options={'HIDDEN'}
    )
    
    texture_type: EnumProperty(
        name="Texture Type",
        description="Type of texture to import",
        items=[
            ('DIFFUSE', "Diffuse", "Diffuse/Albedo texture"),
            ('NORMAL', "Normal", "Normal map"),
            ('SPECULAR', "Specular", "Specular map"),
        ],
        default='DIFFUSE'
    )
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        if not self.filepath:
            self.report({'ERROR'}, "No texture file selected")
            return {'CANCELLED'}
        
        # Import texture
        success, message = stylegan2_helpers.StyleGAN2Helpers.import_texture_to_material(
            self.filepath,
            obj,
            self.texture_type
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                f"StyleGAN2 texture imported as {self.texture_type}", 'INFO'
            )
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FO4_OT_ShowStyleGAN2Info(Operator):
    """Show information about StyleGAN2 texture generation"""
    bl_idname = "fo4.show_stylegan2_info"
    bl_label = "About StyleGAN2"
    
    def execute(self, context):
        success, message = stylegan2_helpers.StyleGAN2Helpers.check_stylegan2_installation()
        
        if success:
            self.report({'INFO'}, "StyleGAN2 is available")
            print("\n" + "="*70)
            print("STYLEGAN2 STATUS")
            print("="*70)
            print(message)
            print("\nAvailable models:")
            models = stylegan2_helpers.StyleGAN2Helpers.list_available_models()
            if models:
                for model in models:
                    print(f"  - {os.path.basename(model)}")
            else:
                print("  No models found. Download pre-trained models from NVIDIA.")
            print("\nTexture categories:")
            categories = stylegan2_helpers.StyleGAN2Helpers.get_texture_categories()
            for cat in categories:
                print(f"  - {cat}")
            print("="*70 + "\n")
        else:
            self.report({'WARNING'}, "StyleGAN2 not found")
            print("\n" + "="*70)
            print("STYLEGAN2 INSTALLATION")
            print("="*70)
            print(message)
            print("\nFor detailed instructions, see NVIDIA_RESOURCES.md")
            print("="*70 + "\n")
        
        # Show workflow guide
        guide = stylegan2_helpers.StyleGAN2Helpers.create_workflow_guide()
        print("\n" + guide)
        
        return {'FINISHED'}


class FO4_OT_CheckStyleGAN2Installation(Operator):
    """Check if StyleGAN2 is installed"""
    bl_idname = "fo4.check_stylegan2_installation"
    bl_label = "Check StyleGAN2 Installation"
    
    def execute(self, context):
        success, message = stylegan2_helpers.StyleGAN2Helpers.check_stylegan2_installation()
        
        if success:
            self.report({'INFO'}, message)
            print("\n" + "="*70)
            print("STYLEGAN2 STATUS")
            print("="*70)
            print("✅ StyleGAN2 is installed and ready!")
            print(message)
            print("\nYou can now:")
            print("  - Generate unique textures with AI")
            print("  - Create custom diffuse maps")
            print("  - Generate variations quickly")
            print("\nNote: Texture generation runs outside Blender")
            print("Use 'About StyleGAN2' for workflow guide")
            
            settings = stylegan2_helpers.StyleGAN2Helpers.get_recommended_settings()
            print("\nRecommended settings:")
            for key, value in settings.items():
                print(f"  {key}: {value}")
            print("="*70 + "\n")
        else:
            self.report({'WARNING'}, "StyleGAN2 not found")
            print("\n" + "="*70)
            print("STYLEGAN2 INSTALLATION")
            print("="*70)
            print(message)
            print("\nFor detailed instructions, see NVIDIA_RESOURCES.md")
            print("="*70 + "\n")
        
        return {'FINISHED'}

# Instant-NGP Operators

class FO4_OT_ReconstructFromImages(Operator):
    """Reconstruct 3D mesh from images using Instant-NGP (NeRF)"""
    bl_idname = "fo4.reconstruct_from_images"
    bl_label = "Reconstruct from Images (Instant-NGP)"
    bl_options = {'REGISTER'}
    
    images_dir: StringProperty(
        name="Images Directory",
        description="Directory containing input images for reconstruction",
        subtype='DIR_PATH'
    )
    
    output_path: StringProperty(
        name="Output Mesh",
        description="Path for output mesh file",
        subtype='FILE_PATH',
        default="reconstruction.obj"
    )
    
    def execute(self, context):
        # Check if Instant-NGP is available
        if not instantngp_helpers.InstantNGPHelpers.is_instantngp_available():
            success, message = instantngp_helpers.InstantNGPHelpers.check_instantngp_installation()
            self.report({'ERROR'}, "Instant-NGP not found")
            print("\n" + "="*70)
            print("INSTANT-NGP INSTALLATION")
            print("="*70)
            print(message)
            print("="*70 + "\n")
            notification_system.FO4_NotificationSystem.notify(
                "Instant-NGP not installed", 'ERROR'
            )
            return {'CANCELLED'}
        
        if not self.images_dir:
            self.report({'ERROR'}, "No images directory selected")
            return {'CANCELLED'}
        
        # Reconstruct (returns instructions)
        success, message = instantngp_helpers.InstantNGPHelpers.reconstruct_from_images(
            self.images_dir,
            self.output_path
        )
        
        self.report({'INFO'}, "See console for reconstruction instructions")
        print("\n" + "="*70)
        print("INSTANT-NGP 3D RECONSTRUCTION")
        print("="*70)
        print(message)
        print("="*70 + "\n")
        
        notification_system.FO4_NotificationSystem.notify(
            "Instant-NGP reconstruction instructions printed to console", 'INFO'
        )
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=450)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "images_dir")
        layout.prop(self, "output_path")


class FO4_OT_ImportInstantNGPMesh(Operator):
    """Import a mesh reconstructed by Instant-NGP"""
    bl_idname = "fo4.import_instantngp_mesh"
    bl_label = "Import Instant-NGP Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(
        name="Instant-NGP Mesh File",
        description="Path to .obj file reconstructed by Instant-NGP",
        subtype='FILE_PATH'
    )
    
    filter_glob: StringProperty(
        default="*.obj",
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        if not self.filepath:
            self.report({'ERROR'}, "No file selected")
            return {'CANCELLED'}
        
        # Import Instant-NGP mesh
        success, message, imported_obj = instantngp_helpers.InstantNGPHelpers.import_instantngp_mesh(
            self.filepath
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                f"Instant-NGP mesh imported: {imported_obj.name}", 'INFO'
            )
            
            print("\n" + "="*70)
            print("INSTANT-NGP MESH IMPORTED")
            print("="*70)
            print(f"Mesh: {imported_obj.name}")
            print(f"File: {self.filepath}")
            print(f"Polygons: {len(imported_obj.data.polygons)}")
            print("\nNext steps:")
            print("1. Use 'Optimize NeRF Mesh' to prepare for FO4")
            print("2. NeRF meshes often need decimation")
            print("3. Setup materials and textures")
            print("4. Validate and export")
            print("="*70 + "\n")
        else:
            self.report({'ERROR'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'ERROR')
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class FO4_OT_OptimizeNERFMesh(Operator):
    """Optimize an Instant-NGP NeRF mesh for Fallout 4"""
    bl_idname = "fo4.optimize_nerf_mesh"
    bl_label = "Optimize NeRF Mesh for FO4"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        if obj.type != 'MESH':
            self.report({'ERROR'}, "Selected object is not a mesh")
            return {'CANCELLED'}
        
        poly_count_before = len(obj.data.polygons)
        
        # Optimize mesh for FO4
        success, message = instantngp_helpers.InstantNGPHelpers.optimize_nerf_mesh_for_fo4(obj)
        
        poly_count_after = len(obj.data.polygons)
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                f"NeRF mesh optimized: {poly_count_before} → {poly_count_after} polygons", 'INFO'
            )
            
            print("\n" + "="*70)
            print("NERF MESH OPTIMIZATION")
            print("="*70)
            print(f"Before: {poly_count_before} polygons")
            print(f"After: {poly_count_after} polygons")
            print(f"Reduction: {((poly_count_before - poly_count_after) / poly_count_before * 100):.1f}%")
            print("="*70 + "\n")
        else:
            self.report({'WARNING'}, message)
            notification_system.FO4_NotificationSystem.notify(message, 'WARNING')
        
        return {'FINISHED'}


class FO4_OT_ShowInstantNGPInfo(Operator):
    """Show information about Instant-NGP reconstruction"""
    bl_idname = "fo4.show_instantngp_info"
    bl_label = "About Instant-NGP"
    
    def execute(self, context):
        success, message = instantngp_helpers.InstantNGPHelpers.check_instantngp_installation()
        
        if success:
            self.report({'INFO'}, "Instant-NGP is available")
            print("\n" + "="*70)
            print("INSTANT-NGP STATUS")
            print("="*70)
            print(message)
            
            settings = instantngp_helpers.InstantNGPHelpers.get_recommended_settings()
            print("\nRecommended settings:")
            for key, value in settings.items():
                print(f"  {key}: {value}")
            
            print("\nEstimated training time:")
            print(f"  100 images with RTX GPU: {instantngp_helpers.InstantNGPHelpers.estimate_training_time(100, True)}")
            print(f"  100 images without RTX: {instantngp_helpers.InstantNGPHelpers.estimate_training_time(100, False)}")
            print("="*70 + "\n")
        else:
            self.report({'WARNING'}, "Instant-NGP not found")
            print("\n" + "="*70)
            print("INSTANT-NGP INSTALLATION")
            print("="*70)
            print(message)
            print("\nFor detailed instructions, see NVIDIA_RESOURCES.md")
            print("="*70 + "\n")
        
        # Show workflow guide
        guide = instantngp_helpers.InstantNGPHelpers.create_workflow_guide()
        print("\n" + guide)
        
        return {'FINISHED'}


class FO4_OT_CheckInstantNGPInstallation(Operator):
    """Check if Instant-NGP is installed"""
    bl_idname = "fo4.check_instantngp_installation"
    bl_label = "Check Instant-NGP Installation"
    
    def execute(self, context):
        success, message = instantngp_helpers.InstantNGPHelpers.check_instantngp_installation()
        
        if success:
            self.report({'INFO'}, message)
            print("\n" + "="*70)
            print("INSTANT-NGP STATUS")
            print("="*70)
            print("✅ Instant-NGP is installed and ready!")
            print(message)
            print("\nYou can now:")
            print("  - Reconstruct 3D from photos")
            print("  - Create meshes using NeRF technology")
            print("  - Import and optimize for Fallout 4")
            print("\nNote: Reconstruction runs in Instant-NGP application")
            print("Use 'About Instant-NGP' for workflow guide")
            print("="*70 + "\n")
        else:
            self.report({'WARNING'}, "Instant-NGP not found")
            print("\n" + "="*70)
            print("INSTANT-NGP INSTALLATION")
            print("="*70)
            print(message)
            print("\nFor detailed instructions, see NVIDIA_RESOURCES.md")
            print("="*70 + "\n")
        
        return {'FINISHED'}

# Image-to-3D Comparison and Status Operators

class FO4_OT_ShowImageTo3DComparison(Operator):
    """Show comparison of all available image-to-3D methods"""
    bl_idname = "fo4.show_imageto3d_comparison"
    bl_label = "Compare Image-to-3D Methods"
    
    def execute(self, context):
        # Show comparison guide
        guide = imageto3d_helpers.ImageTo3DHelpers.create_comparison_guide()
        print("\n" + guide)
        
        # Show installation status
        print("\n" + "="*70)
        print("INSTALLATION STATUS")
        print("="*70)
        
        status = imageto3d_helpers.ImageTo3DHelpers.get_installation_status()
        for name, (installed, message) in status.items():
            icon = "✅" if installed else "❌"
            print(f"{icon} {name}")
            if not installed:
                print(f"   Install: See guide above")
        
        print("="*70 + "\n")
        
        self.report({'INFO'}, "Image-to-3D comparison printed to console")
        notification_system.FO4_NotificationSystem.notify(
            "Image-to-3D comparison guide available in console", 'INFO'
        )
        
        return {'FINISHED'}


class FO4_OT_CheckAllImageTo3D(Operator):
    """Check installation status of all image-to-3D tools"""
    bl_idname = "fo4.check_all_imageto3d"
    bl_label = "Check All Image-to-3D Tools"
    
    def execute(self, context):
        print("\n" + "="*70)
        print("IMAGE-TO-3D TOOLS STATUS")
        print("="*70)
        
        # Check each tool
        tools = [
            ('TripoSR', imageto3d_helpers.ImageTo3DHelpers.check_triposr_installation),
            ('DreamGaussian', imageto3d_helpers.ImageTo3DHelpers.check_dreamgaussian_installation),
            ('Shap-E', imageto3d_helpers.ImageTo3DHelpers.check_shap_e_installation),
            ('Instant-NGP', instantngp_helpers.InstantNGPHelpers.check_instantngp_installation),
            ('GET3D', get3d_helpers.GET3DHelpers.check_get3d_installation),
            ('Hunyuan3D-2', hunyuan3d_helpers.Hunyuan3DHelpers.check_installation),
        ]
        
        installed_count = 0
        total_count = len(tools)
        
        for name, check_func in tools:
            try:
                installed, message = check_func()
                icon = "✅" if installed else "❌"
                print(f"\n{icon} {name}")
                if installed:
                    installed_count += 1
                    # Show first line of message
                    first_line = message.split('\n')[0]
                    print(f"   {first_line}")
                else:
                    print(f"   Not installed")
            except Exception as e:
                print(f"❌ {name}")
                print(f"   Error checking: {e}")
        
        print("\n" + "="*70)
        print(f"Summary: {installed_count}/{total_count} tools installed")
        print("="*70)
        
        # Show available methods
        available = imageto3d_helpers.ImageTo3DHelpers.get_available_methods()
        print("\nAvailable methods:")
        for method_id, name, description in available:
            print(f"  • {name}: {description}")
        
        print("\n" + "="*70 + "\n")
        
        self.report({'INFO'}, f"{installed_count}/{total_count} image-to-3D tools available")
        
        return {'FINISHED'}


class FO4_OT_SuggestImageTo3DMethod(Operator):
    """Get suggestion for best image-to-3D method"""
    bl_idname = "fo4.suggest_imageto3d_method"
    bl_label = "Suggest Best Method"
    
    use_case: EnumProperty(
        name="Use Case",
        items=[
            ('speed', "Speed", "Fastest conversion"),
            ('quality', "Quality", "Best quality output"),
            ('ease', "Ease of Use", "Easiest to setup"),
            ('terrain', "Terrain", "Height maps and terrain"),
            ('photos', "Photos", "Multiple photo reconstruction"),
            ('texture', "Textures", "Texture generation"),
        ],
        default='speed'
    )
    
    def execute(self, context):
        suggestion = imageto3d_helpers.ImageTo3DHelpers.suggest_best_method(self.use_case)
        
        self.report({'INFO'}, suggestion)
        print("\n" + "="*70)
        print("RECOMMENDATION")
        print("="*70)
        print(f"Use Case: {self.use_case}")
        print(f"Suggestion: {suggestion}")
        print("="*70 + "\n")
        
        notification_system.FO4_NotificationSystem.notify(
            f"Recommended: {suggestion.split(' - ')[0]}", 'INFO'
        )
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# TripoSR Texture Generation Operators

class FO4_OT_GenerateTripoSRTexture(Operator):
    """Generate enhanced textures for TripoSR mesh"""
    bl_idname = "fo4.generate_triposr_texture"
    bl_label = "Generate TripoSR Textures"
    bl_options = {'REGISTER'}
    
    mesh_path: StringProperty(
        name="Mesh File",
        description="Path to TripoSR generated mesh",
        subtype='FILE_PATH'
    )
    
    reference_image: StringProperty(
        name="Reference Image",
        description="Original image used for 3D generation",
        subtype='FILE_PATH'
    )
    
    output_dir: StringProperty(
        name="Output Directory",
        description="Directory for generated textures",
        subtype='DIR_PATH'
    )
    
    def execute(self, context):
        # Check if texture gen is available
        success, message = imageto3d_helpers.ImageTo3DHelpers.check_triposr_texture_gen_installation()
        
        if not success:
            self.report({'ERROR'}, "triposr-texture-gen not installed")
            print("\n" + "="*70)
            print("TRIPOSR TEXTURE GENERATION")
            print("="*70)
            print(message)
            print("="*70 + "\n")
            notification_system.FO4_NotificationSystem.notify(
                "triposr-texture-gen not installed", 'ERROR'
            )
            return {'CANCELLED'}
        
        if not self.mesh_path or not self.reference_image:
            self.report({'ERROR'}, "Mesh and reference image required")
            return {'CANCELLED'}
        
        # Generate textures (returns instructions)
        success, msg, texture_paths = imageto3d_helpers.ImageTo3DHelpers.generate_texture_for_triposr_mesh(
            self.mesh_path,
            self.reference_image,
            self.output_dir
        )
        
        self.report({'INFO'}, "See console for texture generation instructions")
        print("\n" + "="*70)
        print("TRIPOSR TEXTURE GENERATION")
        print("="*70)
        print(msg)
        print("="*70 + "\n")
        
        notification_system.FO4_NotificationSystem.notify(
            "Texture generation instructions in console", 'INFO'
        )
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "mesh_path")
        layout.prop(self, "reference_image")
        layout.prop(self, "output_dir")


class FO4_OT_ShowTripoSRWorkflow(Operator):
    """Show complete TripoSR workflow with texture generation"""
    bl_idname = "fo4.show_triposr_workflow"
    bl_label = "TripoSR Complete Workflow"
    
    def execute(self, context):
        # Show workflow guide
        guide = imageto3d_helpers.ImageTo3DHelpers.create_triposr_complete_workflow_guide()
        print("\n" + guide)
        
        self.report({'INFO'}, "Complete TripoSR workflow printed to console")
        notification_system.FO4_NotificationSystem.notify(
            "TripoSR workflow guide available in console", 'INFO'
        )
        
        return {'FINISHED'}


class FO4_OT_CheckTripoSRTextureGen(Operator):
    """Check triposr-texture-gen installation"""
    bl_idname = "fo4.check_triposr_texture_gen"
    bl_label = "Check TripoSR Texture Gen"
    
    def execute(self, context):
        success, message = imageto3d_helpers.ImageTo3DHelpers.check_triposr_texture_gen_installation()
        
        if success:
            self.report({'INFO'}, message)
            print("\n" + "="*70)
            print("TRIPOSR TEXTURE GENERATION STATUS")
            print("="*70)
            print("✅ triposr-texture-gen is installed and ready!")
            print(message)
            print("\nYou can now:")
            print("  - Generate enhanced textures for TripoSR meshes")
            print("  - Create PBR materials (diffuse, normal, roughness)")
            print("  - Optimize UV layouts automatically")
            print("\nUse 'Generate TripoSR Textures' operator")
            print("See 'TripoSR Complete Workflow' for full guide")
            print("="*70 + "\n")
        else:
            self.report({'WARNING'}, "triposr-texture-gen not found")
            print("\n" + "="*70)
            print("TRIPOSR TEXTURE GENERATION INSTALLATION")
            print("="*70)
            print(message)
            print("\nFor workflow guide, use 'TripoSR Complete Workflow' operator")
            print("="*70 + "\n")
        
        return {'FINISHED'}

# Stereo/Multi-View 3D Generation Operators

class FO4_OT_GenerateFromStereo(Operator):
    """Generate 3D from stereo image pair"""
    bl_idname = "fo4.generate_from_stereo"
    bl_label = "Generate from Stereo Images"
    bl_options = {'REGISTER'}
    
    left_image: StringProperty(
        name="Left Image",
        subtype='FILE_PATH'
    )
    
    right_image: StringProperty(
        name="Right Image",
        subtype='FILE_PATH'
    )
    
    output_path: StringProperty(
        name="Output Mesh",
        subtype='FILE_PATH',
        default="stereo_output.obj"
    )
    
    def execute(self, context):
        success, message = imageto3d_helpers.ImageTo3DHelpers.check_stereo_triposr_installation()
        
        if not success:
            self.report({'ERROR'}, "Stereo TripoSR not installed")
            print("\n" + "="*70)
            print(message)
            print("="*70 + "\n")
            return {'CANCELLED'}
        
        if not self.left_image or not self.right_image:
            self.report({'ERROR'}, "Both left and right images required")
            return {'CANCELLED'}
        
        success, msg, output = imageto3d_helpers.ImageTo3DHelpers.generate_from_stereo_images(
            self.left_image, self.right_image, self.output_path
        )
        
        print("\n" + "="*70)
        print("STEREO 3D GENERATION")
        print("="*70)
        print(msg)
        print("="*70 + "\n")
        
        self.report({'INFO'}, "See console for instructions")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)


class FO4_OT_CheckStereoTripoSR(Operator):
    """Check stereo TripoSR installation"""
    bl_idname = "fo4.check_stereo_triposr"
    bl_label = "Check Stereo TripoSR"
    
    def execute(self, context):
        success, message = imageto3d_helpers.ImageTo3DHelpers.check_stereo_triposr_installation()
        
        print("\n" + "="*70)
        print("STEREO TRIPOSR STATUS")
        print("="*70)
        print(message)
        print("="*70 + "\n")
        
        if success:
            self.report({'INFO'}, "Stereo TripoSR available")
        else:
            self.report({'WARNING'}, "Not installed")
        
        return {'FINISHED'}

# Advanced Mesh Analysis and Repair Operators

class FO4_OT_AnalyzeMeshQuality(Operator):
    """Analyze mesh quality and identify issues"""
    bl_idname = "fo4.analyze_mesh_quality"
    bl_label = "Analyze Mesh Quality"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        # Analyze mesh
        scores, issues, details = advanced_mesh_helpers.AdvancedMeshHelpers.analyze_mesh_quality(obj)
        
        if scores is None:
            self.report({'ERROR'}, issues[0])
            return {'CANCELLED'}
        
        # Report results
        self.report({'INFO'}, f"Overall Quality: {scores['overall']:.1f}/100")
        
        print("\n" + "="*70)
        print("MESH QUALITY ANALYSIS")
        print("="*70)
        print(f"Object: {obj.name}")
        print(f"\nQuality Scores:")
        print(f"  Overall:  {scores['overall']:.1f}/100")
        print(f"  Topology: {scores['topology']:.1f}/100")
        print(f"  Geometry: {scores['geometry']:.1f}/100")
        print(f"  UV:       {scores['uv']:.1f}/100")
        print(f"\nMesh Statistics:")
        print(f"  Vertices: {details['vertex_count']}")
        print(f"  Edges:    {details['edge_count']}")
        print(f"  Faces:    {details['face_count']}")
        print(f"    - Tris:  {details['tris']}")
        print(f"    - Quads: {details['quads']}")
        print(f"    - N-gons: {details['ngons']}")
        print(f"\nIssues Found:")
        for issue in issues:
            print(f"  • {issue}")
        print("="*70 + "\n")
        
        notification_system.FO4_NotificationSystem.notify(
            f"Mesh quality: {scores['overall']:.1f}/100", 
            'INFO' if scores['overall'] > 70 else 'WARNING'
        )
        
        return {'FINISHED'}


class FO4_OT_AutoRepairMesh(Operator):
    """Automatically repair common mesh issues"""
    bl_idname = "fo4.auto_repair_mesh"
    bl_label = "Auto-Repair Mesh"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        # Repair mesh
        success, message, repairs = advanced_mesh_helpers.AdvancedMeshHelpers.auto_repair_mesh(obj)
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                "Mesh repaired successfully", 'INFO'
            )
            
            print("\n" + "="*70)
            print("MESH REPAIR RESULTS")
            print("="*70)
            print(f"Object: {obj.name}")
            print(f"\nRepairs Made:")
            for key, value in repairs.items():
                print(f"  {key}: {value}")
            print("="*70 + "\n")
        else:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}
        
        return {'FINISHED'}


class FO4_OT_SmartDecimate(Operator):
    """Intelligently reduce polygon count with feature preservation"""
    bl_idname = "fo4.smart_decimate"
    bl_label = "Smart Decimate"
    bl_options = {'REGISTER', 'UNDO'}
    
    method: EnumProperty(
        name="Method",
        items=[
            ('RATIO', "Ratio", "Use reduction ratio"),
            ('TARGET', "Target Count", "Target specific polygon count"),
        ],
        default='RATIO'
    )
    
    ratio: FloatProperty(
        name="Ratio",
        description="Reduction ratio (0.5 = 50% reduction)",
        default=0.5,
        min=0.01,
        max=1.0
    )
    
    target_poly_count: IntProperty(
        name="Target Poly Count",
        description="Target polygon count",
        default=10000,
        min=100,
        max=1000000
    )
    
    preserve_uvs: BoolProperty(
        name="Preserve UVs",
        description="Preserve UV seams during decimation",
        default=True
    )
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        # Decimate mesh
        if self.method == 'TARGET':
            success, message, stats = advanced_mesh_helpers.AdvancedMeshHelpers.smart_decimate(
                obj, target_poly_count=self.target_poly_count, preserve_uvs=self.preserve_uvs
            )
        else:
            success, message, stats = advanced_mesh_helpers.AdvancedMeshHelpers.smart_decimate(
                obj, ratio=self.ratio, preserve_uvs=self.preserve_uvs
            )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                f"Decimated: {stats['reduction_percent']:.1f}% reduction", 'INFO'
            )
        else:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "method")
        if self.method == 'RATIO':
            layout.prop(self, "ratio")
        else:
            layout.prop(self, "target_poly_count")
        layout.prop(self, "preserve_uvs")


class FO4_OT_GenerateLOD(Operator):
    """Generate Level of Detail mesh chain"""
    bl_idname = "fo4.generate_lod"
    bl_label = "Generate LOD Chain"
    bl_options = {'REGISTER', 'UNDO'}
    
    num_levels: IntProperty(
        name="LOD Levels",
        description="Number of LOD levels to generate",
        default=4,
        min=1,
        max=6
    )
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        # Generate LOD chain
        success, message, lod_objects = advanced_mesh_helpers.AdvancedMeshHelpers.generate_lod_chain(obj)
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                f"Generated {len(lod_objects)} LOD levels", 'INFO'
            )
            
            print("\n" + "="*70)
            print("LOD GENERATION RESULTS")
            print("="*70)
            print(f"Source Object: {obj.name}")
            print(f"\nLOD Meshes Created:")
            for lod_obj, poly_count in lod_objects:
                print(f"  {lod_obj.name}: {poly_count} polygons")
            print("="*70 + "\n")
        else:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class FO4_OT_OptimizeUVs(Operator):
    """Optimize UV layout"""
    bl_idname = "fo4.optimize_uvs"
    bl_label = "Optimize UVs"
    bl_options = {'REGISTER', 'UNDO'}
    
    method: EnumProperty(
        name="Method",
        items=[
            ('SMART', "Smart UV Project", "Smart UV projection with automatic seams"),
            ('UNWRAP', "Angle-Based Unwrap", "Unwrap with angle-based method"),
            ('CUBE', "Cube Projection", "Simple cube projection"),
        ],
        default='SMART'
    )
    
    margin: FloatProperty(
        name="Margin",
        description="Space between UV islands",
        default=0.01,
        min=0.0,
        max=0.1
    )
    
    def execute(self, context):
        obj = context.active_object
        
        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}
        
        # Optimize UVs
        success, message = advanced_mesh_helpers.AdvancedMeshHelpers.optimize_uvs(
            obj, self.method, self.margin
        )
        
        if success:
            self.report({'INFO'}, message)
            notification_system.FO4_NotificationSystem.notify(
                "UVs optimized", 'INFO'
            )
        else:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Register all operators

classes = (
    FO4_OT_StartTutorial,
    FO4_OT_ShowHelp,
    FO4_OT_ShowMessage,
    FO4_OT_CreateBaseMesh,
    FO4_OT_OptimizeMesh,
    FO4_OT_ValidateMesh,
    FO4_OT_SetupTextures,
    FO4_OT_InstallTexture,
    FO4_OT_ValidateTextures,
    FO4_OT_SetupArmature,
    FO4_OT_ValidateAnimation,
    FO4_OT_ExportMesh,
    FO4_OT_ExportAll,
    FO4_OT_ValidateExport,
    FO4_OT_ImageToMesh,
    FO4_OT_ApplyDisplacementMap,
    FO4_OT_GenerateMeshFromText,
    FO4_OT_GenerateMeshFromImageAI,
    FO4_OT_ShowHunyuan3DInfo,
    FO4_OT_StartGradioServer,
    FO4_OT_StopGradioServer,
    FO4_OT_ShowGradioInfo,
    FO4_OT_GenerateMotionFromText,
    FO4_OT_ImportMotionFile,
    FO4_OT_ShowHyMotionInfo,
    FO4_OT_ConvertTextureToDDS,
    FO4_OT_ConvertObjectTexturesToDDS,
    FO4_OT_CheckNVTTInstallation,
    FO4_OT_UpscaleTexture,
    FO4_OT_UpscaleObjectTextures,
    FO4_OT_CheckRealESRGANInstallation,
    FO4_OT_ImportGET3DMesh,
    FO4_OT_OptimizeGET3DMesh,
    FO4_OT_ShowGET3DInfo,
    FO4_OT_CheckGET3DInstallation,
    FO4_OT_GenerateTextureStyleGAN2,
    FO4_OT_ImportStyleGAN2Texture,
    FO4_OT_ShowStyleGAN2Info,
    FO4_OT_CheckStyleGAN2Installation,
    FO4_OT_ReconstructFromImages,
    FO4_OT_ImportInstantNGPMesh,
    FO4_OT_OptimizeNERFMesh,
    FO4_OT_ShowInstantNGPInfo,
    FO4_OT_CheckInstantNGPInstallation,
    FO4_OT_ShowImageTo3DComparison,
    FO4_OT_CheckAllImageTo3D,
    FO4_OT_SuggestImageTo3DMethod,
    FO4_OT_GenerateTripoSRTexture,
    FO4_OT_ShowTripoSRWorkflow,
    FO4_OT_CheckTripoSRTextureGen,
    FO4_OT_GenerateFromStereo,
    FO4_OT_CheckStereoTripoSR,
    FO4_OT_AnalyzeMeshQuality,
    FO4_OT_AutoRepairMesh,
    FO4_OT_SmartDecimate,
    FO4_OT_GenerateLOD,
    FO4_OT_OptimizeUVs,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
