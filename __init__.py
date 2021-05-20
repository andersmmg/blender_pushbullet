bl_info = {
    "name" : "Pushbullet Notifications",
    "blender": (2, 80, 0),
    "category": "Tools",
    "author": "Andersmmg",
    "description": "Sends Pushbullet notifications for different events"
}

import bpy
from bpy.app.handlers import persistent
from bpy.props import *
from bpy.types import Operator, AddonPreferences
from .pushbullet import Pushbullet

class RequestAddonPreferences(AddonPreferences):
    bl_idname = __name__

    api_key: StringProperty(
            name="API Key",
            subtype='NONE',
            description="Your API key for Pushbullet",
            )

    n_rendered: BoolProperty(
            name="Render Complete",
            subtype='NONE',
            description="When a render has finished rendering and is ready for viewing",
            )

    n_cancelled: BoolProperty(
            name="Render Cancelled",
            subtype='NONE',
            description="When a render is cancelled before finishing",
            )

    def draw(self, context):
        layout = self.layout
        layout.label(text="You'll need to generate an API key from Pushbullet if you don't have one.")
        layout.prop(self, "api_key")
        layout.label(text="Choose the notifications you want to recieve")
        layout.prop(self, "n_rendered")
        layout.prop(self, "n_cancelled")

@persistent
def notify_render_complete(dummy):
    user_preferences = bpy.context.preferences
    addon_prefs = user_preferences.addons[__name__].preferences
    
    blend_name = get_blend()
    
    if addon_prefs.n_rendered:
        pb = Pushbullet(addon_prefs.api_key)
        push = pb.push_note("Render Complete", "%s has finished rendering" % (blend_name))

@persistent
def notify_render_cancel(dummy):
    user_preferences = bpy.context.preferences
    addon_prefs = user_preferences.addons[__name__].preferences
    
    blend_name = get_blend()
    
    if addon_prefs.n_cancelled:
        pb = Pushbullet(addon_prefs.api_key)
        push = pb.push_note("Render Cancelled", "%s cancelled rendering" % (blend_name))

# Get the name of the blend file
def get_blend():
    blend_name = bpy.path.basename(bpy.context.blend_data.filepath)
    if blend_name == "":
        blend_name = "unnamed file"
    
    return blend_name

def register():
    bpy.app.handlers.render_complete.append(notify_render_complete)
    bpy.app.handlers.render_cancel.append(notify_render_cancel)
    bpy.utils.register_class(RequestAddonPreferences)

def unregister():
    bpy.app.handlers.render_complete.remove(notify_render_complete)
    bpy.app.handlers.render_cancel.remove(notify_render_cancel)
    bpy.utils.unregister_class(RequestAddonPreferences)

