# <pep8 compliant>

import bpy
from bpy_extras.wm_utils.progress_report import ProgressReport

from .modules.ShenmueDKPy.files.models.mt5 import MT5


def load(context, filepath):
    """
    Called by the user interface or another script.
    load_obj(path) - should give acceptable results.
    This function passes the file and sends the data off
        to be split into objects and then converted into mesh objects
    """

    with ProgressReport(context.window_manager) as progress:
        progress.enter_substeps(1, "Importing MT5 %r..." % filepath)

        progress.enter_substeps(2, "Reading MT5...")
        mt5 = MT5()
        mt5.read(filepath)
        progress.leave_substeps("Done.")

        progress.enter_substeps(2, "Creating animation rig...")

        # create armature
        armature = bpy.data.armatures.new('ShenmueRig')
        obj = bpy.data.objects.new('ShenmueRig', armature)
        bpy.context.scene.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        bpy.context.view_layer.update()
        bpy.ops.object.mode_set(mode='EDIT')

        # create root
        root = armature.edit_bones.new('Root')
        root.head[:] = 0.0, 0.0, 0.0
        root.tail[:] = 0.0, 0.0, 0.0
        root.roll = 0.0
        root.use_connect = True

        # create bones from nodes
        nodes = mt5.root_node.get_all_nodes()[1:]
        node_bone_dict = {mt5.root_node: root}
        for node in nodes:
            bone = armature.edit_bones.new(str(node.get_bone_id()))
            node_bone_dict[node] = bone
            parent_pos = node.parent.get_global_position()
            pos = node.get_global_position()
            bone.head[:] = parent_pos.x, parent_pos.y, parent_pos.z
            bone.tail[:] = pos.x, pos.y, pos.z
            bone.roll = 0.0
            bone.use_connect = True
            bone.parent = node_bone_dict[node.parent]

        # create IK bones and constraints

        progress.leave_substeps("Done.")

        progress.leave_substeps("Finished importing: %r" % filepath)

    return {'FINISHED'}
