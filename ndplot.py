# Copyright Hugh Perkins 2016
# License: MPL


import pyglet
import math
import numpy as np
from pyglet.gl import *


try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config)
except pyglet.window.NoSuchConfigException:
    print('fall back to no multisampling')
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)


window.push_handlers(pyglet.window.event.WindowEventLogger())


# @window.event
# def on_key_press(symbol, modifiers):
#     print(symbol, modifiers)


# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     print(x, y, button, modifiers)


@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    print('drag, button=%s' % button)
    global rx, ry, rz
    global points
    global projection_basis

    R1 = np.identity(K)
    theta = dx * 3.1416 / 180

    # # rotates around axis into screen
    # R[0, 0] = math.cos(theta)
    # R[1, 1] = R[0, 0]
    # R[1, 0] = math.sin(theta)
    # R[0, 1] = - math.sin(theta)

    # rotates around vertical axis (vertical, coplanar with the screen surface)
    R1[0, 0] = math.cos(theta)
    R1[2, 2] = R1[0, 0]
    R1[2, 0] = math.sin(theta)
    R1[0, 2] = - R1[2, 0]

    phi = dy * 3.1416 / 180
    R2 = np.identity(K)
    # rotates around left-right axis (axis coplanar with screen surface)
    R2[1, 1] = math.cos(phi)
    R2[2, 2] = R2[0, 0]
    R2[2, 1] = math.sin(phi)
    R2[1, 2] = - R2[2, 1]

    # points = points.dot(R1)
    # points = points.dot(R2)
    projection_basis = projection_basis.dot(R1)
    projection_basis = projection_basis.dot(R2)
    # projection_basis, _ = np.linalg.qr(projection_basis)
    projection_basis /= np.linalg.norm(projection_basis)
    # print(projection_basis, np.linalg.norm(projection_basis))

    # ry += dx
    # rx += dy
    # # rz += dt * 30

    # rx %= 360
    # ry %= 360
    # rz %= 360

    # print(x, y, dx, dy, button, modifiers)

# @window.event
# def on_draw():
#     window.clear()
#     # image.blit(0, 0)
#     # label.draw()


@window.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


sphere = gluNewQuadric()


def nparray2_to_pygletmatrix(M):
    rows = M.shape[0]
    cols = M.shape[1]
    assert rows == cols
    # size = rows * cols
    a = (GLfloat * 16)(0 * 16)
    for row in range(M.shape[0]):
        for col in range(M.shape[1]):
            a[col * rows + row] = M[row, col]
    return a


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -4)
    glRotatef(rz, 0, 0, 1)
    glRotatef(rx, 1, 0, 0)
    glRotatef(ry, 0, 1, 0)
    # torus.draw()
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(1.0, 1.0, 1.0, 0))

    points_ = points.dot(projection_basis)
    for point in points_:
        glPushMatrix()
        glTranslatef(point[0], point[1], point[2])
        glScalef(0.01, 0.01, 0.01)
        # torus.draw()
        gluSphere(sphere, 1.0, 10, 10)
        glPopMatrix()
    # for point in squared:
    #     glPushMatrix()
    #     glTranslatef(point[0], point[1], point[2])
    #     glScalef(0.05, 0.05, 0.05)
    #     # torus.draw()
    #     gluSphere(sphere, 1.0, 10, 10)
    #     glPopMatrix()

    AXIS_THICKNESS = 0.03

    # glColor3f(1, 1, 0)
    # pyglet.gl.glLineWidth(10.5)
    # pyglet.graphics.draw(
    #     2, pyglet.gl.GL_LINES,
    #     ('v3f', (0.0, 0.0, 0.0, 1.0, 0.0, 0.0))
    # )

    # origin
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 1.0, 0.0, 0))
    glPushMatrix()
    glScalef(0.05, 0.05, 0.05)
    gluSphere(sphere, 1.0, 10, 10)
    glPopMatrix()

    for k in range(K):
        k_bin = format(k + 1, '03b')
        color = [0, 0, 0, 0]
        for i, b in enumerate(k_bin):
            if b == '1':
                color[i] = 1
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(*color))
        glPushMatrix()
        axis_v = np.zeros(K)
        axis_v[k] = 1
        axis_v = axis_v.dot(projection_basis)

        glTranslatef(axis_v[0], axis_v[1], axis_v[2])
        glScalef(0.05, 0.05, 0.05)
        gluSphere(sphere, 1.0, 10, 10)
        glPopMatrix()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0, 0.3, 1))


# Define a simple function to create ctypes arrays of floats:
def vec(*args):
    return (GLfloat * len(args))(*args)


def setup():
    glClearColor(0, 0, 0, 1)
    glColor3f(1, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glLightfv(GL_LIGHT0, GL_POSITION, vec(.5, .5, 1, 0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.1, .1, 0.1, 0.1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))
    glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .5, .5, 1))
    glLightfv(GL_LIGHT1, GL_SPECULAR, vec(0.1, 0.1, 0.1, 0.1))

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0, 0.3, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0)


setup()

N = 1000
K = 4
# points = np.random.randn(N, K) * 0.5
np.random.seed(123)
A = np.random.randn(K)
cov = A.T.dot(A) + 0.1 * np.identity(K)
points = np.random.multivariate_normal(
    mean=np.zeros(K),
    cov=cov,
    size=(N,)
)

squared_side = 5
squared = np.zeros((squared_side * squared_side, K))
for i in range(squared_side):
    for j in range(squared_side):
        squared[i * squared_side + j][0] = i / squared_side
        squared[i * squared_side + j][1] = j / squared_side
        squared[i * squared_side + j][2] = (i * i + j * j) / squared_side / squared_side

# projection_basis = np.random.randn(K, K)
projection_basis = np.identity(K)
# projection_basis[:3, :3] = np.identity(3)
projection_basis, _ = np.linalg.qr(projection_basis)
print(projection_basis)

rx = ry = rz = 0


pyglet.app.run()
