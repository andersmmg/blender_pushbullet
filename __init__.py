bl_info = {
    "name" : "Pushbullet Notifications",
    "blender": (2, 80, 0),
    "category": "Tools",
    "author": "Andersmmg",
    "description": "Sends Pushbullet notifications when renders are complete"
}

import bpy
from bpy.app.handlers import persistent
from bpy.props import *
from bpy.types import Operator, AddonPreferences
from .pushbullet import Pushbullet

class NotificationTogglePanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Pushbullet Notifications"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        row = layout.row(align=True)
        row.prop(scene, "render_notification_toggle")
        row.prop(scene, "render_cancel_notification_toggle")

class RequestAddonPreferences(AddonPreferences):
    bl_idname = __name__

    api_key: StringProperty(
            name="API Key",
            subtype='NONE',
            description="Your API key for Pushbullet",
            )

    def draw(self, context):
        layout = self.layout
        layout.label(text="You'll need to generate an API key from Pushbullet if you don't have one.")
        layout.prop(self, "api_key")
        layout.label(text="Choose which notifications you want to recieve:")
        layout.label(text="Pushbullet Notifications section of the Render Properties panel.")

@persistent
def notify_render_complete(dummy):
    user_preferences = bpy.context.preferences
    addon_prefs = user_preferences.addons[__name__].preferences
    
    blend_name = get_blend()
    
    if bpy.context.scene.render_notification_toggle:
        pb = Pushbullet(addon_prefs.api_key)
        push = pb.push_note("Render Complete", "%s has finished rendering" % (blend_name))

@persistent
def notify_render_cancel(dummy):
    user_preferences = bpy.context.preferences
    addon_prefs = user_preferences.addons[__name__].preferences
    
    blend_name = get_blend()
    
    if bpy.context.scene.render_cancel_notification_toggle:
        pb = Pushbullet(addon_prefs.api_key)
        push = pb.push_note("Render Cancelled", "%s cancelled rendering" % (blend_name))

# Get the name of the blend file
def get_blend():
    blend_name = bpy.path.basename(bpy.context.blend_data.filepath)
    if blend_name == "":
        blend_name = "unnamed file"
    
    return blend_name

def register():
    bpy.types.Scene.render_notification_toggle = bpy.props.BoolProperty(
        name="Render Complete",
        description="Send a Pushbullet notification when a render is completed.",
        default = True)
    bpy.types.Scene.render_cancel_notification_toggle = bpy.props.BoolProperty(
        name="Render Cancelled",
        description="Send a Pushbullet notification when a render is cancelled before finishing.",
        default = False)
    bpy.utils.register_class(NotificationTogglePanel)
    bpy.app.handlers.render_complete.append(notify_render_complete)
    bpy.app.handlers.render_cancel.append(notify_render_cancel)
    bpy.utils.register_class(RequestAddonPreferences)

def unregister():
    bpy.utils.unregister_class(NotificationTogglePanel)
    bpy.app.handlers.render_complete.remove(notify_render_complete)
    bpy.app.handlers.render_cancel.remove(notify_render_cancel)
    bpy.utils.unregister_class(RequestAddonPreferences)

