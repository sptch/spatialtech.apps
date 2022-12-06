import bpy
import cv2 as cv
import numpy as np
from mathutils import Matrix, Vector
import datetime


def get_scene_info(self, context):
    print('test')
    try:
        clip = context.area.spaces.active.clip
        context.scene.pnp_clip_name = clip.name
    except:
        clip = bpy.data.movieclips[context.scene.pnp_clip_name]

    if not clip:
        self.report({'ERROR'}, 'Please load an image in the clip editor')
    size = clip.size

    clipcam = clip.tracking.camera
    # clip.tracking.camera.focal_length = 20
    focal = clipcam.focal_length_pixels
    optcent = clipcam.principal
    # take radial distortion parameters:
    k1, k2, k3 = 0, 0, 0
    # if clipcam.distortion_model == 'POLYNOMIAL':
    #     k1, k2, k3 = clipcam.k1, clipcam.k2, clipcam.k3
    # elif clipcam.distortion_model == 'BROWN':
    #     k1, k2, k3 = clipcam.brown_k1, clipcam.brown_k2, clipcam.brown_k3
    # else:
    #     k1, k2, k3 = 0.0, 0.0, 0.0
    #     self.report(
    #         {'WARNING'}, 'Current distortion model is not supported, use Polynomial instead.')

    # get current frame to retrieve marker locations
    frame = bpy.data.scenes[0].frame_current
    fr = bpy.data.scenes[0].frame_current - bpy.data.scenes[0].frame_start
    fr = 0

    # get list of tracks and retrieve marker positions at current frame
    points2d = []
    markers = []
    tracks = clip.tracking.tracks
    if not tracks:
        self.report({'ERROR'}, 'Please add markers for the 2D points')
        l2d = 0
    else:

        for track in sorted(tracks, key=lambda o: o.name):
            marker = track.markers.find_frame(frame, exact=True)
            if (marker) and (marker.mute == False):
                markers.append(track.name)
                point = [marker.co[0]*size[0], size[1]-marker.co[1]*size[1]]
                points2d.append(point)
        points2d = np.asarray(points2d, dtype='double')
        markers = np.array(markers)

# retrieve 3D points from scene objects
    points3d = []
    points = []
    col3d = context.scene.pnp_collection
    if col3d == None:
        self.report({'ERROR'}, 'Please specify a collection for the 3D points')
        l3d = 0
    else:
        for point in sorted(col3d.all_objects, key=lambda o: o.name):
            points3d.append(point.location)
            points.append(point.name)
        points3d = np.asarray(points3d, dtype='double')
        points = np.array(points)

    mp, m_ind, p_ind = np.intersect1d(markers, points, return_indices=True)

    points3d = points3d[p_ind]
    points2d = points2d[m_ind]
    print(points2d)

    # construct camera intrinsics
    camintr = np.array([[focal, 0, optcent[0]],
                        [0, focal, size[1]-optcent[1]],
                        [0, 0, 1]], dtype='double')

    # construct distortion vector, only k1,k2,k3 (polynomial or brown models)
    distcoef = np.array([k1, k2, 0, 0, k3])

    return self, context, clip, points3d, points2d, camintr, distcoef, size, frame


# solver function
def solve_pnp(self, context, clip, points3d, points2d, camintr, distcoef, size, frame):
    print('test')
    if len(points2d) < 4:
        self.report(
            {'ERROR'}, 'Not enough point pairs, use at least 4 markers to solve a camera pose.')
        return {'CANCELLED'}

    ret, rvec, tvec, error = cv.solvePnPGeneric(
        points3d, points2d, camintr, distcoef, flags=cv.SOLVEPNP_SQPNP)
    rmat, _ = cv.Rodrigues(rvec[0])
    context.scene.campnp_msg = (
        "Reprojection Error: %.2f" % error) if ret else "solvePnP failed!"

    # get R and T matrices
    # https://blender.stackexchange.com/questions/38009/3x4-camera-matrix-from-blender-camera
    R_world2cv = Matrix(rmat.tolist())
    T_world2cv = Vector(tvec[0])

    # blender camera to opencv camera coordinate conversion
    R_bcam2cv = Matrix(
        ((1, 0, 0),
         (0, -1, 0),
         (0, 0, -1)))

    # calculate transform in world coordinates
    R_cv2world = R_world2cv.transposed()
    rot = R_cv2world @ R_bcam2cv
    loc = -1 * R_cv2world @ T_world2cv

    test = clip.name
    print(test)
    # Create new camera or use existing
    # check if active object is a camera, if so, assume user wants to set it up, otherwise create a new camera
    # if context.active_object == None or context.active_object.type != 'CAMERA':  # add a new one
    #     bpy.ops.object.add(type='CAMERA')
    #     bpy.context.object.name = clip.name

    # get all camera wrapper objects names in the scene
    cam_names = [obj.name for obj in bpy.data.objects if obj.type == 'CAMERA']
    print(cam_names)

    if clip.name not in cam_names:
        bpy.ops.object.add(type='CAMERA')
        bpy.context.object.name = clip.name
        cam = context.object
        bg.frame_method = 'FIT'
        bg.display_depth = 'FRONT'
    else:
        cam = bpy.data.objects[clip.name]

    # Set camera intrinsics, extrinsics and background
    camd = cam.data
    camd.type = 'PERSP'
    camd.lens = clip.tracking.camera.focal_length
    camd.sensor_width = clip.tracking.camera.sensor_width
    camd.sensor_height = clip.tracking.camera.sensor_width*size[1]/size[0]
    render_size = [context.scene.render.pixel_aspect_x * context.scene.render.resolution_x,
                   context.scene.render.pixel_aspect_y * context.scene.render.resolution_y]
    camd.sensor_fit = 'HORIZONTAL' if render_size[0] / \
        render_size[1] <= size[0]/size[1] else 'VERTICAL'
    refsize = size[0] if render_size[0] / \
        render_size[1] <= size[0]/size[1] else size[1]
    camd.shift_x = (size[0]*0.5 - clip.tracking.camera.principal[0])/refsize
    camd.shift_y = (size[1]*0.5 - clip.tracking.camera.principal[1])/refsize

    camd.show_background_images = True
    if not camd.background_images:
        bg = camd.background_images.new()
    else:
        bg = camd.background_images[0]
    bg.source = 'MOVIE_CLIP'
    bg.clip = clip

    bg.clip_user.use_render_undistorted = True

    cam.matrix_world = Matrix.Translation(loc) @ rot.to_4x4()
    cam.keyframe_insert("location", frame=frame)
    cam.keyframe_insert("rotation_euler", frame=frame)
    cam.data.keyframe_insert("shift_x", frame=frame)
    cam.data.keyframe_insert("shift_y", frame=frame)
    cam.data.keyframe_insert("lens", frame=frame)
    cam.data.keyframe_insert("sensor_height", frame=frame)
    cam.data.keyframe_insert("sensor_fit", frame=frame)

    # set custom property object data created datetime to current datetime
    cam.data["position_created"] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")
    # set is_precise to true
    cam.data["is_precise"] = True

    # get object last modified datetime

    context.scene.camera = cam

    return {'FINISHED'}
