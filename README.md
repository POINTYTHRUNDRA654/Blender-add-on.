# Blender Fallout 4 Tutorial Add-on

A comprehensive Blender add-on that provides a desktop tutorial system and helper tools for creating Fallout 4 mods. This add-on guides you through every step of the mod creation process, from mesh creation to final export.

**⚠️ Important:** This add-on is designed for **Fallout 4 modding with Havok physics**. It is **not compatible with NVIDIA PhysX**. See [COMPATIBILITY.md](COMPATIBILITY.md) for details.

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
- Collision mesh generation (basic geometry for Havok physics)

### 🖼️ Image to Mesh Conversion
- Convert images to 3D meshes using height maps
- Support for common image formats (PNG, JPG, BMP, TIFF, TGA)
- Adjustable displacement strength and mesh resolution
- Apply displacement maps to existing meshes
- Uses free resources: PIL/Pillow and NumPy

### 🤖 AI-Powered Generation (Optional)
- **NEW**: Generate 3D meshes from text descriptions using AI
- **NEW**: Create full 3D models from 2D images (not just height maps)
- Powered by Tencent's Hunyuan3D-2 model
- Completely optional - add-on works perfectly without it
- Requires: GPU, PyTorch, and Hunyuan3D-2 installation
- See installation guide for setup instructions

### 🎬 Motion Generation (Optional)
- **NEW**: Generate character animations from text descriptions
- **NEW**: Create motion sequences using AI
- Powered by Tencent's HY-Motion-1.0 model
- Import and apply motion data to Blender armatures
- Requires: git-lfs, PyTorch, and HY-Motion-1.0 installation
- Completely optional feature

### 🌐 Web Interface (Optional)
- **NEW**: Browser-based UI for AI generation powered by Gradio
- Easy-to-use interface (no command-line knowledge needed)
- Start/stop web server from Blender
- Access from any device on your network
- Text-to-3D and Image-to-3D generation via web browser
- Completely optional - install with `pip install gradio`

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

## Optional: AI Generation with Hunyuan3D-2

The add-on supports AI-powered 3D generation using Tencent's Hunyuan3D-2 model. This is **completely optional** - the add-on works perfectly without it.

### What is Hunyuan3D-2?

Hunyuan3D-2 is a powerful AI model that can:
- Generate 3D meshes from text descriptions
- Convert 2D images into full 3D models (not just height maps)
- Create textured, game-ready assets

### Prerequisites for AI Features

**Hardware Requirements:**
- NVIDIA GPU with CUDA support (8GB+ VRAM recommended)
- 20GB+ free disk space (for models and dependencies)
- 16GB+ RAM recommended

**Software Requirements:**
- PyTorch with CUDA support
- Hunyuan3D-2 repository and model weights

### Installation Steps

