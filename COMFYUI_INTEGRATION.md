# ComfyUI Integration for Fallout 4 Blender Add-on

This guide covers setting up ComfyUI and its extensions for advanced texture and image generation workflows with the Fallout 4 Blender Add-on.

## What is ComfyUI?

ComfyUI is a powerful and modular node-based interface for Stable Diffusion and other generative AI models. It's particularly useful for:
- Generating textures for 3D models
- Creating concept art for Fallout 4 mods
- Generating reference images
- Upscaling and enhancing textures

## Installation

### Step 1: Install ComfyUI

You have several options for installing ComfyUI:

#### Option A: Standard Installation (Recommended for developers)

**Using GitHub CLI:**
```bash
gh repo clone Comfy-Org/ComfyUI
cd ComfyUI
```

**Using Git:**
```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

#### Option B: Portable Installation (Windows users)

Download the portable version from ComfyUI releases. This includes:
- Embedded Python interpreter (`python_embeded` folder)
- All required dependencies pre-installed
- No system Python configuration needed

**Benefits:**
- ✅ No Python installation required
- ✅ Self-contained
- ✅ Easy to move/backup
- ✅ No conflicts with system Python

**Note:** When using portable version, use `.\python_embeded\python.exe` for all pip commands.

### Step 2: Install Dependencies

**For Standard Installation:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install PyTorch (if not already installed)
# For CUDA (NVIDIA GPU):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CPU only:
pip install torch torchvision
```

**For Portable ComfyUI (Windows with embedded Python):**
```cmd
# ComfyUI portable versions include python_embeded folder
cd ComfyUI

# Install requirements using embedded Python
.\python_embeded\python.exe -s -m pip install -r requirements.txt

# Install PyTorch for embedded Python
# For CUDA:
.\python_embeded\python.exe -s -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CPU:
.\python_embeded\python.exe -s -m pip install torch torchvision
```

### Step 3: Install ComfyUI-GGUF Extension (Recommended)

The GGUF extension allows you to use quantized models for better performance:

```bash
# Navigate to custom_nodes directory
cd custom_nodes

# Clone GGUF extension
git clone https://github.com/city96/ComfyUI-GGUF.git
```

**Install dependencies:**

**For Standard Python Installation:**
```bash
cd ComfyUI-GGUF
pip install -r requirements.txt
```

**For Portable/Embedded Python (Windows):**
```cmd
# If ComfyUI has embedded Python (portable version)
cd ComfyUI
.\python_embeded\python.exe -s -m pip install -r .\custom_nodes\ComfyUI-GGUF\requirements.txt
```

**For System Python (Windows):**
```cmd
cd ComfyUI\custom_nodes\ComfyUI-GGUF
python -m pip install -r requirements.txt
```

### Step 4: Download Models

ComfyUI requires at least one generative model. We recommend starting with FLUX.1-dev:

#### FLUX.1-dev (Recommended - State of the Art)

FLUX.1-dev is one of the most advanced text-to-image models available:

```bash
# Clone FLUX.1-dev from Hugging Face
git clone https://huggingface.co/black-forest-labs/FLUX.1-dev

# Or download specific files:
# Place in: ComfyUI/models/checkpoints/
```

**FLUX.1-dev Features:**
- ✅ Exceptional image quality
- ✅ Better text rendering
- ✅ Improved prompt understanding
- ✅ Great for textures and concepts
- ✅ 12B parameter model

**Requirements:**
- VRAM: 12GB+ recommended (8GB minimum with optimizations)
- Storage: ~24GB
- GGUF quantized versions available for lower VRAM

#### Alternative Models

**Stable Diffusion Models:**
- Stable Diffusion 1.5 (4GB VRAM)
- Stable Diffusion XL (8GB VRAM)
- Realistic Vision
- DreamShaper

