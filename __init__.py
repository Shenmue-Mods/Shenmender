# <pep8-80 compliant>

bl_info = {
    "name": "Shenmender",
    "author": "Phil",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Blender tools for importing and exporting Shenmue 1 & 2 files.",
    "warning": "",
    "wiki_url": "",
    "support": "OFFICIAL",
    "category": "Import-Export"}

if "bpy" in locals():
    import importlib
    if "import_mt5" in locals():
        importlib.reload(import_mt5)
    if "import_mot" in locals():
        importlib.reload(import_mot)

import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
from . import import_mot
from . import import_mt5


class MT5ImportOperator(bpy.types.Operator, ImportHelper):

    #: Name of function for calling the MT5 import operator.
    bl_idname = "import_scene.mt5"

    #: How the MT5 import operator is labelled in the user interface.
    bl_label = "Import .MT5"

    filename_ext = ".mt5"
    filter_glob: StringProperty(default="*.mt5;", options={'HIDDEN'})

    def execute(self, context):
        path = "Importing " + self.properties.filepath
        self.report({'INFO'}, path)
        return import_mt5.load(context, self.properties.filepath)


class MOTImportOperator(bpy.types.Operator, ImportHelper):

    #: Name of function for calling the MOT import operator.
    bl_idname = "import_scene.mot"

    #: How the MOT import operator is labelled in the user interface.
    bl_label = "Import MOTION.BIN"

    filename_ext = ".bin"
    filter_glob: StringProperty(default="*.bin;", options={'HIDDEN'})

    def execute(self, context):
        path = "Importing " + self.properties.filepath
        self.report({'INFO'}, path)
        return import_mot.load(context, self.properties.filepath)


def menu_func_import(self, context):
    self.layout.operator(MT5ImportOperator.bl_idname, text="MT5 Model (.MT5)")
    self.layout.operator(MOTImportOperator.bl_idname, text="MOTION.BIN (.bin)")


def register():
    bpy.utils.register_class(MT5ImportOperator)
    bpy.utils.register_class(MOTImportOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(MT5ImportOperator)
    bpy.utils.unregister_class(MOTImportOperator)


if __name__ == "__main__":
    register()
