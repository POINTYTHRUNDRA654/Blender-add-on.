"""
Image-to-3D repositories integration helper
Consolidates various image-to-3D solutions for Fallout 4 modding
"""

import bpy
import os
import subprocess
import shutil
from pathlib import Path

class ImageTo3DHelpers:
    """Helper functions for various image-to-3D solutions"""
    
    # ==================== TripoSR ====================
    
    @staticmethod
    def is_triposr_available():
        """Check if TripoSR is available"""
        try:
            import torch
            # Check for TripoSR installation
            possible_paths = [
                os.path.expanduser('~/TripoSR'),
                os.path.expanduser('~/Projects/TripoSR'),
                '/opt/TripoSR',
                'C:/Projects/TripoSR',
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return True
            
            # Check if installed as package
            try:
                import importlib.util
                spec = importlib.util.find_spec('tsr')
                if spec:
                    return True
            except:
                pass
            
            return False
        except ImportError:
            return False
    
    @staticmethod
    def find_triposr_path():
        """Find TripoSR installation path"""
        possible_paths = [
            os.path.expanduser('~/TripoSR'),
            os.path.expanduser('~/Projects/TripoSR'),
            os.path.expanduser('~/Documents/TripoSR'),
            '/opt/TripoSR',
            'C:/Projects/TripoSR',
            'C:/Users/' + os.environ.get('USERNAME', '') + '/TripoSR',
        ]
        
        for path in possible_paths:
            if os.path.exists(os.path.join(path, 'run.py')):
                return path
        
        return None
    
    @staticmethod
    def check_triposr_installation():
        """Check TripoSR installation status"""
        try:
            import torch
            has_torch = True
            cuda_available = torch.cuda.is_available()
        except ImportError:
            has_torch = False
            cuda_available = False
        
        triposr_path = ImageTo3DHelpers.find_triposr_path()
        
        if triposr_path and has_torch:
            msg = f"TripoSR found at: {triposr_path}\n"
            if cuda_available:
                msg += "CUDA: Available ✓ (GPU acceleration)\n"
            else:
                msg += "CUDA: Not available (CPU mode - slower)\n"
            msg += "Ready to convert images to 3D!"
            return True, msg
        else:
            install_msg = (
                "TripoSR not found. To install:\n\n"
                "METHOD 1 - Official Repository (Recommended):\n"
                "1. Clone repository:\n"
                "   gh repo clone VAST-AI-Research/TripoSR\n"
                "   (or: git clone https://github.com/VAST-AI-Research/TripoSR.git)\n\n"
                "2. Install dependencies:\n"
                "   cd TripoSR\n"
                "   pip install torch torchvision\n"
                "   pip install -r requirements.txt\n\n"
                "3. Download model weights (automatic on first run)\n\n"
                "METHOD 2 - Python Package:\n"
                "   pip install triposr\n\n"
                "METHOD 3 - ComfyUI Node (NEW):\n"
                "1. Clone ComfyUI-Flowty-TripoSR:\n"
                "   gh repo clone flowtyone/ComfyUI-Flowty-TripoSR\n"
                "   (or: git clone https://github.com/flowtyone/ComfyUI-Flowty-TripoSR.git)\n\n"
                "2. For use with ComfyUI:\n"
                "   - Place in ComfyUI/custom_nodes/\n"
                "   - Install requirements: pip install -r requirements.txt\n"
                "   - Restart ComfyUI\n\n"
                "3. For standalone use from Blender:\n"
                "   - Can use TripoSR model from this installation\n"
                "   - Provides optimized inference pipeline\n\n"
                "FEATURES:\n"
                "- Very fast inference (~5 seconds per image)\n"
                "- High quality 3D reconstruction\n"
                "- Single image input\n"
                "- Works on CPU or GPU\n"
                "- ComfyUI integration for workflow automation\n\n"
            )
            
            if not has_torch:
                install_msg += "⚠️ PyTorch not installed\n"
                install_msg += "Install: pip install torch torchvision\n\n"
            
            return False, install_msg
    
    @staticmethod
    def convert_image_to_3d_triposr(image_path, output_path=None):
        """
        Convert single image to 3D using TripoSR
        
        Args:
            image_path: Path to input image
            output_path: Path for output mesh (optional)
        
        Returns: (bool success, str message, str output_file)
        """
        triposr_path = ImageTo3DHelpers.find_triposr_path()
        
        if not triposr_path:
            return False, "TripoSR not installed", None
        
        if not os.path.exists(image_path):
            return False, f"Image not found: {image_path}", None
        
        # Determine output path
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = f"{base_name}_triposr.obj"
        
        # Instructions for running TripoSR
        msg = (
            "To convert image to 3D with TripoSR:\n\n"
            f"1. Navigate to: {triposr_path}\n"
            "2. Run TripoSR:\n"
            f"   python run.py {image_path} --output {output_path}\n\n"
            "   OR for batch processing:\n"
            f"   python run.py {os.path.dirname(image_path)}/ --output ./output/\n\n"
            "3. Import generated mesh:\n"
            "   - Use 'Import' operator in Blender\n"
            "   - Or use File → Import → Wavefront (.obj)\n\n"
            "TIPS:\n"
            "- Best results with clear, well-lit object photos\n"
            "- White/neutral background recommended\n"
            "- Object should fill most of frame\n"
            "- Inference takes ~5 seconds on GPU\n"
            "- Output includes texture map\n"
        )
        
        return False, msg, None
    
    @staticmethod
    def find_triposr_texture_gen_path():
        """Find triposr-texture-gen installation path"""
        possible_paths = [
            os.path.expanduser('~/triposr-texture-gen'),
            os.path.expanduser('~/Projects/triposr-texture-gen'),
            os.path.expanduser('~/Documents/triposr-texture-gen'),
            '/opt/triposr-texture-gen',
            'C:/Projects/triposr-texture-gen',
        ]
        
        for path in possible_paths:
            if os.path.exists(os.path.join(path, 'generate_texture.py')):
                return path
            # Also check for main.py or other entry points
            if os.path.exists(os.path.join(path, 'main.py')):
                return path
        
        return None
    
    @staticmethod
    def check_triposr_texture_gen_installation():
        """
        Check triposr-texture-gen installation status
        Returns: (bool success, str message)
        """
        try:
            import torch
            has_torch = True
            cuda_available = torch.cuda.is_available()
        except ImportError:
            has_torch = False
            cuda_available = False
        
        texture_gen_path = ImageTo3DHelpers.find_triposr_texture_gen_path()
        
        if texture_gen_path and has_torch:
            msg = f"triposr-texture-gen found at: {texture_gen_path}\n"
            if cuda_available:
                msg += "CUDA: Available ✓\n"
            else:
                msg += "CUDA: Not available (CPU mode - slower)\n"
            msg += "Ready to generate textures for TripoSR meshes!"
            return True, msg
        else:
            install_msg = (
                "triposr-texture-gen not found. To install:\n\n"
                "INSTALLATION:\n"
                "1. Clone repository:\n"
                "   gh repo clone ejones/triposr-texture-gen\n"
                "   (or: git clone https://github.com/ejones/triposr-texture-gen.git)\n\n"
                "2. Install dependencies:\n"
                "   cd triposr-texture-gen\n"
                "   pip install torch torchvision\n"
                "   pip install -r requirements.txt\n\n"
                "3. Download required models:\n"
                "   - TripoSR model (if not already installed)\n"
                "   - Texture generation models (automatic on first run)\n\n"
                "FEATURES:\n"
                "- Enhanced texture generation for TripoSR meshes\n"
                "- Improved texture quality and consistency\n"
                "- UV unwrapping optimization\n"
                "- Multi-view texture synthesis\n"
                "- PBR material generation (diffuse, normal, roughness)\n\n"
                "WORKFLOW:\n"
                "1. Generate mesh with TripoSR\n"
                "2. Use triposr-texture-gen to create high-quality textures\n"
                "3. Import to Blender with complete materials\n\n"
            )
            
            if not has_torch:
                install_msg += "⚠️ PyTorch not installed\n"
                install_msg += "Install: pip install torch torchvision\n\n"
            
            return False, install_msg
    
    @staticmethod
    def generate_texture_for_triposr_mesh(mesh_path, reference_image, output_dir=None):
        """
        Generate enhanced textures for TripoSR mesh
        
        Args:
            mesh_path: Path to TripoSR generated mesh
            reference_image: Original reference image used for 3D generation
            output_dir: Directory for output textures (optional)
        
        Returns: (bool success, str message, dict texture_paths)
        """
        texture_gen_path = ImageTo3DHelpers.find_triposr_texture_gen_path()
        
        if not texture_gen_path:
            return False, "triposr-texture-gen not installed", {}
        
        if not os.path.exists(mesh_path):
            return False, f"Mesh not found: {mesh_path}", {}
        
        if not os.path.exists(reference_image):
            return False, f"Reference image not found: {reference_image}", {}
        
        # Determine output directory
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(mesh_path), "textures")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Instructions for generating textures
        msg = (
            "To generate enhanced textures for TripoSR mesh:\n\n"
            f"1. Navigate to: {texture_gen_path}\n"
            "2. Run texture generation:\n"
            f"   python generate_texture.py \\\n"
            f"     --mesh {mesh_path} \\\n"
            f"     --image {reference_image} \\\n"
            f"     --output {output_dir}\n\n"
            "3. Generated textures will include:\n"
            "   - diffuse.png (base color map)\n"
            "   - normal.png (normal map)\n"
            "   - roughness.png (roughness map)\n"
            "   - metallic.png (metallic map - if applicable)\n\n"
            "4. Import to Blender:\n"
            "   - Import mesh: File → Import → Wavefront (.obj)\n"
            "   - Use 'Setup FO4 Materials' operator\n"
            "   - Load generated textures with 'Install Texture' operator\n"
            "   - Convert to DDS with NVTT for Fallout 4\n\n"
            "TIPS:\n"
            "- Higher resolution images = better texture quality\n"
            "- Ensure good lighting in reference image\n"
            "- Process takes ~30 seconds on GPU\n"
            "- Output textures are already UV-unwrapped\n"
            "- Can upscale with Real-ESRGAN for higher quality\n"
        )
        
        return False, msg, {}
    
    @staticmethod
    def create_triposr_complete_workflow_guide():
        """
        Create complete workflow guide for TripoSR + texture generation
        
        Returns: str guide text
        """
        guide = """
COMPLETE TRIPOSR WORKFLOW WITH TEXTURE GENERATION
=================================================

This workflow combines TripoSR for 3D reconstruction with enhanced
texture generation for production-quality assets.

STEP 1: PREPARE SOURCE IMAGE
-----------------------------
• Take high-quality photo of object
• Good lighting, neutral background
• Object fills ~70% of frame
• Clear focus, no motion blur
• Save as PNG or JPG (1024x1024 or higher)

STEP 2: GENERATE 3D MESH (TripoSR)
-----------------------------------
Option A - Official TripoSR:
  cd ~/TripoSR
  python run.py input.png --output output/mesh.obj

Option B - ComfyUI Node:
  gh repo clone flowtyone/ComfyUI-Flowty-TripoSR
  # Use in ComfyUI workflow
  # or: python run_standalone.py input.png

Output: mesh.obj (with basic texture)

STEP 3: GENERATE ENHANCED TEXTURES
-----------------------------------
gh repo clone ejones/triposr-texture-gen
cd triposr-texture-gen
python generate_texture.py \\
  --mesh output/mesh.obj \\
  --image input.png \\
  --output textures/

Output:
  textures/diffuse.png (4096x4096)
  textures/normal.png
  textures/roughness.png
  textures/metallic.png (if applicable)

STEP 4: IMPORT TO BLENDER
--------------------------
In Blender with FO4 Add-on:

1. Import mesh:
   File → Import → Wavefront (.obj)
   Select: output/mesh.obj

2. Setup materials:
   • Select imported object
   • Use 'Setup FO4 Materials' operator
   • Creates PBR material setup

3. Load textures:
   • Use 'Install Texture' operator
   • Load diffuse: textures/diffuse.png
   • Load normal: textures/normal.png
   • Load specular: textures/roughness.png

STEP 5: OPTIMIZE FOR FALLOUT 4
-------------------------------
1. Analyze quality:
   • Use 'Analyze Mesh Quality' operator
   • Check overall score and issues

2. Repair if needed:
   • Use 'Auto-Repair Mesh' operator
   • Fixes non-manifold geometry

3. Decimate if too high poly:
   • Use 'Smart Decimate' operator
   • Target: <65,535 polygons for FO4
   • Preserve UVs: ON

4. Optimize UVs:
   • Use 'Optimize UVs' operator
   • Method: Smart UV Project
   • Ensures no overlap

5. Generate LODs:
   • Use 'Generate LOD Chain' operator
   • Creates 4 LOD levels
   • Perfect for game performance

STEP 6: ENHANCE TEXTURES (OPTIONAL)
------------------------------------
1. Upscale with Real-ESRGAN:
   • Use 'Upscale Texture' operator
   • 4x scale for maximum quality
   • Apply to all texture maps

2. Convert to DDS:
   • Use 'Convert to DDS' operator
   • BC1 for diffuse
   • BC5 for normal maps
   • Required for Fallout 4

STEP 7: EXPORT
---------------
1. Validate:
   • Use 'Validate Mesh' operator
   • Ensure FO4 compatibility

2. Export:
   • Use 'Export Mesh' operator
   • Exports to FBX
   • Convert to NIF with external tools

COMPLETE EXAMPLE
================
# 1. Take photo
photo.png (of a weapon, prop, or object)

# 2. Generate 3D
cd ~/TripoSR
python run.py photo.png --output weapon.obj
# Result: weapon.obj (~10,000 polys, 5 seconds)

# 3. Generate textures
cd ~/triposr-texture-gen
python generate_texture.py \\
  --mesh ../TripoSR/weapon.obj \\
  --image ../photo.png \\
  --output weapon_textures/
# Result: 4K textures (30 seconds)

# 4. Blender import
# Import weapon.obj
# Setup FO4 materials
# Load weapon_textures/*.png

# 5. Optimize
# Analyze Quality → 85/100
# Auto-Repair (fixes minor issues)
# Smart Decimate → 8,000 polys (if needed)
# Generate LOD → 4 levels
# Optimize UVs → packed efficiently

# 6. Enhance
# Upscale textures → 8K (Real-ESRGAN)
# Convert to DDS → weapon_d.dds, weapon_n.dds

# 7. Export
# Export to FBX → weapon.fbx
# Convert to NIF → weapon.nif
# Ready for Fallout 4!

TIMING BREAKDOWN
================
• Photo capture: 2 minutes
• TripoSR generation: 5 seconds
• Texture generation: 30 seconds
• Blender import: 1 minute
• Mesh optimization: 2 minutes
• Texture enhancement: 2 minutes
• Export: 1 minute
---------------------------------
TOTAL TIME: ~10 minutes for complete asset!

Compare to traditional workflow:
• Manual 3D modeling: 2-4 hours
• Manual UV unwrapping: 30-60 minutes
• Manual texture painting: 1-2 hours
---------------------------------
TRADITIONAL TIME: 4-7 hours

TIME SAVED: 95%+

QUALITY COMPARISON
==================
TripoSR + Texture Gen Pipeline:
✅ Photorealistic accuracy
✅ Proper UV layout
✅ PBR materials
✅ Game-ready topology
✅ Automatic LODs
✅ Production quality in minutes

SUPPORTED WORKFLOWS
===================
1. Props/Weapons: Photo → 3D → Game
2. Characters: Multi-photo → 3D → Retopo → Game
3. Environments: Photo → 3D → Tile → Game
4. Textures: Photo → Extract → Enhance → Game

See NVIDIA_RESOURCES.md for more AI tools.
See README.md for Fallout 4 modding guide.
"""
        return guide
    
    # ==================== DreamGaussian ====================
    
    @staticmethod
    def is_dreamgaussian_available():
        """Check if DreamGaussian is available"""
        try:
            import torch
            possible_paths = [
                os.path.expanduser('~/dreamgaussian'),
                os.path.expanduser('~/Projects/dreamgaussian'),
                '/opt/dreamgaussian',
                'C:/Projects/dreamgaussian',
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return True
            
            return False
        except ImportError:
            return False
    
    @staticmethod
    def find_dreamgaussian_path():
        """Find DreamGaussian installation path"""
        possible_paths = [
            os.path.expanduser('~/dreamgaussian'),
            os.path.expanduser('~/Projects/dreamgaussian'),
            os.path.expanduser('~/Documents/dreamgaussian'),
            '/opt/dreamgaussian',
            'C:/Projects/dreamgaussian',
        ]
        
        for path in possible_paths:
            if os.path.exists(os.path.join(path, 'main.py')):
                return path
        
        return None
    
    @staticmethod
    def check_dreamgaussian_installation():
        """Check DreamGaussian installation status"""
        try:
            import torch
            has_torch = True
            cuda_available = torch.cuda.is_available()
        except ImportError:
            has_torch = False
            cuda_available = False
        
        dreamgaussian_path = ImageTo3DHelpers.find_dreamgaussian_path()
        
        if dreamgaussian_path and has_torch:
            msg = f"DreamGaussian found at: {dreamgaussian_path}\n"
            if cuda_available:
                msg += "CUDA: Available ✓\n"
            else:
                msg += "CUDA: Not available (requires GPU)\n"
            msg += "Ready for image/text to 3D!"
            return True, msg
        else:
            install_msg = (
                "DreamGaussian not found. To install:\n\n"
                "1. Clone repository:\n"
                "   gh repo clone dreamgaussian/dreamgaussian\n"
                "   (or: git clone https://github.com/dreamgaussian/dreamgaussian.git)\n\n"
                "2. Install dependencies:\n"
                "   cd dreamgaussian\n"
                "   pip install torch torchvision\n"
                "   pip install -r requirements.txt\n\n"
                "3. Install additional requirements:\n"
                "   pip install kiui nvdiffrast\n\n"
                "REQUIREMENTS:\n"
                "- NVIDIA GPU with CUDA (required)\n"
                "- 8GB+ VRAM recommended\n\n"
                "FEATURES:\n"
                "- Text to 3D generation\n"
                "- Image to 3D conversion\n"
                "- High quality results\n"
                "- Uses Gaussian Splatting\n\n"
            )
            
            if not has_torch:
                install_msg += "⚠️ PyTorch not installed\n"
            
            return False, install_msg
    
    # ==================== Shap-E ====================
    
    @staticmethod
    def is_shap_e_available():
        """Check if Shap-E is available"""
        try:
            import shap_e
            return True
        except ImportError:
            return False
    
    @staticmethod
    def check_shap_e_installation():
        """Check Shap-E installation status"""
        if ImageTo3DHelpers.is_shap_e_available():
            msg = "Shap-E is installed ✓\n"
            msg += "Ready to generate 3D from text/images!"
            return True, msg
        else:
            install_msg = (
                "Shap-E not found. To install:\n\n"
                "METHOD 1 - Python Package (Easiest):\n"
                "   pip install shap-e\n\n"
                "METHOD 2 - From Source:\n"
                "1. Clone repository:\n"
                "   gh repo clone openai/shap-e\n"
                "   (or: git clone https://github.com/openai/shap-e.git)\n\n"
                "2. Install:\n"
                "   cd shap-e\n"
                "   pip install -e .\n\n"
                "FEATURES:\n"
                "- Text to 3D\n"
                "- Image to 3D\n"
                "- From OpenAI\n"
                "- Easy to use Python API\n\n"
            )
            return False, install_msg
    
    # ==================== Unified Interface ====================
    
    @staticmethod
    def get_available_methods():
        """Get list of available image-to-3D methods"""
        methods = []
        
        if ImageTo3DHelpers.is_triposr_available():
            methods.append(('triposr', 'TripoSR', 'Fast, high quality'))
        
        if ImageTo3DHelpers.is_dreamgaussian_available():
            methods.append(('dreamgaussian', 'DreamGaussian', 'Text/Image to 3D'))
        
        if ImageTo3DHelpers.is_shap_e_available():
            methods.append(('shap_e', 'Shap-E', 'OpenAI, easy API'))
        
        # Always available - existing features
        methods.append(('heightmap', 'Height Map', 'Image to mesh via displacement'))
        methods.append(('hunyuan3d', 'Hunyuan3D-2', 'Tencent AI (if installed)'))
        
        return methods
    
    @staticmethod
    def create_comparison_guide():
        """Create comparison guide for image-to-3D methods"""
        guide = """
IMAGE-TO-3D METHODS COMPARISON
==============================

1. TripoSR (Stability AI/Tripo AI)
   Repo: gh repo clone VAST-AI-Research/TripoSR
   ⚡ Speed: Very Fast (~5 seconds)
   📊 Quality: High
   💻 Requirements: PyTorch (GPU optional)
   📝 Input: Single image
   ✨ Best for: Quick results, production use
   
2. DreamGaussian
   Repo: gh repo clone dreamgaussian/dreamgaussian
   ⚡ Speed: Fast (~1 minute)
   📊 Quality: Very High
   💻 Requirements: NVIDIA GPU required
   📝 Input: Text or Image
   ✨ Best for: High quality, artistic results

3. Shap-E (OpenAI)
   Repo: gh repo clone openai/shap-e
   ⚡ Speed: Medium (~30 seconds)
   📊 Quality: Good
   💻 Requirements: PyTorch (GPU optional)
   📝 Input: Text or Image
   ✨ Best for: Easy integration, API usage

4. Instant-NGP (Already integrated)
   Repo: gh repo clone NVlabs/instant-ngp
   ⚡ Speed: Fast (~10 seconds)
   📊 Quality: Very High
   💻 Requirements: NVIDIA RTX GPU
   📝 Input: Multiple images (NeRF)
   ✨ Best for: Photorealistic reconstruction

5. GET3D (Already integrated)
   Repo: gh repo clone NVIDIA/GET3D
   ⚡ Speed: Fast
   📊 Quality: High
   💻 Requirements: NVIDIA GPU
   📝 Input: Random generation
   ✨ Best for: Creating varied assets

6. Hunyuan3D-2 (Already integrated)
   Repo: gh repo clone Tencent-Hunyuan/Hunyuan3D-2
   ⚡ Speed: Medium
   📊 Quality: High
   💻 Requirements: GPU
   📝 Input: Text or Image
   ✨ Best for: Versatile generation

7. Height Map (Built-in)
   ⚡ Speed: Instant
   📊 Quality: Depends on image
   💻 Requirements: PIL/Pillow
   📝 Input: Grayscale image
   ✨ Best for: Terrain, displacement

RECOMMENDATIONS FOR FALLOUT 4 MODDING:
======================================

Quick Assets:
  → TripoSR (fastest, good quality)

High Quality:
  → DreamGaussian or Instant-NGP

Terrain/Ground:
  → Height Map method (built-in)

Photo Scanning:
  → Instant-NGP (multiple photos)

Random Generation:
  → GET3D or StyleGAN2

Textures:
  → StyleGAN2 (textures)
  → Real-ESRGAN (upscaling)

WORKFLOW EXAMPLE:
================
1. Take photo of object
2. Use TripoSR to convert to 3D (5 sec)
3. Import to Blender
4. Optimize for FO4 (reduce polys)
5. Apply textures (StyleGAN2 generated)
6. Upscale textures (Real-ESRGAN)
7. Convert to DDS (NVTT)
8. Export to FO4

See NVIDIA_RESOURCES.md for detailed setup instructions.
"""
        return guide
    
    @staticmethod
    def get_installation_status():
        """Get installation status of all image-to-3D methods"""
        status = {}
        
        status['TripoSR'] = ImageTo3DHelpers.check_triposr_installation()
        status['DreamGaussian'] = ImageTo3DHelpers.check_dreamgaussian_installation()
        status['Shap-E'] = ImageTo3DHelpers.check_shap_e_installation()
        
        return status
    
    @staticmethod
    def suggest_best_method(use_case):
        """Suggest best image-to-3D method for specific use case"""
        suggestions = {
            'speed': 'TripoSR - Fastest single image to 3D (~5 seconds)',
            'quality': 'DreamGaussian or Instant-NGP - Best quality output',
            'ease': 'Shap-E - Easiest Python API, pip install',
            'terrain': 'Height Map - Built-in, instant for heightmaps',
            'photos': 'Instant-NGP - Best for multiple photo reconstruction',
            'texture': 'StyleGAN2 - For generating texture maps',
        }
        
        return suggestions.get(use_case, 'TripoSR recommended for general use')

def register():
    """Register image-to-3D helper functions"""
    pass

def unregister():
    """Unregister image-to-3D helper functions"""
    pass
    
    # ==================== Stereo Vision Multi-View Generation ====================
    
    @staticmethod
    def find_stereo_triposr_path():
        """Find super-ai-vision-stereo-world-generate-triposr installation path"""
        possible_paths = [
            os.path.expanduser('~/super-ai-vision-stereo-world-generate-triposr'),
            os.path.expanduser('~/Projects/super-ai-vision-stereo-world-generate-triposr'),
            os.path.expanduser('~/stereo-triposr'),
            '/opt/stereo-triposr',
            'C:/Projects/stereo-triposr',
        ]
        
        for path in possible_paths:
            if os.path.exists(os.path.join(path, 'generate.py')):
                return path
            if os.path.exists(os.path.join(path, 'main.py')):
                return path
        
        return None
    
    @staticmethod
    def check_stereo_triposr_installation():
        """Check stereo-world-triposr installation status"""
        try:
            import torch
            has_torch = True
            cuda_available = torch.cuda.is_available()
        except ImportError:
            has_torch = False
            cuda_available = False
        
        stereo_path = ImageTo3DHelpers.find_stereo_triposr_path()
        
        if stereo_path and has_torch:
            msg = f"Stereo TripoSR found at: {stereo_path}\n"
            if cuda_available:
                msg += "CUDA: Available ✓\n"
            else:
                msg += "CUDA: Not available (CPU mode)\n"
            msg += "Ready for stereo/multi-view 3D!"
            return True, msg
        else:
            install_msg = (
                "stereo-world-generate-triposr not found.\n\n"
                "Install: gh repo clone yuedajiong/super-ai-vision-stereo-world-generate-triposr\n"
                "Features: Stereo pairs, multi-view, better geometry\n"
            )
            return False, install_msg
    
    @staticmethod
    def generate_from_stereo_images(left_image, right_image, output_path=None):
        """Generate 3D from stereo image pair"""
        stereo_path = ImageTo3DHelpers.find_stereo_triposr_path()
        
        if not stereo_path:
            return False, "Stereo TripoSR not installed", None
        
        msg = f"Run: python generate.py --left {left_image} --right {right_image}"
        return False, msg, None