**Where to Download:**
- [Hugging Face](https://huggingface.co/models)
- [Civitai](https://civitai.com/)

**Model Locations:**
```
ComfyUI/models/
├── checkpoints/        # Main models (SD, FLUX, etc.)
├── loras/             # LoRA adapters
├── vae/               # VAE models
├── controlnet/        # ControlNet models
└── upscale_models/    # Upscalers
```

## Running ComfyUI

### Start the Server

```bash
# From ComfyUI directory
python main.py

# Or with custom port:
python main.py --port 8188

# For listening on all interfaces:
python main.py --listen 0.0.0.0
```

### Access the Interface

Open your browser and navigate to:
```
http://localhost:8188
```

## Integration with Blender Add-on

### Workflow 1: Generate Textures

1. **In ComfyUI:**
   - Load a workflow for texture generation
   - Set prompt: "rusty metal texture, post-apocalyptic, weathered"
   - Generate texture
   - Save image

2. **In Blender:**
   - Select your mesh
   - Go to Fallout 4 panel
   - Use "Smart Material Setup" operator
   - Browse to generated texture
   - Apply to model

### Workflow 2: Concept to 3D

1. **Generate concept art in ComfyUI:**
   - Prompt: "fallout 4 style weapon, rifle, side view, white background"
   - Save image

2. **Convert to 3D in Blender:**
   - Go to AI Generation panel
   - Use Shap-E "Image to 3D" feature
   - Select concept art image
   - Generate 3D mesh

3. **Refine and export:**
   - Use mesh optimization tools
   - Apply materials
   - Export for Fallout 4

### Workflow 3: Texture Enhancement

1. **Export UV map from Blender:**
   - UV unwrap your mesh
   - Export UV layout as image

2. **Generate texture in ComfyUI:**
   - Use UV map as control input
   - Generate texture matching UV layout
   - Prompt: "vault-tec texture, blue and yellow, metal panels"

3. **Apply in Blender:**
   - Import generated texture
   - Apply to mesh using UV mapping

## ComfyUI-GGUF Benefits

### Why Use GGUF Format?

**Traditional Models:**
- Size: 5-7 GB (FP16)
- VRAM: 6-8 GB required
- Speed: ~5-10 seconds per image

**GGUF Models:**
- Size: 2-4 GB (quantized)
- VRAM: 3-5 GB required
- Speed: ~3-8 seconds per image
- Quality: Minimal loss with proper quantization

### Quantization Levels

| Level | Size Reduction | Quality | Best For |
|-------|----------------|---------|----------|
| Q4_0  | 75% smaller    | Good    | Fast iteration |
| Q5_0  | 65% smaller    | Better  | Balanced |
| Q8_0  | 50% smaller    | Excellent | Production |
| FP16  | Original       | Perfect | Reference |

### Using GGUF Models

1. Download GGUF models from Hugging Face
2. Place in `models/checkpoints/`
3. Load in ComfyUI (GGUF loader node)
4. Works with all standard workflows

## Useful ComfyUI Extensions

### Essential Extensions

Install in `custom_nodes/` directory:

```bash
cd ComfyUI/custom_nodes

# 1. ComfyUI Manager (highly recommended)
git clone https://github.com/ltdrdata/ComfyUI-Manager.git

# 2. ControlNet
git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git

# 3. Image Enhancement
git clone https://github.com/WASasquatch/was-node-suite-comfyui.git

# 4. Upscaling
git clone https://github.com/ssitu/ComfyUI_UltimateSDUpscale.git
```

Restart ComfyUI after installing extensions.

## Workflows for FO4 Modding

### Pre-made Workflow Ideas

1. **Texture Generator**
   - Input: Text prompt
   - Output: Tileable texture
   - Nodes: Text encoder, SD model, tiling

2. **Concept Art Generator**
   - Input: Description + style
   - Output: Concept image
   - Nodes: Text encoder, SD model, post-processing

3. **Texture Upscaler**
   - Input: Low-res texture
   - Output: High-res texture
   - Nodes: Upscale model, detail enhancement

4. **PBR Material Generator**
   - Input: Base texture
   - Output: Diffuse, normal, roughness maps
   - Nodes: Multiple generators, image processing

### Save Workflows

1. Create workflow in ComfyUI
2. Click "Save" button
3. Store in your project folder
4. Load anytime with "Load" button

## Performance Optimization

### For Texture Generation

**Fast iteration:**
```
- Use GGUF Q4_0 models
- Reduce image resolution (512x512)
- Fewer sampling steps (20-25)
- Simple prompts
```

**High quality:**
```
- Use GGUF Q8_0 or FP16 models
- Higher resolution (1024x1024+)
- More sampling steps (30-50)
- Detailed prompts with negative prompts
```

### Memory Management

**Low VRAM (4GB):**
- Use GGUF Q4_0 models
- Enable `--lowvram` flag
- Generate smaller images
- Close other applications

**Medium VRAM (8GB):**
- Use GGUF Q5_0/Q8_0 models
- Standard settings work well
- Can generate 1024x1024

**High VRAM (12GB+):**
- Use any models
- Can use SDXL models
- Batch generation
- High resolution

## Troubleshooting

### ComfyUI Won't Start

**Check Python version:**
```bash
python --version  # Should be 3.8+
```

**Reinstall dependencies:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Models Not Loading

**GGUF models:**
- Ensure ComfyUI-GGUF extension is installed
- Check model is in correct directory
- Restart ComfyUI

**Standard models:**
- Verify file isn't corrupted
- Check file extension (.safetensors or .ckpt)
- Ensure sufficient disk space

### Out of Memory Errors

**Solutions:**
1. Use GGUF quantized models (Q4_0)
2. Reduce image resolution
3. Add `--lowvram` flag when starting ComfyUI
4. Close other GPU applications
5. Use CPU mode if necessary: `--cpu`

### Slow Generation

**Optimizations:**
1. Enable xformers: `--xformers`
2. Use GGUF models
3. Reduce sampling steps
4. Use smaller resolution
5. Upgrade GPU (if possible)

## Integration Examples

### Example 1: Weapon Texture Pipeline

```bash
# 1. Start ComfyUI
python main.py

# 2. In ComfyUI interface:
#    - Load texture generation workflow
#    - Prompt: "rusty assault rifle texture, military green, worn"
#    - Generate and save to: textures/weapon_diffuse.png

# 3. In Blender (with add-on):
import bpy
bpy.ops.fo4.smart_material_setup()
# Browse to weapon_diffuse.png
# Material automatically created

# 4. Export mesh
bpy.ops.fo4.export_mesh()
```

### Example 2: Environment Prop Creation

```bash
# 1. Generate concept in ComfyUI
#    Prompt: "post-apocalyptic barrel, side view, game asset"

# 2. Use Shap-E in Blender
import bpy
bpy.context.scene.fo4_shap_e_image_path = "concept_barrel.png"
bpy.ops.fo4.generate_shap_e_image()

# 3. Generate texture in ComfyUI
#    Upload UV layout, generate detailed texture

# 4. Apply and optimize
bpy.ops.fo4.optimize_mesh()
bpy.ops.fo4.smart_material_setup()
bpy.ops.fo4.validate_mesh()
```

## Best Practices

### For Fallout 4 Textures

1. **Resolution:**
   - Small props: 512x512 or 1024x1024
   - Weapons/armor: 2048x2048
   - Large objects: 4096x4096

2. **Format:**
   - Generate as PNG (lossless)
   - Convert to DDS for FO4

3. **Style matching:**
   - Use reference images from FO4
   - Include style keywords: "fallout 4 style", "post-apocalyptic"
   - Study vanilla game textures

4. **PBR workflow:**
   - Generate base color (diffuse)
   - Create normal map
   - Generate roughness/metallic maps
   - Test in Blender before export

### Prompting Tips

**Good prompts for FO4:**
- "rusty metal texture, weathered, post-apocalyptic, high detail"
- "vault-tec panel texture, blue and yellow, sci-fi, worn"
- "concrete wall texture, damaged, bullet holes, wasteland"

**Negative prompts:**
- "blurry, low quality, watermark, text"
- "modern, clean, pristine, new"

## Resources

### Model Sources

- **Hugging Face**: https://huggingface.co/models
- **Civitai**: https://civitai.com/
- **GGUF Models**: Search for "[model name] GGUF" on Hugging Face

### Tutorials

- ComfyUI official examples
- YouTube tutorials for ComfyUI
- Fallout 4 modding texture guides

### Community

- ComfyUI Discord
- r/StableDiffusion
- Fallout 4 modding forums

## Summary

ComfyUI with GGUF support provides:
- ✅ Professional texture generation
- ✅ Efficient memory usage
- ✅ Fast iteration for mod development
- ✅ High-quality results
- ✅ Flexible workflow creation

Combined with the Fallout 4 Blender Add-on, you have a complete pipeline from concept to in-game asset!

---

**Version:** 1.0
**Last Updated:** 2026-02-17
**Compatible with:** ComfyUI latest, GGUF extension latest
