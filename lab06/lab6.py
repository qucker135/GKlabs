#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

from math import sin, cos, pi

textureNr = 1

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

hide_wall_up = 0
hide_wall_down = 0
hide_wall_right = 0
hide_wall_left = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

N = 21

def x(u,v):
    return ((((-90.0*u + 225.0)*u - 270.0)*u + 180.0)*u - 45.0)*u * cos(pi * v)

def y(u,v):
    return ((160.0*u - 320.0)*u + 160.0)*u*u - 5.0
    # alternatively: return 160.0*u*u*(u-1.0)*(u-1.0) - 5.0

def z(u,v):
    return ((((-90.0*u + 225.0)*u - 270.0)*u + 180.0)*u - 45.0)*u * sin(pi * v)

#image1 = Image.open("tekstura_tosia.tga")
#image2 = Image.open("tekstura_drugi_kot.tga")
image3 = Image.open("2k_mars.tga")
vertices = [[[x(u,v),y(u,v),z(u,v)] for i in range(N) for u in [i/(N-1)] ] for j in range(N) for v in [j/(N-1)]] #[TA LISTA]

def startup():
    global image3

    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image3.size[0], image3.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image3.tobytes("raw", "RGB", 0, -1)
    )


def shutdown():
    pass

def draw_egg_triangles(): #dlaczego tranpozycja wspolrzednych???
    glBegin(GL_TRIANGLES)
    for i in range(N-1):
        for j in range(N-1):
            if j >= (N-1)//2:
                #pierwszy trojkat
                #glColor3fv(colors[i][j])
                glTexCoord2f(i/(N-1), j/(N-1))
                glVertex3fv(vertices[i][j])
                #glColor3fv(colors[i+1][j])
                glTexCoord2f((i+1)/(N-1), j/(N-1))
                glVertex3fv(vertices[i+1][j])
                #glColor3fv(colors[i][j+1])
                glTexCoord2f(i/(N-1), (j+1)/(N-1))
                glVertex3fv(vertices[i][j+1])
                #drugi trojkat
                #glColor3fv(colors[i][j+1])
                glTexCoord2f(i/(N-1), (j+1)/(N-1))
                glVertex3fv(vertices[i][j+1])
	        #glColor3fv(colors[i+1][j])
                glTexCoord2f((i+1)/(N-1), j/(N-1))
                glVertex3fv(vertices[i+1][j])
	        #glColor3fv(colors[i+1][j+1])
                glTexCoord2f((i+1)/(N-1), (j+1)/(N-1))
                glVertex3fv(vertices[i+1][j+1])
            else:
                #pierwszy trojkat
                #glColor3fv(colors[i][j])
                glTexCoord2f(i/(N-1), j/(N-1))
                glVertex3fv(vertices[i][j])
                #glColor3fv(colors[i][j+1])
                glTexCoord2f(i/(N-1), (j+1)/(N-1))
                glVertex3fv(vertices[i][j+1])
                #glColor3fv(colors[i+1][j])
                glTexCoord2f((i+1)/(N-1), j/(N-1))
                glVertex3fv(vertices[i+1][j])
		#drugi trojkat
                #glColor3fv(colors[i+1][j])
                glTexCoord2f((i+1)/(N-1), j/(N-1))
                glVertex3fv(vertices[i+1][j])
	        #glColor3fv(colors[i][j+1])
                glTexCoord2f(i/(N-1), (j+1)/(N-1))
                glVertex3fv(vertices[i][j+1])
		#glColor3fv(colors[i+1][j+1])
                glTexCoord2f((i+1)/(N-1), (j+1)/(N-1))
                glVertex3fv(vertices[i+1][j+1])



    glEnd()





def render(time):
    global theta
    global image1
    global image2

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    #if textureNr==2:
    #    glTexImage2D(
    #        GL_TEXTURE_2D, 0, 3, image2.size[0], image2.size[1], 0,
    #        GL_RGB, GL_UNSIGNED_BYTE, image2.tobytes("raw", "RGB", 0, -1)
    #    )
    #else:
    #    glTexImage2D(
    #        GL_TEXTURE_2D, 0, 3, image1.size[0], image1.size[1], 0,
    #        GL_RGB, GL_UNSIGNED_BYTE, image1.tobytes("raw", "RGB", 0, -1)
    #    )

    draw_egg_triangles()

    #glBegin(GL_TRIANGLES)
    #glTexCoord2f(0.0, 0.0)
    #glVertex3f(-5.0, -5.0, 0.0)
    #glTexCoord2f(1.0, 0.0)
    #glVertex3f(5.0, -5.0, 0.0)
    #glTexCoord2f(1.0, 1.0)
    #glVertex3f(5.0, 5.0, 0.0)
    #
    #glTexCoord2f(1.0, 1.0)
    #glVertex3f(5.0, 5.0, 0.0)
    #glTexCoord2f(0.0, 1.0)
    #glVertex3f(-5.0, 5.0, 0.0)
    #glTexCoord2f(0.0, 0.0)
    #glVertex3f(-5.0, -5.0, 0.0)

   # 

   # if hide_wall_up==0:
   #     glTexCoord2f(0.0, 1.0)
   #     glVertex3f(5.0, 5.0, 0.0)
   #     glTexCoord2f(0.5, 0.5)
   #     glVertex3f(0.0, 0.0, -3.0)
   #     glTexCoord2f(1.0, 1.0)
   #     glVertex3f(-5.0, 5.0, 0.0)

   # if hide_wall_right==0:
   #     glTexCoord2f(1.0, 1.0)
   #     glVertex3f(-5.0, 5.0, 0.0)
   #     glTexCoord2f(0.5, 0.5)
   #     glVertex3f(0.0, 0.0, -3.0)
   #     glTexCoord2f(1.0, 0.0)
   #     glVertex3f(-5.0, -5.0, 0.0)

   # if hide_wall_down==0:
   #     glTexCoord2f(1.0, 0.0)
   #     glVertex3f(-5.0, -5.0, 0.0)
   #     glTexCoord2f(0.5, 0.5)
   #     glVertex3f(0.0, 0.0, -3.0)
   #     glTexCoord2f(0.0, 0.0)
   #     glVertex3f(5.0, -5.0, 0.0)

   # if hide_wall_left==0:
   #     glTexCoord2f(0.0, 0.0)
   #     glVertex3f(5.0, -5.0, 0.0)
   #     glTexCoord2f(0.5, 0.5)
   #     glVertex3f(0.0, 0.0, -3.0)
   #     glTexCoord2f(0.0, 1.0)
   #     glVertex3f(5.0, 5.0, 0.0)

    #glEnd()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global hide_wall_up
    global hide_wall_down
    global hide_wall_right
    global hide_wall_left
    global textureNr

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_H and action == GLFW_PRESS:
        hide_wall_left = 1
    if key == GLFW_KEY_H and action == GLFW_RELEASE:
        hide_wall_left = 0
    if key == GLFW_KEY_J and action == GLFW_PRESS:
        hide_wall_down = 1
    if key == GLFW_KEY_J and action == GLFW_RELEASE:
        hide_wall_down = 0
    if key == GLFW_KEY_K and action == GLFW_PRESS:
        hide_wall_up = 1
    if key == GLFW_KEY_K and action == GLFW_RELEASE:
        hide_wall_up = 0
    if key == GLFW_KEY_L and action == GLFW_PRESS:
        hide_wall_right = 1
    if key == GLFW_KEY_L and action == GLFW_RELEASE:
        hide_wall_right = 0
    
    if key == GLFW_KEY_T and action == GLFW_PRESS:
        textureNr = 3 - textureNr
        




def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
