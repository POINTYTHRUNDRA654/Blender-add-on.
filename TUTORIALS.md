# Tutorial Guide

This guide provides detailed walkthroughs for using the Fallout 4 Tutorial Add-on.

## Tutorial 1: Creating Your First Fallout 4 Mesh

### Objective
Learn to create a basic mesh optimized for Fallout 4.

### Steps

#### 1. Start the Tutorial
1. Press `N` to open the sidebar
2. Click the "Fallout 4" tab
3. Click "Start Tutorial"
4. Select "Basic Mesh" from the dropdown
5. Click OK

#### 2. Create Base Mesh
1. In the Mesh Helpers panel, click "Create Base Mesh"
2. A cube optimized for FO4 will be created
3. The mesh has:
   - Applied scale (1,1,1)
   - UV map already created
   - Proper naming

#### 3. Edit the Mesh
1. Press `Tab` to enter Edit Mode
2. Select faces, edges, or vertices
3. Use standard Blender modeling tools:
   - `E` to extrude
   - `S` to scale
   - `R` to rotate
   - `G` to move
4. Model your object (e.g., a simple weapon or armor piece)

#### 4. Optimize for Fallout 4
1. Press `Tab` to return to Object Mode
2. With your mesh selected, click "Optimize for FO4"
3. This will:
   - Remove duplicate vertices
   - Recalculate normals
   - Triangulate faces (FO4 requirement)
   - Apply any unapplied transformations

#### 5. Validate Your Mesh
1. Click "Validate Mesh"
2. Review any warnings or errors
3. Common issues and solutions:
   - **Scale not applied**: Press `Ctrl+A > Scale`
   - **No UV map**: Tab to Edit Mode, press `U > Unwrap`
   - **Too many polygons**: Use Decimate modifier

#### 6. Check Notifications
Look at the Notifications section in the main panel to see a summary of operations and any issues.

### Tips
- Keep poly count under 65,535 (FO4 limit)
- Always apply transformations before optimizing
- Use reference images for better results
- Save your work frequently

---

## Tutorial 2: Setting Up Textures

### Objective
Learn to setup and install textures for your Fallout 4 mesh.

### Prerequisites
- Completed mesh from Tutorial 1
- Texture files ready (PNG, TGA, or DDS)

### Steps

#### 1. Prepare Your Textures
You need at least:
- **Diffuse/Color map**: The base color texture
- **Normal map**: For surface detail (optional but recommended)
- **Specular map**: For shininess/reflections (optional)

Recommended dimensions: 1024x1024 or 2048x2048 (power of 2)

#### 2. Setup FO4 Material
1. Select your mesh
2. In Texture Helpers panel, click "Setup FO4 Materials"
3. A new material with proper node setup is created
4. Switch to Shading workspace to see the nodes

#### 3. Install Diffuse Texture
1. Click "Install Texture"
2. Select "Diffuse" from the Texture Type dropdown
3. Browse to your diffuse texture file
4. Click "Install Texture"
5. The texture is loaded into the Diffuse node

#### 4. Install Normal Map
1. Click "Install Texture" again
2. Select "Normal" from Texture Type
3. Browse to your normal map
4. Click "Install Texture"
5. Colorspace is automatically set to "Non-Color"

#### 5. Install Specular Map (Optional)
1. Click "Install Texture" again
2. Select "Specular" from Texture Type
3. Browse to your specular map
4. Click "Install Texture"

#### 6. Validate Textures
1. Click "Validate Textures"
2. Review any warnings
3. Common issues:
   - **Dimensions not power of 2**: Resize to 512, 1024, 2048, etc.
   - **Wrong colorspace**: Automatically fixed by add-on

#### 7. Preview in Viewport
1. In the 3D Viewport, change viewport shading to "Material Preview" (3rd sphere icon)
2. You should see your textures applied

### Tips
- Use DDS format for final textures (FO4 native format)
- Keep texture sizes reasonable (2048x2048 max for most objects)
- Normal maps should be in tangent space
- Always validate before moving to next step

---

## Tutorial 3: Creating Animations

### Objective
Learn to setup a skeleton and create animations for Fallout 4.

### Prerequisites
- Completed mesh from Tutorial 1
- Understanding of armatures in Blender

