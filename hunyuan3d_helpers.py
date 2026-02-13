"""
Hunyuan3D-2 AI model integration for generating 3D meshes from text and images.
This module provides optional AI-powered mesh generation using Tencent's Hunyuan3D-2 model.

Note: This is an OPTIONAL feature. The add-on works perfectly without it.
Installing Hunyuan3D-2 requires significant disk space and GPU resources.

Installation:
1. Clone the repository: gh repo clone Tencent-Hunyuan/Hunyuan3D-2
2. Follow their installation instructions
3. The add-on will automatically detect if it's available
"""

import bpy
import os
import sys
import tempfile
from pathlib import Path

# Check if Hunyuan3D-2 is available
HUNYUAN3D_AVAILABLE = False
HUNYUAN3D_ERROR = None

try:
    # Try to import the necessary dependencies
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    HUNYUAN3D_ERROR = "PyTorch not installed"

# We don't actually import Hunyuan3D here to keep the add-on lightweight
# It will be imported dynamically when needed


def check_hunyuan3d_availability():
    """
    Check if Hunyuan3D-2 is installed and available.
    
    Returns:
        tuple: (available: bool, message: str)
    """
    if not TORCH_AVAILABLE:
        return False, "PyTorch not installed. Install with: pip install torch torchvision"
    
    # Check if Hunyuan3D-2 repository is cloned
    # Common locations to check
    possible_paths = [
        os.path.expanduser("~/Hunyuan3D-2"),
        os.path.expanduser("~/Projects/Hunyuan3D-2"),
        "/opt/Hunyuan3D-2",
        os.path.join(os.path.dirname(__file__), "..", "Hunyuan3D-2"),
    ]
    
    hunyuan_path = None
    for path in possible_paths:
        if os.path.exists(path) and os.path.isdir(path):
            hunyuan_path = path
            break
    
    if hunyuan_path is None:
        return False, (
            "Hunyuan3D-2 not found. Clone it with:\n"
            "gh repo clone Tencent-Hunyuan/Hunyuan3D-2\n"
            "Or: git clone https://github.com/Tencent-Hunyuan/Hunyuan3D-2.git"
        )
    
    # Check if the main module exists
    if not os.path.exists(os.path.join(hunyuan_path, "infer.py")):
        return False, f"Hunyuan3D-2 found at {hunyuan_path} but infer.py not found"
    
    return True, f"Hunyuan3D-2 available at: {hunyuan_path}"


def generate_mesh_from_text(prompt, output_path=None, resolution=256):
    """
    Generate a 3D mesh from a text prompt using Hunyuan3D-2.
    
    Args:
        prompt (str): Text description of the 3D model
        output_path (str): Path to save the generated mesh (optional)
        resolution (int): Resolution of the generated mesh
        
    Returns:
        tuple: (success: bool, object/error_message)
    """
    available, message = check_hunyuan3d_availability()
    if not available:
        return False, f"Hunyuan3D-2 not available: {message}"
    
    try:
        # This is a placeholder for the actual Hunyuan3D-2 integration
        # The real implementation would call the Hunyuan3D-2 inference code
        
        return False, (
            "Text-to-3D generation not yet implemented.\n"
            "This feature requires integration with Hunyuan3D-2's inference pipeline.\n"
            f"Prompt: '{prompt}'\n"
            "See documentation for manual usage instructions."
        )
        
    except Exception as e:
        return False, f"Error generating mesh from text: {str(e)}"


