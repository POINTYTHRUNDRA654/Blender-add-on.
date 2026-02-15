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