### Steps

#### 1. Setup FO4 Armature
1. In Animation Helpers panel, click "Setup FO4 Armature"
2. A basic humanoid skeleton is created with:
   - Root bone
   - Spine
   - Head
   - Arms (left and right)
   - Legs (left and right)

#### 2. Position the Armature
1. Select the armature
2. Press `G` to move it to align with your mesh
3. Press `S` to scale if needed
4. Press `Tab` to enter Edit Mode
5. Adjust individual bones to match your mesh

#### 3. Parent Mesh to Armature
1. Select your mesh
2. Shift-select the armature
3. Press `Ctrl+P`
4. Choose "With Automatic Weights"
5. Blender will auto-weight paint your mesh

#### 4. Test the Rigging
1. Select the armature
2. Press `Ctrl+Tab` to enter Pose Mode
3. Select bones and move them (`G`), rotate (`R`)
4. Verify mesh deforms correctly
5. Press `Alt+G`, `Alt+R` to reset pose

#### 5. Create Animation
1. Switch to Animation workspace
2. Set timeline length (e.g., frame 1-60 for 1 second at 60fps)
3. At frame 1, select bones and press `I` to insert keyframe
4. Move to frame 30, pose the bones differently
5. Press `I` again to insert another keyframe
6. Play animation with spacebar

#### 6. Validate Animation
1. Return to Layout workspace
2. Select armature
3. Click "Validate Animation"
4. Review any issues:
   - **Too many bones**: FO4 limit is 256
   - **No animation data**: Create at least one keyframe
   - **Bone naming issues**: Avoid spaces in names

### Tips
- Start with simple animations (idle, walk)
- Keep bone count under 256
- Use constraints for complex movements
- Test in-game after export

---

## Exporting Your Mod

### Objective
Export your completed mod for use in Fallout 4.

### Prerequisites
- Completed and validated mesh
- Textures applied and validated
- Animations created (if needed)

### Steps

#### 1. Final Validation
1. Select your main object (mesh or armature)
2. Click "Validate Before Export"
3. Address any remaining issues
4. Ensure all validations pass

#### 2. Export Single Mesh
1. Select the mesh to export
2. In Export to FO4 panel, click "Export Mesh (.nif)"
3. Choose destination folder
4. Enter filename
5. Click "Export Mesh"
6. FBX file is created (convert to NIF with external tool)

#### 3. Export Complete Mod
1. Click "Export Complete Mod"
2. Choose destination folder
3. All meshes and assets are exported
4. Mod structure is created automatically:
   - `/meshes/` - Contains FBX files
   - `/textures/` - Copy your textures here manually
   - `/manifest.json` - Lists exported assets

#### 4. Convert to NIF
(Requires external tools)
1. Use NifSkope or Outfit Studio
2. Import the FBX files
3. Export as NIF format
4. Place in appropriate Fallout 4 data directory

#### 5. Test in Game
1. Copy files to Fallout 4 Data folder
2. Enable mod in mod manager or plugins.txt
3. Launch game and test
4. Iterate as needed

### Tips
- Always validate before exporting
- Keep backup of Blender files
- Document your mod structure
- Test thoroughly before release

---

## Common Workflows

### Armor Piece Workflow
1. Create base mesh → Optimize → Validate
2. Setup textures → Validate
3. Export → Convert to NIF
4. Test in Creation Kit with body references

### Weapon Workflow
1. Create weapon mesh → Optimize → Validate
2. Create grip armature if needed
3. Setup textures → Validate
4. Export → Convert to NIF
5. Setup in Creation Kit with weapon records

### Static Object Workflow
1. Create mesh → Optimize → Validate
2. Setup textures → Validate
3. Create collision mesh (optional)
4. Export → Convert to NIF
5. Place in world with Creation Kit

---

## Next Steps

After completing these tutorials:
1. Practice with more complex models
2. Experiment with advanced texturing
3. Learn about Fallout 4 material types (.bgsm, .bgem)
4. Study Creation Kit for mod integration
5. Join Fallout 4 modding communities

## Resources

- Fallout 4 Creation Kit Wiki
- Nexus Mods Fallout 4 forum
- Blender documentation
- NifSkope documentation
