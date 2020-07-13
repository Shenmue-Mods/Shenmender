# <pep8 compliant>

import bpy
from bpy_extras.wm_utils.progress_report import ProgressReport

from .modules.ShenmueDKPy.files.animation.motn import MOTN
from .modules.ShenmueDKPy.utils.model import *

ShenmueRigMap = {
    'IKBoneID.Root': 'BoneID.Root',
    #'IKBoneID.Spine': 'BoneID.Spine',
    #'IKBoneID.Hip': 'BoneID.Hip',
    #'IKBoneID.HandIKTarget_R': 'BoneID.Hand_IK_R',
    #'IKBoneID.HandIKTarget_L': 'BoneID.Hand_IK_L',
    'IKBoneID.FootIKTarget_R': 'BoneID.Foot_IK_R',
    'IKBoneID.FootIKTarget_L': 'BoneID.Foot_IK_L',
    #'IKBoneID.Shoulder_R': 'BoneID.Shoulder_R',
    #'IKBoneID.Shoulder_L': 'BoneID.Shoulder_L',
}

def load(context, filepath):
    """
    Called by the user interface or another script.
    load_obj(path) - should give acceptable results.
    This function passes the file and sends the data off
        to be split into objects and then converted into mesh objects
    """

    with ProgressReport(context.window_manager) as progress:
        progress.enter_substeps(1, "Importing MOTION.BIN %r..." % filepath)

        progress.enter_substeps(2, "Reading MOTION.BIN...")
        motn = MOTN()
        motn.read(filepath)
        progress.leave_substeps("Done.")

        # get the armature
        armature = bpy.context.scene.objects['ShenmueRig']
        bpy.context.view_layer.objects.active = armature
        armature.select_set(True)
        bpy.ops.object.mode_set(mode='POSE')

        # set rotation mode to euler angle for all bones
        for bone in armature.pose.bones:
            bone.rotation_mode = "XYZ"

        progress.enter_substeps(2, "Loading sequences to selected rig...")
        for sequence in motn.sequences:

            # debug walk selection
            if sequence.name == "A_WALK_L_02":
                print("A_WALK_L_02\n")
                for bone_data in sequence.data.bone_keyframes:
                    bone_id = str(IKBoneID(bone_data.bone_index))
                    print(bone_id)
                    if bone_id in ShenmueRigMap:
                        bone_name = ShenmueRigMap[bone_id]
                        for bone in armature.pose.bones:

                            if bone.name == bone_name:

                                print(bone_id, bone_name)

                                for pos_x in bone_data.pos_x:
                                    bone.location = [pos_x.value, 0.0, 0.0]
                                    bone.keyframe_insert(data_path="location", index=0, frame=pos_x.frame)
                                for pos_y in bone_data.pos_z:
                                    bone.location = [0.0, pos_y.value, 0.0]
                                    bone.keyframe_insert(data_path="location", index=1, frame=pos_y.frame)
                                for pos_z in bone_data.pos_y:
                                    bone.location = [0.0, 0.0, pos_z.value]
                                    bone.keyframe_insert(data_path="location", index=2, frame=pos_z.frame)

                                for rot_x in bone_data.rot_x:
                                    bone.rotation_euler = [rot_x.value, 0.0, 0.0]
                                    bone.keyframe_insert(data_path="rotation_euler", index=0, frame=rot_x.frame)
                                for rot_y in bone_data.rot_z:
                                    bone.rotation_euler = [0.0, rot_y.value, 0.0]
                                    bone.keyframe_insert(data_path="rotation_euler", index=1, frame=rot_y.frame)
                                for rot_z in bone_data.rot_y:
                                    bone.rotation_euler = [0.0, 0.0, rot_z.value]
                                    bone.keyframe_insert(data_path="rotation_euler", index=2, frame=rot_z.frame)

                                break

        progress.leave_substeps("Done.")

        progress.leave_substeps("Finished importing: %r" % filepath)

    return {'FINISHED'}
