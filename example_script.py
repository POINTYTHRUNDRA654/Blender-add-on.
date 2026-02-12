"""
Example script showing how to use the Fallout 4 Tutorial Add-on programmatically

This script demonstrates the scripting interface for automating mod creation tasks.
Run this in Blender's scripting workspace.
"""

import bpy

# Import helper modules
# Note: These imports work when the add-on is installed and enabled
try:
    from Blender-add-on import mesh_helpers, texture_helpers, animation_helpers, export_helpers
except ImportError:
    print("Please ensure the Fallout 4 Tutorial Add-on is installed and enabled")
    exit()

def create_simple_weapon():
    """Example: Create a simple weapon mesh"""
    
    print("Creating weapon mesh...")
    
    # Create base mesh
    obj = mesh_helpers.MeshHelpers.create_base_mesh()
    obj.name = "SimpleWeapon"
    
    # Enter edit mode and modify (simplified example)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=1)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Optimize for FO4
    success, message = mesh_helpers.MeshHelpers.optimize_mesh(obj)
    print(f"Optimization: {message}")
    
    # Validate mesh
    success, issues = mesh_helpers.MeshHelpers.validate_mesh(obj)
    if success:
        print("Mesh validation: PASSED")
    else:
        print("Mesh validation issues:")
        for issue in issues:
            print(f"  - {issue}")
    
    return obj

def setup_textures_for_object(obj, texture_dir):
    """Example: Setup textures for an object"""
    
    import os
    
    print(f"Setting up textures for {obj.name}...")
    
    # Create FO4 material
    mat = texture_helpers.TextureHelpers.setup_fo4_material(obj)
    print(f"Material created: {mat.name}")
    
    # Install textures (if files exist)
    diffuse_path = os.path.join(texture_dir, "diffuse.png")
    normal_path = os.path.join(texture_dir, "normal.png")
    
    if os.path.exists(diffuse_path):
        success, message = texture_helpers.TextureHelpers.install_texture(
            obj, diffuse_path, 'DIFFUSE'
        )
        print(f"Diffuse texture: {message}")
    
    if os.path.exists(normal_path):
        success, message = texture_helpers.TextureHelpers.install_texture(
            obj, normal_path, 'NORMAL'
        )
        print(f"Normal texture: {message}")
    
    # Validate textures
    success, issues = texture_helpers.TextureHelpers.validate_textures(obj)
    if success:
        print("Texture validation: PASSED")
    else:
        print("Texture validation issues:")
        for issue in issues:
            print(f"  - {issue}")

def create_simple_armature():
    """Example: Create and validate an armature"""
    
    print("Creating armature...")
    
    # Create FO4 armature
    armature_obj = animation_helpers.AnimationHelpers.setup_fo4_armature()
    print(f"Armature created: {armature_obj.name}")
    
    # Validate armature
    success, issues = animation_helpers.AnimationHelpers.validate_animation(armature_obj)
    if success:
        print("Armature validation: PASSED")
    else:
        print("Armature validation issues:")
        for issue in issues:
            print(f"  - {issue}")
    
    return armature_obj

def export_mod_assets(output_dir):
    """Example: Export all assets in the scene"""
    
    print(f"Exporting mod to {output_dir}...")
    
    scene = bpy.context.scene
    
    # Export complete mod
    success, results = export_helpers.ExportHelpers.export_complete_mod(
        scene, output_dir
    )
    
    if success:
        print("Export completed successfully!")
        print(f"Meshes exported: {len(results['meshes'])}")
        print(f"Animations: {len(results['animations'])}")
        if results['errors']:
            print("Errors encountered:")
            for error in results['errors']:
                print(f"  - {error}")
    else:
        print("Export failed!")

def complete_workflow_example():
    """Complete example workflow"""
    
    print("=" * 60)
    print("Fallout 4 Mod Creation - Complete Workflow Example")
    print("=" * 60)
    
    # Clear existing scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Step 1: Create mesh
    print("\n1. Creating mesh...")
    weapon = create_simple_weapon()
    
    # Step 2: Setup materials (using dummy paths)
    print("\n2. Setting up materials...")
    mat = texture_helpers.TextureHelpers.setup_fo4_material(weapon)
    print(f"Material setup complete: {mat.name}")
    
    # Step 3: Validate before export
    print("\n3. Validating for export...")
    success, issues = export_helpers.ExportHelpers.validate_before_export(weapon)
    if success:
        print("Validation: PASSED - Ready for export!")
    else:
        print("Validation issues found:")
        for issue in issues:
            print(f"  - {issue}")
    
    # Step 4: Export (uncomment to actually export)
    # export_path = "/tmp/fo4_mod_output"
    # export_mod_assets(export_path)
    
    print("\n" + "=" * 60)
    print("Workflow example completed!")
    print("=" * 60)

# Run the complete workflow example
if __name__ == "__main__":
    complete_workflow_example()