1. **Install PyTorch** (in Blender's Python environment):
```bash
# Windows
cd "C:\Program Files\Blender Foundation\Blender X.X\X.X\python\bin"
python.exe -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# macOS/Linux
cd /path/to/blender/X.X/python/bin
./python3.xx -m pip install torch torchvision
```

2. **Clone Hunyuan3D-2 repository**:
```bash
# Using GitHub CLI (recommended)
gh repo clone Tencent-Hunyuan/Hunyuan3D-2

# Or using git
git clone https://github.com/Tencent-Hunyuan/Hunyuan3D-2.git
```

3. **Install Hunyuan3D-2 dependencies**:
```bash
cd Hunyuan3D-2
pip install -r requirements.txt
```

4. **Download model weights**:
Follow the instructions in the Hunyuan3D-2 README to download the model weights.

5. **Restart Blender**

The add-on will automatically detect if Hunyuan3D-2 is installed and enable the AI features.

### Using AI Features

Once installed, you'll see an "AI Generation (Optional)" panel in the Fallout 4 sidebar:

- **Text to 3D**: Enter a description and generate a 3D model
- **Image to 3D**: Upload an image and get a full 3D model (not just height map)
- **Status Indicator**: Shows if Hunyuan3D-2 is available

### Note on AI Features

- AI generation is **experimental** and may require manual integration
- Model inference can be slow on CPU (GPU recommended)
- Generated meshes may need optimization for Fallout 4
- This is a beta feature - traditional methods work more reliably

## Optional: Gradio Web Interface

For an easy-to-use browser interface for AI generation, install Gradio:

```bash
# In Blender's Python environment
pip install gradio
```

Then in Blender:
1. Go to "AI Generation (Optional)" panel
2. Click "Start Web UI"
3. Open your browser to http://localhost:7860
4. Use the web interface for AI generation

**Benefits:**
- No command-line knowledge required
- User-friendly interface
- Works on any device with a browser
- Can create a shareable public link (optional)

## Optional: HY-Motion-1.0 for Motion Generation

For AI-powered animation and motion generation, install HY-Motion-1.0:

### Prerequisites
- git-lfs (Large File Storage)
- PyTorch
- Several GB of disk space

### Installation Steps

1. **Install git-lfs**:
```bash
# Windows (with Chocolatey)
choco install git-lfs

# macOS
brew install git-lfs

# Linux (Ubuntu/Debian)
sudo apt-get install git-lfs

# Initialize git-lfs
git lfs install
```

2. **Clone HY-Motion-1.0**:
```bash
git clone https://github.com/Tencent-Hunyuan/HY-Motion-1.0.git
cd HY-Motion-1.0/
```

3. **Pull model weights with git-lfs**:
```bash
git lfs pull
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

5. **Restart Blender**

The add-on will automatically detect HY-Motion-1.0 and enable motion features.

**Features:**
- Generate animations from text descriptions
- Import motion files (.bvh, .fbx)
- Apply motion to Blender armatures
- Create character animations with AI

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

#### 5. Generate with AI (Optional - Requires Hunyuan3D-2)
```
1. Install Hunyuan3D-2 (see AI Generation section below)
2. Expand "AI Generation (Optional)" panel
3. For text-to-3D:
   - Click "Generate from Text"
   - Enter description (e.g., "medieval sword")
   - Click OK to generate
4. For image-to-3D:
   - Click "Generate from Image (AI)"
   - Select your image
   - Full 3D model will be created (not just height map)
```

#### 6. Create Animations (Optional)
```
1. Click "Setup FO4 Armature" to create a skeleton
2. Parent your mesh to the armature
3. Create your animation
4. Click "Validate Animation" to check for issues
```

#### 7. Export Your Mod
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

## Best Free Resources for Image to Mesh

### For Creating/Editing Height Maps

**Image Editors:**
- **GIMP** (gimp.org) - Professional image editor for creating and editing height maps
- **Blender** - Use Blender's own texture painting to create height maps

**Height Map Generators:**
- **terrain.party** - Generate real-world terrain height maps from any location
- **tangrams.github.io/heightmapper** - Create height maps from map data
- **NASA Earth Observatory** - Download real terrain data

**Texture Libraries with Height Maps:**
- **polyhaven.com** - High-quality PBR textures including height maps
- **cgbookcase.com** - Free PBR textures with displacement maps
- **3dtextures.me** - Free seamless textures

### Tips for Best Results

1. **Use square images** (512x512, 1024x1024, 2048x2048) for best results
2. **Higher contrast** = more dramatic terrain
3. **Grayscale images** work best (bright = high, dark = low)
4. **Start with lower resolution** to test, then increase for final mesh
5. **See TUTORIALS.md** for detailed guide on using these resources

## Physics System Compatibility

### Important: Fallout 4 Uses Havok Physics, Not PhysX

**This add-on is designed for Fallout 4 modding, which uses Havok physics.**

- **Fallout 4 uses Havok:** All Bethesda Creation Engine games (Skyrim, Fallout 4, Starfield) use Havok physics
- **PhysX is not compatible:** NVIDIA PhysX (including NVIDIA-Omniverse/PhysX) is a different physics engine used in other games
- **This add-on does NOT require PhysX:** Everything works with Fallout 4's native Havok system

### What This Add-on Provides

**Collision Mesh Generation:**
- Creates simplified geometry for collision boundaries
- Exports to FBX/NIF format compatible with Fallout 4
- Basic collision shapes for static objects

**What This Add-on Does NOT Provide:**
- Full Havok physics simulation (requires Havok Content Tools)
- Ragdoll physics setup (requires Creation Kit)
- Dynamic physics properties (requires NifSkope + Creation Kit)
- PhysX support (not used in Fallout 4)

### For Advanced Physics in Fallout 4

If you need advanced physics features, use these tools **in addition to** this add-on:
1. **Havok Content Tools** - For creating physics simulations (available from Bethesda)
2. **NifSkope** - For editing collision properties in .nif files
3. **Creation Kit** - For setting up physics properties in-game
4. **This add-on** - For creating meshes and basic collision geometry

**Bottom line:** This add-on works perfectly for Fallout 4 modding. PhysX is not needed or compatible with Fallout 4.

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

### Image to Mesh Issues

**"PIL/Pillow not installed" or "NumPy not installed"**
- Solution: Install dependencies in Blender's Python (see Prerequisites section above)

**"Mesh looks flat or has no detail"**
- Solution: Increase "Displacement Strength" parameter
- Ensure your image has good contrast (not all one color)

**"Mesh has too many polygons"**
- Solution: Use smaller "Subdivisions" value or let it auto-calculate (set to 0)
- Use a smaller resolution image

**"Unsupported image format"**
- Solution: Convert your image to PNG, JPG, BMP, TIFF, or TGA format

### AI Generation Issues

**"Hunyuan3D-2 not available"**
- Solution: Install Hunyuan3D-2 following the instructions in the "Optional: AI Generation" section
- Check that PyTorch is installed in Blender's Python environment
- Verify the Hunyuan3D-2 repository is cloned in a standard location

**"PyTorch not installed"**
- Solution: Install PyTorch in Blender's Python environment:
  ```bash
  python -m pip install torch torchvision
  ```

**"Hunyuan3D-2 not found"**
- Solution: Clone the repository:
  ```bash
  gh repo clone Tencent-Hunyuan/Hunyuan3D-2
  ```
- Place it in your home directory or Projects folder
- Restart Blender after installation

**AI features grayed out**
- This is normal if Hunyuan3D-2 is not installed
- AI features are optional - other features work without it
- Click "Installation Info" for setup instructions

**"Text-to-3D generation not yet implemented"**
- The AI integration is in beta/placeholder state
- Manual integration with Hunyuan3D-2 inference code required
- See their documentation for direct usage
- Traditional mesh creation methods work reliably

### Motion Generation Issues

**"HY-Motion-1.0 not available"**
- Solution: Install HY-Motion-1.0 following the instructions above
- Check that git-lfs is installed: `git lfs version`
- Verify PyTorch is installed in Blender's Python
- Check the repository is cloned and lfs files pulled

**"git-lfs not installed"**
- Solution: Install git-lfs for your platform
  - Windows: `choco install git-lfs` or download from git-lfs.github.com
  - macOS: `brew install git-lfs`
  - Linux: `sudo apt-get install git-lfs`
- Run `git lfs install` after installation

**"Motion generation not yet implemented"**
- The motion integration is in placeholder state
- Manual integration with HY-Motion-1.0's inference code required
- See their documentation for direct usage
- Generated animations can be imported as .bvh or .fbx files

**"Import motion file failed"**
- Check file format (.bvh or .fbx supported)
- Verify file path is correct
- Try importing manually: File → Import → Motion Capture (.bvh)

## Documentation

This add-on comes with comprehensive documentation:

- **[README.md](README.md)** - Main documentation (you are here)
- **[INSTALLATION.md](INSTALLATION.md)** - Installation instructions
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[TUTORIALS.md](TUTORIALS.md)** - Detailed tutorials
- **[FAQ.md](FAQ.md)** - Frequently asked questions
- **[API_REFERENCE.md](API_REFERENCE.md)** - API documentation for scripting
- **[COMPATIBILITY.md](COMPATIBILITY.md)** - Compatibility with PhysX, other tools, and platforms
- **[NVIDIA_RESOURCES.md](NVIDIA_RESOURCES.md)** - NVIDIA repositories and tools that can help with Blender add-on development
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## Version History

### 1.0.0 (Initial Release)
- Tutorial system with three tutorials
- Error notification system
- Mesh creation and optimization tools
- Texture setup and validation
- Animation helpers
- Export functionality
- Complete mod structure generation