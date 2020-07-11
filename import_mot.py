# <pep8 compliant>

import bpy
from bpy_extras.wm_utils.progress_report import ProgressReport

from .modules.ShenmueDKPy.files.animation.motn import MOTN


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

        print(bpy.context.selected_bones)
        print(bpy.context.selected_objects[0])
        progress.enter_substeps(2, "Loading sequences to selected rig...")
        for sequence in motn.sequences:
            print(sequence.data.bone_keyframes)
            None
            # create a new cube
            #bpy.ops.mesh.primitive_cube_add()

            # newly created cube will be automatically selected
            #cube = bpy.context.selected_objects[0]

            # change name
            #cube.name = sequence.name

            # change its location
            #cube.location = (0.0, 0.0, 0.0)
        progress.leave_substeps("Done.")

        progress.leave_substeps("Finished importing: %r" % filepath)

    return {'FINISHED'}
