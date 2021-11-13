import numpy as np
import mathutils, bpy, os

def importBaseObj():
    bpy.ops.import_scene.obj(filepath=os.path.join(os.path.dirname(__file__), "head_model.obj"))
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    return bpy.context.active_object

def particleEditNotify():
    try:
        bpy.ops.particle.brush_edit(stroke=[{"name":"", "location":(0, 0, 0), "mouse":(0, 0), "mouse_event":(0, 0), "pressure":0, "size":0, "pen_flip":False, "x_tilt":0, "y_tilt":0, "time":0, "is_start":False}])
        # bpy.ops.particle.brush_edit(stroke=[{"name":"", "pressure":0, "size":0}])
    except RuntimeError:
        pass

def sub_v3_v3v3(a, b):
    return a - b

def sub_norm_v3_v3v3(key1, key2):
    rawVec = key1 - key2
    return rawVec / np.linalg.norm(rawVec)

def mul_v3_v3s1(a, b):#s1 means scalar
    return [a[0] * b, a[1] * b, a[2] * b]

### c implemented
# def mul_qt_qtqt(a, b):
#     # q = np.empty(4)
#     q = [0.,0.,0.,0.]

#     # t0 = a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]
#     # t1 = a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2]
#     # t2 = a[0] * b[2] + a[2] * b[0] + a[3] * b[1] - a[1] * b[3]
#     q[3] = a[0] * b[3] + a[3] * b[0] + a[1] * b[2] - a[2] * b[1]
#     q[0] = a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]#t0
#     q[1] = a[0] * b[1] + a[1] * b[0] + a[2] * b[3] - a[3] * b[2]#t1
#     q[2] = a[0] * b[2] + a[2] * b[0] + a[3] * b[1] - a[1] * b[3]#t2
#     return q

### c implemented
# def mul_v3_qtv3(q, r):
#     t0 = -q[1] * r[0] - q[2] * r[1] - q[3] * r[2]
#     # t1 = q[0] * r[0] + q[2] * r[2] - q[3] * r[1]
#     # t2 = q[0] * r[1] + q[3] * r[0] - q[1] * r[2]
#     r[2] = q[0] * r[2] + q[1] * r[1] - q[2] * r[0]
#     r[0] = q[0] * r[0] + q[2] * r[2] - q[3] * r[1] #t1
#     r[1] = q[0] * r[1] + q[3] * r[0] - q[1] * r[2] #t2

#     # t1 = t0 * -q[1] + r[0] * q[0] - r[1] * q[3] + r[2] * q[2]
#     # t2 = t0 * -q[2] + r[1] * q[0] - r[2] * q[1] + r[0] * q[3]
#     r[2] = t0 * -q[3] + r[2] * q[0] - r[0] * q[2] + r[1] * q[1]
#     r[0] = t0 * -q[1] + r[0] * q[0] - r[1] * q[3] + r[2] * q[2]# t1
#     r[1] = t0 * -q[2] + r[1] * q[0] - r[2] * q[1] + r[0] * q[3]#t2
#     return r

def norm_v3_v3(v):
    return v / np.linalg.norm(v)

def norm_s1_v3(v):
    return np.sqrt(np.dot(v,v))

### c implemented
# def axis_angle_to_quat(norm, angle):
#     phi = 0.5 * angle
#     si = np.sin(phi)
#     co = np.cos(phi)
#     # return 1
#     return [co, norm[0]*si, norm[1]*si, norm[2]*si]

def dot_fl_v3v3(a,b):
    d = np.dot(a,b)
    if d < -1:
        return -1
    elif d > 1:
        return 1
    return d

def add_v3_v3v3(a,b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

### not used
# def interp_v3_v3v3(a, b, t):
#     s = 1. - t
#     return [s * a[0] + t * b[0], s * a[1] + t * b[1], s * a[2] + t * b[2]]

def clamp(num, mi, ma):
   return max(min(num, ma), mi)