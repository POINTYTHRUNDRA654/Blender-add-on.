"""
NVIDIA Texture Tools (NVTT) integration helper
Provides DDS texture conversion functionality for Fallout 4 modding
"""

import bpy
import os
import subprocess
import shutil
from pathlib import Path

class NVTTHelpers:
    """Helper functions for NVIDIA Texture Tools integration"""
    
    @staticmethod
    def is_nvtt_available():
        """Check if NVIDIA Texture Tools (nvcompress) is available in PATH"""
        return shutil.which('nvcompress') is not None
    
    @staticmethod
    def get_nvtt_path():
        """Get the path to nvcompress executable"""
        nvcompress_path = shutil.which('nvcompress')
        return nvcompress_path if nvcompress_path else None
    
    @staticmethod
    def check_nvtt_installation():
        """
        Check NVTT installation and return status message
        Returns: (bool success, str message)
        """
        if NVTTHelpers.is_nvtt_available():
            nvtt_path = NVTTHelpers.get_nvtt_path()
            return True, f"NVIDIA Texture Tools found at: {nvtt_path}"
        else:
            install_msg = (
                "NVIDIA Texture Tools not found. To install:\n"
                "1. Clone: gh repo clone castano/nvidia-texture-tools\n"
                "2. Build following repository instructions\n"
                "3. Add nvcompress to your PATH\n"
                "See NVIDIA_RESOURCES.md for details"
            )
            return False, install_msg
    
    @staticmethod
    def convert_to_dds(input_path, output_path=None, compression_format='bc1', quality='production'):
        """
        Convert an image to DDS format using NVIDIA Texture Tools
        
        Args:
            input_path: Path to input image (PNG, JPG, TGA, etc.)
            output_path: Path for output DDS file (optional, defaults to input_path with .dds extension)
            compression_format: DDS compression format
                - 'bc1' (DXT1): For diffuse textures without alpha
                - 'bc3' (DXT5): For textures with alpha channel
                - 'bc5' (ATI2): For normal maps
            quality: Compression quality ('fastest', 'normal', 'production', 'highest')
        
        Returns: (bool success, str message)
        """
        if not NVTTHelpers.is_nvtt_available():
            return False, "NVIDIA Texture Tools (nvcompress) not found in PATH"
        
        if not os.path.exists(input_path):
            return False, f"Input file not found: {input_path}"
        
        # Determine output path
        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + '.dds'
        
        # Validate compression format
        valid_formats = {
            'bc1': 'DXT1',
            'bc3': 'DXT5',
            'bc5': 'ATI2',
            'dxt1': 'DXT1',
            'dxt5': 'DXT5',
            'ati2': 'ATI2'
        }
        
        format_lower = compression_format.lower()
        if format_lower not in valid_formats:
            return False, f"Invalid compression format: {compression_format}. Use bc1, bc3, or bc5"
        
        # Build nvcompress command
        try:
            nvcompress_path = NVTTHelpers.get_nvtt_path()
            
            # Command structure: nvcompress -format <format> -quality <quality> input output
            cmd = [
                nvcompress_path,
                f'-{format_lower}',
                f'-{quality}',
                input_path,
                output_path
            ]
            
            # Run conversion
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    size_kb = file_size / 1024
                    return True, f"Successfully converted to DDS ({compression_format.upper()}): {output_path} ({size_kb:.1f} KB)"
                else:
                    return False, f"Conversion completed but output file not found: {output_path}"
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                return False, f"nvcompress failed: {error_msg}"
        
        except subprocess.TimeoutExpired:
            return False, "Texture conversion timed out (60 seconds)"
        except Exception as e:
            return False, f"Failed to convert texture: {str(e)}"
    
    @staticmethod
    def batch_convert_textures(texture_list, output_dir=None, compression_map=None):
        """
        Convert multiple textures to DDS format
        
        Args:
            texture_list: List of (input_path, texture_type) tuples
            output_dir: Directory for output files (optional)
            compression_map: Dict mapping texture_type to compression format
        
        Returns: (int success_count, list results)
        """
        if compression_map is None:
            # Default compression formats for different texture types
            compression_map = {
                'DIFFUSE': 'bc1',    # DXT1 for diffuse
                'NORMAL': 'bc5',     # ATI2 for normal maps
                'SPECULAR': 'bc1',   # DXT1 for specular
                'ALPHA': 'bc3',      # DXT5 for textures with alpha
            }
        
        success_count = 0
        results = []
        
        for input_path, texture_type in texture_list:
            # Determine compression format
            compression = compression_map.get(texture_type, 'bc1')
            
            # Determine output path
            if output_dir:
                filename = os.path.basename(input_path)
                base_name = os.path.splitext(filename)[0]
                output_path = os.path.join(output_dir, base_name + '.dds')
            else:
                output_path = None
            
            # Convert
            success, message = NVTTHelpers.convert_to_dds(
                input_path,
                output_path,
                compression
            )
            
            results.append({
                'input': input_path,
                'type': texture_type,
                'success': success,
                'message': message
            })
            
            if success:
                success_count += 1
        
        return success_count, results
    
    @staticmethod
    def get_texture_type_for_node(node_name):
        """
        Determine texture type from node name
        Returns: texture type string for compression mapping
        """
        node_name_lower = node_name.lower()
        
        if 'diffuse' in node_name_lower or 'color' in node_name_lower or 'albedo' in node_name_lower:
            return 'DIFFUSE'
        elif 'normal' in node_name_lower:
            return 'NORMAL'
        elif 'specular' in node_name_lower or 'spec' in node_name_lower:
            return 'SPECULAR'
        elif 'alpha' in node_name_lower or 'opacity' in node_name_lower:
            return 'ALPHA'
        else:
            return 'DIFFUSE'  # Default
    
    @staticmethod
    def convert_object_textures(obj, output_dir):
        """
        Convert all textures used by an object to DDS format
        
        Args:
            obj: Blender object
            output_dir: Directory to save converted textures
        
        Returns: (bool success, str message, list converted_files)
        """
        if obj.type != 'MESH':
            return False, "Object is not a mesh", []
        
        if not obj.data.materials:
            return False, "Object has no materials", []
        
        if not NVTTHelpers.is_nvtt_available():
            return False, "NVIDIA Texture Tools not installed", []
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Collect textures from material
        texture_list = []
        
        for mat in obj.data.materials:
            if not mat or not mat.use_nodes:
                continue
            
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image:
                    # Get image file path
                    img = node.image
                    if img.filepath:
                        # Get absolute path
                        img_path = bpy.path.abspath(img.filepath)
                        if os.path.exists(img_path):
                            texture_type = NVTTHelpers.get_texture_type_for_node(node.name)
                            texture_list.append((img_path, texture_type))
        
        if not texture_list:
            return False, "No textures found in object materials", []
        
        # Convert textures
        success_count, results = NVTTHelpers.batch_convert_textures(
            texture_list,
            output_dir
        )
        
        # Collect converted file paths
        converted_files = []
        for result in results:
            if result['success']:
                # Extract output path from message
                if 'converted to DDS' in result['message']:
                    parts = result['message'].split(': ')
                    if len(parts) >= 2:
                        path_part = parts[1].split(' (')[0]
                        converted_files.append(path_part)
        
        if success_count > 0:
            message = f"Converted {success_count}/{len(texture_list)} textures to DDS format"
            return True, message, converted_files
        else:
            return False, "Failed to convert any textures", []

def register():
    """Register NVTT helper functions"""
    pass

def unregister():
    """Unregister NVTT helper functions"""
    pass