def generate_mesh_from_image(image_path, output_path=None, resolution=256):
    """
    Generate a full 3D mesh from a 2D image using Hunyuan3D-2 AI model.
    This is different from height map conversion - it creates a complete 3D object.
    
    Args:
        image_path (str): Path to the input image
        output_path (str): Path to save the generated mesh (optional)
        resolution (int): Resolution of the generated mesh
        
    Returns:
        tuple: (success: bool, object/error_message)
    """
    available, message = check_hunyuan3d_availability()
    if not available:
        return False, f"Hunyuan3D-2 not available: {message}"
    
    if not os.path.exists(image_path):
        return False, f"Image file not found: {image_path}"
    
    try:
        # This is a placeholder for the actual Hunyuan3D-2 integration
        # The real implementation would call the Hunyuan3D-2 inference code
        
        return False, (
            "Image-to-3D generation not yet implemented.\n"
            "This feature requires integration with Hunyuan3D-2's inference pipeline.\n"
            f"Image: '{image_path}'\n"
            "See documentation for manual usage instructions."
        )
        
    except Exception as e:
        return False, f"Error generating mesh from image: {str(e)}"


def import_mesh_file(filepath, mesh_name="AI_Generated_Mesh"):
    """
    Import a mesh file (OBJ, GLB, etc.) into Blender.
    
    Args:
        filepath (str): Path to the mesh file
        mesh_name (str): Name for the imported object
        
    Returns:
        tuple: (success: bool, object/error_message)
    """
    if not os.path.exists(filepath):
        return False, f"Mesh file not found: {filepath}"
    
    try:
        # Determine file type and import accordingly
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.obj':
            bpy.ops.import_scene.obj(filepath=filepath)
        elif ext in ['.glb', '.gltf']:
            bpy.ops.import_scene.gltf(filepath=filepath)
        elif ext == '.fbx':
            bpy.ops.import_scene.fbx(filepath=filepath)
        elif ext == '.stl':
            bpy.ops.import_mesh.stl(filepath=filepath)
        else:
            return False, f"Unsupported file format: {ext}"
        
        # Get the imported object
        obj = bpy.context.selected_objects[0] if bpy.context.selected_objects else None
        if obj:
            obj.name = mesh_name
            return True, obj
        else:
            return False, "Import succeeded but no object was created"
            
    except Exception as e:
        return False, f"Error importing mesh: {str(e)}"


class Hunyuan3DHelpers:
    """Helper class for Hunyuan3D-2 AI operations"""
    
    @staticmethod
    def is_available():
        """Check if Hunyuan3D-2 is available"""
        available, _ = check_hunyuan3d_availability()
        return available
    
    @staticmethod
    def get_status_message():
        """Get the current status message for Hunyuan3D-2"""
        available, message = check_hunyuan3d_availability()
        if available:
            return f"✓ {message}"
        else:
            return f"✗ {message}"
    
    @staticmethod
    def get_installation_instructions():
        """Get installation instructions for Hunyuan3D-2"""
        return """
To install Hunyuan3D-2:

1. Install PyTorch (if not already installed):
   pip install torch torchvision

2. Clone the Hunyuan3D-2 repository:
   gh repo clone Tencent-Hunyuan/Hunyuan3D-2
   OR
   git clone https://github.com/Tencent-Hunyuan/Hunyuan3D-2.git

3. Follow the installation instructions in their README:
   cd Hunyuan3D-2
   pip install -r requirements.txt

4. Download the model weights (follow their documentation)

5. Restart Blender

Note: Hunyuan3D-2 requires:
- Several GB of disk space for models
- GPU with CUDA support recommended
- Significant computational resources

The add-on will automatically detect when it's installed.
"""


def register():
    """Register Hunyuan3D helper functions"""
    global HUNYUAN3D_AVAILABLE, HUNYUAN3D_ERROR
    
    # Check availability on registration
    HUNYUAN3D_AVAILABLE, HUNYUAN3D_ERROR = check_hunyuan3d_availability()
    
    if HUNYUAN3D_AVAILABLE:
        print("✓ Hunyuan3D-2 is available")
    else:
        print(f"ℹ Hunyuan3D-2 not available: {HUNYUAN3D_ERROR}")
        print("  (This is optional - the add-on works without it)")


def unregister():
    """Unregister Hunyuan3D helper functions"""
    pass
