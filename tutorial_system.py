"""
Tutorial system for guiding users through Fallout 4 mod creation
"""

import bpy
from bpy.props import StringProperty, IntProperty

class TutorialStep:
    """Represents a single tutorial step"""
    def __init__(self, title, description, action=None, validation=None):
        self.title = title
        self.description = description
        self.action = action
        self.validation = validation

class Tutorial:
    """Represents a complete tutorial"""
    def __init__(self, name, description, steps):
        self.name = name
        self.description = description
        self.steps = steps
        self.current_step = 0
    
    def get_current_step(self):
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            return True
        return False
    
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            return True
        return False

# Tutorial definitions
TUTORIALS = {}

def create_basic_mesh_tutorial():
    """Tutorial for creating a basic mesh for Fallout 4"""
    steps = [
        TutorialStep(
            "Create Base Mesh",
            "Start by creating a base mesh. Use Shift+A to add a mesh object.",
        ),
        TutorialStep(
            "Apply Scale",
            "Apply the object's scale by pressing Ctrl+A and selecting 'Scale'.",
        ),
        TutorialStep(
            "Add UV Map",
            "Add a UV map by entering Edit mode (Tab), pressing U, and selecting 'Unwrap'.",
        ),
        TutorialStep(
            "Optimize Mesh",
            "Use the 'Optimize for FO4' button to ensure mesh meets Fallout 4 requirements.",
        ),
        TutorialStep(
            "Add Materials",
            "Add materials to your mesh using the 'Setup FO4 Materials' button.",
        ),
    ]
    return Tutorial("Basic Mesh Creation", "Learn to create a basic mesh for Fallout 4", steps)

def create_texture_tutorial():
    """Tutorial for setting up textures"""
    steps = [
        TutorialStep(
            "Prepare Textures",
            "Prepare your texture files (diffuse, normal, specular) in DDS format.",
        ),
        TutorialStep(
            "Setup Material",
            "Use 'Setup FO4 Materials' to create a Fallout 4 compatible material.",
        ),
        TutorialStep(
            "Install Textures",
            "Use 'Install Texture' to load your texture files into the material.",
        ),
        TutorialStep(
            "Validate",
            "Validate your textures using the 'Validate Textures' button.",
        ),
    ]
    return Tutorial("Texture Setup", "Learn to setup textures for Fallout 4", steps)

def create_animation_tutorial():
    """Tutorial for creating animations"""
    steps = [
        TutorialStep(
            "Setup Armature",
            "Use 'Setup FO4 Armature' to create a Fallout 4 compatible skeleton.",
        ),
        TutorialStep(
            "Weight Paint",
            "Enter Weight Paint mode and paint vertex weights for each bone.",
        ),
        TutorialStep(
            "Create Animation",
            "Switch to Animation workspace and create your animation keyframes.",
        ),
        TutorialStep(
            "Validate",
            "Use 'Validate Animation' to check for common issues.",
        ),
    ]
    return Tutorial("Animation Setup", "Learn to create animations for Fallout 4", steps)

def initialize_tutorials():
    """Initialize all available tutorials"""
    TUTORIALS['basic_mesh'] = create_basic_mesh_tutorial()
    TUTORIALS['textures'] = create_texture_tutorial()
    TUTORIALS['animation'] = create_animation_tutorial()
    
    # Store in scene
    bpy.types.Scene.fo4_current_tutorial = StringProperty(
        name="Current Tutorial",
        default=""
    )
    bpy.types.Scene.fo4_tutorial_step = IntProperty(
        name="Tutorial Step",
        default=0
    )

def get_current_tutorial(context):
    """Get the currently active tutorial"""
    tutorial_name = context.scene.fo4_current_tutorial
    if tutorial_name in TUTORIALS:
        tutorial = TUTORIALS[tutorial_name]
        tutorial.current_step = context.scene.fo4_tutorial_step
        return tutorial
    return None

def register():
    """Register tutorial properties"""
    pass  # Properties initialized in initialize_tutorials()

def unregister():
    """Unregister tutorial properties"""
    if hasattr(bpy.types.Scene, 'fo4_current_tutorial'):
        del bpy.types.Scene.fo4_current_tutorial
    if hasattr(bpy.types.Scene, 'fo4_tutorial_step'):
        del bpy.types.Scene.fo4_tutorial_step
