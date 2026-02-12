# Blender Fallout 4 Tutorial Add-on

A comprehensive Blender add-on that provides a desktop tutorial system and helper tools for creating Fallout 4 mods. This add-on guides you through every step of the mod creation process, from mesh creation to final export.

## Features

### 🎓 Tutorial System
- Interactive step-by-step tutorials for:
  - Basic mesh creation
  - Texture setup
  - Animation workflow
- Real-time guidance and tips
- Progress tracking

### 🔔 Error Notification System
- Real-time error detection
- Automatic validation checks
- Clear, actionable warnings
- Helps you avoid common mistakes

### 🎨 Mesh Creation Helpers
- Create FO4-optimized base meshes
- Automatic mesh optimization
- Poly count validation
- UV mapping checks
- Collision mesh generation

### 🖼️ Image to Mesh Conversion
- Convert images to 3D meshes using height maps
- Support for common image formats (PNG, JPG, BMP, TIFF, TGA)
- Adjustable displacement strength and mesh resolution
- Apply displacement maps to existing meshes
- Uses free resources: PIL/Pillow and NumPy

### 🎨 Texture Installation
- FO4-compatible material setup
- Easy texture loading (diffuse, normal, specular)
- Texture validation
- Power-of-2 dimension checking

### 🎭 Animation Tools
- FO4-compatible armature generation
- Automatic weight painting
- Animation validation
- Bone count checking

### 📦 Export Functionality
- Export to FBX (convertible to NIF)
- Complete mod package export
- Pre-export validation
- Automatic mod directory structure creation

## Prerequisites for Image to Mesh Feature

To use the Image to Mesh functionality, you need to install the following free Python packages in Blender's Python environment:

1. **PIL/Pillow** - For image processing
2. **NumPy** - For numerical operations

### Installing Dependencies

**On Windows:**
```bash
# Open command prompt as administrator
cd "C:\Program Files\Blender Foundation\Blender X.X\X.X\python\bin"
python.exe -m pip install Pillow numpy
```

**On macOS:**
```bash
# Open terminal
cd /Applications/Blender.app/Contents/Resources/X.X/python/bin
./python3.xx -m pip install Pillow numpy
```

**On Linux:**
```bash
# Open terminal
cd /path/to/blender/X.X/python/bin
./python3.xx -m pip install Pillow numpy
```

Note: Replace `X.X` with your Blender version number (e.g., 3.6).


## Installation

1. Download the add-on files
2. In Blender, go to `Edit > Preferences > Add-ons`
3. Click `Install...` and select the add-on ZIP file or folder
4. Enable the "Fallout 4 Tutorial Helper" add-on

## Usage

### Accessing the Add-on

After installation, find the add-on in the 3D Viewport sidebar:
1. Press `N` to open the sidebar
2. Click on the "Fallout 4" tab

### Quick Start Guide

#### 1. Start a Tutorial
- Click "Start Tutorial" in the main panel
- Choose a tutorial type (Basic Mesh, Textures, or Animation)
- Follow the step-by-step instructions

#### 2. Create a Basic Mesh
```
1. Click "Create Base Mesh" to start with a FO4-optimized cube
2. Edit the mesh to your needs
3. Click "Optimize for FO4" to ensure compatibility
4. Click "Validate Mesh" to check for issues
```

#### 3. Setup Materials and Textures
```
1. Select your mesh
2. Click "Setup FO4 Materials" to create a material with proper nodes
3. Click "Install Texture" to load your texture files
4. Click "Validate Textures" to check compatibility
```

#### 4. Create Mesh from Image (New!)
```
1. Click "Image to Mesh (Height Map)" in the Image to Mesh panel
2. Select a grayscale image (bright areas = high, dark areas = low)
3. Adjust mesh width, height, and displacement strength
4. The mesh will be created automatically with proper UV mapping
```
OR
```
1. Select an existing mesh
2. Click "Apply Displacement Map"
3. Choose your height map image
4. Adjust displacement strength
```

#### 5. Create Animations (Optional)
```
1. Click "Setup FO4 Armature" to create a skeleton
2. Parent your mesh to the armature
3. Create your animation
4. Click "Validate Animation" to check for issues
```

#### 6. Export Your Mod
```
1. Select your object(s)
2. Click "Validate Before Export" to check everything
3. Click "Export Mesh (.nif)" for single objects
   OR
   Click "Export Complete Mod" for all assets
```

## Validation Checks

The add-on automatically checks for common issues:

### Mesh Validation
- ✓ Vertex and polygon count
- ✓ UV mapping presence
- ✓ Loose vertices
- ✓ Applied scale (must be 1,1,1)
- ✓ Maximum poly count (65535 for FO4)

### Texture Validation
- ✓ Material node setup
- ✓ Texture file loading
- ✓ Power-of-2 dimensions (recommended)
- ✓ Proper colorspace (Non-Color for normals/specular)

### Animation Validation
- ✓ Bone count (max 256 for FO4)
- ✓ Root bone presence
- ✓ Bone naming conventions
- ✓ Animation length

## Notification System

The add-on provides real-time notifications:
- **INFO** (Blue): Successful operations
- **WARNING** (Yellow): Potential issues that should be addressed
- **ERROR** (Red): Critical problems that must be fixed

Recent notifications appear in the main panel and in Blender's interface.

## Scripting Interface

You can also use the add-on's functionality through Python scripts in Blender's scripting workspace.

## Fallout 4 Mod Creation Workflow

1. **Planning** - Decide what type of mod you want to create
2. **Mesh Creation** - Use "Mesh Helpers" to create and optimize
3. **Texturing** - Use "Texture Helpers" to setup materials
4. **Animation** - Use "Animation Helpers" if needed
5. **Export** - Use "Export to FO4" to package your mod
6. **Testing** - Test in Creation Kit or game

## Troubleshooting

### Common Issues

**"No mesh object selected"**
- Solution: Click on your mesh object in the 3D viewport to select it

**"Poly count too high"**
- Solution: Use the Decimate modifier or manually reduce polygon count
- FO4 limit: 65,535 polygons per mesh

**"Object scale is not applied"**
- Solution: Press Ctrl+A and select "Scale" to apply the scale

**"No UV map found"**
- Solution: Enter Edit mode (Tab), press U, and select "Unwrap"

## Version History

### 1.0.0 (Initial Release)
- Tutorial system with three tutorials
- Error notification system
- Mesh creation and optimization tools
- Texture setup and validation
- Animation helpers
- Export functionality
- Complete mod structure generation