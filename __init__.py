"""
Desktop Tutorial Integration Add-on for Blender
Integrates Blender with a desktop tutorial application
"""

bl_info = {
    "name": "Desktop Tutorial Integration",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Tutorial",
    "description": "Integrates Blender with desktop tutorial application",
    "warning": "",
    "doc_url": "",
    "category": "Development",
}

import bpy
from bpy.types import Operator, Panel, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty


# Preferences
class TutorialAddonPreferences(AddonPreferences):
    bl_idname = __name__

    server_host: StringProperty(
        name="Server Host",
        description="Host address of the desktop tutorial app",
        default="localhost",
    )

    server_port: IntProperty(
        name="Server Port",
        description="Port number of the desktop tutorial app",
        default=8080,
        min=1024,
        max=65535,
    )

    auto_connect: BoolProperty(
        name="Auto Connect",
        description="Automatically connect to tutorial app on startup",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "server_host")
        layout.prop(self, "server_port")
        layout.prop(self, "auto_connect")


# Operators
class TUTORIAL_OT_connect(Operator):
    """Connect to Desktop Tutorial Application"""
    bl_idname = "tutorial.connect"
    bl_label = "Connect to Tutorial App"
    bl_options = {'REGISTER'}

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        
        try:
            # Store connection info in window manager
            wm = context.window_manager
            wm.tutorial_connected = True
            wm.tutorial_host = prefs.server_host
            wm.tutorial_port = prefs.server_port
            
            self.report({'INFO'}, f"Connected to {prefs.server_host}:{prefs.server_port}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to connect: {str(e)}")
            return {'CANCELLED'}


class TUTORIAL_OT_disconnect(Operator):
    """Disconnect from Desktop Tutorial Application"""
    bl_idname = "tutorial.disconnect"
    bl_label = "Disconnect from Tutorial App"
    bl_options = {'REGISTER'}

    def execute(self, context):
        wm = context.window_manager
        wm.tutorial_connected = False
        self.report({'INFO'}, "Disconnected from tutorial app")
        return {'FINISHED'}


class TUTORIAL_OT_send_event(Operator):
    """Send event to Desktop Tutorial Application"""
    bl_idname = "tutorial.send_event"
    bl_label = "Send Tutorial Event"
    bl_options = {'REGISTER'}

    event_type: StringProperty(
        name="Event Type",
        description="Type of event to send",
        default="action_completed",
    )

    event_data: StringProperty(
        name="Event Data",
        description="Data to send with the event",
        default="",
    )

    def execute(self, context):
        wm = context.window_manager
        
        if not wm.tutorial_connected:
            self.report({'WARNING'}, "Not connected to tutorial app")
            return {'CANCELLED'}
        
        try:
            # Prepare event data
            event = {
                "type": self.event_type,
                "data": self.event_data,
                "timestamp": bpy.context.scene.frame_current,
            }
            
            # Send to tutorial app (mock implementation)
            self.report({'INFO'}, f"Sent event: {self.event_type}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to send event: {str(e)}")
            return {'CANCELLED'}


class TUTORIAL_OT_request_next_step(Operator):
    """Request next tutorial step from Desktop Tutorial Application"""
    bl_idname = "tutorial.request_next_step"
    bl_label = "Next Tutorial Step"
    bl_options = {'REGISTER'}

    def execute(self, context):
        wm = context.window_manager
        
        if not wm.tutorial_connected:
            self.report({'WARNING'}, "Not connected to tutorial app")
            return {'CANCELLED'}
        
        try:
            # Request next step (mock implementation)
            self.report({'INFO'}, "Requested next tutorial step")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to request next step: {str(e)}")
            return {'CANCELLED'}


class TUTORIAL_OT_mark_complete(Operator):
    """Mark current tutorial step as complete"""
    bl_idname = "tutorial.mark_complete"
    bl_label = "Mark Step Complete"
    bl_options = {'REGISTER'}

    def execute(self, context):
        wm = context.window_manager
        
        if not wm.tutorial_connected:
            self.report({'WARNING'}, "Not connected to tutorial app")
            return {'CANCELLED'}
        
        try:
            # Mark step as complete
            event_data = {
                "step_id": wm.tutorial_current_step,
                "completed": True,
            }
            
            self.report({'INFO'}, f"Marked step {wm.tutorial_current_step} as complete")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to mark complete: {str(e)}")
            return {'CANCELLED'}


# UI Panel
class TUTORIAL_PT_main_panel(Panel):
    """Tutorial Integration Panel"""
    bl_label = "Desktop Tutorial"
    bl_idname = "TUTORIAL_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tutorial'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        # Connection status
        box = layout.box()
        box.label(text="Connection Status:")
        
        if wm.tutorial_connected:
            box.label(text="✓ Connected", icon='LINKED')
            box.operator("tutorial.disconnect", icon='UNLINKED')
        else:
            box.label(text="✗ Not Connected", icon='UNLINKED')
            box.operator("tutorial.connect", icon='LINKED')

        # Tutorial controls
        if wm.tutorial_connected:
            layout.separator()
            
            box = layout.box()
            box.label(text="Tutorial Controls:")
            box.operator("tutorial.request_next_step", icon='FORWARD')
            box.operator("tutorial.mark_complete", icon='CHECKMARK')
            
            layout.separator()
            
            box = layout.box()
            box.label(text="Current Step:")
            box.label(text=f"Step {wm.tutorial_current_step}")
            box.label(text=wm.tutorial_step_description)


# Registration
classes = (
    TutorialAddonPreferences,
    TUTORIAL_OT_connect,
    TUTORIAL_OT_disconnect,
    TUTORIAL_OT_send_event,
    TUTORIAL_OT_request_next_step,
    TUTORIAL_OT_mark_complete,
    TUTORIAL_PT_main_panel,
)


def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Add custom properties to window manager
    bpy.types.WindowManager.tutorial_connected = BoolProperty(
        name="Tutorial Connected",
        default=False,
    )
    
    bpy.types.WindowManager.tutorial_host = StringProperty(
        name="Tutorial Host",
        default="localhost",
    )
    
    bpy.types.WindowManager.tutorial_port = IntProperty(
        name="Tutorial Port",
        default=8080,
    )
    
    bpy.types.WindowManager.tutorial_current_step = IntProperty(
        name="Current Tutorial Step",
        default=1,
    )
    
    bpy.types.WindowManager.tutorial_step_description = StringProperty(
        name="Step Description",
        default="No active tutorial",
    )


def unregister():
    # Remove custom properties
    del bpy.types.WindowManager.tutorial_connected
    del bpy.types.WindowManager.tutorial_host
    del bpy.types.WindowManager.tutorial_port
    del bpy.types.WindowManager.tutorial_current_step
    del bpy.types.WindowManager.tutorial_step_description
    
    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
