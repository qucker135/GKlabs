#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin, cos, pi

viewer = [0.0, 0.0, 10.0]

zeta = 0.0

theta = 0.0
phi = 0.0
radius = 10.0
pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

light_components = [light_ambient, light_diffuse, light_specular]
index = [0,0] #index[0] == 0 or 1 or 2; index[1] == 0 or 1 or 2 or 3

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

#light_ambient1 = [0.1, 0.0, 0.0, 1.0]
#light_diffuse1 = [0.8, 0.0, 0.0, 1.0]
#light_specular1 = [1.0, 1.0, 1.0, 1.0]
#light_position1 = [0.1, 0.1, 15.0, 0.5]
#
#att_constant1 = 1.0
#att_linear1 = 0.05
#att_quadratic1 = 0.001

def startup():
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

    #glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    #glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    #glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    #glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    #glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant1)
    #glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear1)
    #glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic1)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    #glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta
    global phi
    global zeta
    #global 

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle #* 0.05
        phi += delta_y * pix2angle #* 0.05
        print("phi: {}".format(phi))
        print("theta: {}".format(theta))

    if right_mouse_button_pressed:
        zeta += delta_x * pix2angle
        print("zeta: {}".format(zeta))
	#pass

    #if right_mouse_button_pressed:
    

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    #glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    #glEnable(GL_LIGHT0)

    glRotatef(zeta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    light_position = [
        radius * cos(theta * pi/180.0) * cos(phi * pi/180.0),
	radius * sin(phi * pi/180.0),
	radius * sin(theta * pi/180.0) * cos(phi * pi/180.0),
        1.0
	]
   
    glRotatef(-zeta, 0.0, 1.0, 0.0)

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    #zrodlo swiatla 
    glTranslate(light_position[0], light_position[1], light_position[2]) #TODO
    
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    glTranslate(-light_position[0], -light_position[1], -light_position[2]) #TODO

    #glTranslate



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
    global light_components
    global index

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_A and action == GLFW_PRESS:
        index[0] = 0
    if key == GLFW_KEY_D and action == GLFW_PRESS:
        index[0] = 1
    if key == GLFW_KEY_S and action == GLFW_PRESS:
        index[0] = 2
    if key == GLFW_KEY_0 and action == GLFW_PRESS:
        index[1] = 0
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        index[1] = 1
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        index[1] = 2
    #nie wiem, czy to nalezy zmieniac
    #if key == GLFW_KEY_3 and action == GLFW_PRESS:
    #    index[1] = 3
    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        light_components[index[0]][index[1]] += 0.1
        if light_components[index[0]][index[1]] > 1.0:
            light_components[index[0]][index[1]] = 1.0
        print("component[{}][{}]=={}".format(index[0],index[1],light_components[index[0]][index[1]]))
        print("Ambient: {}".format(light_components[0]))
        print("Diffuse: {}".format(light_components[1]))
        print("Specular: {}".format(light_components[2]))
    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        light_components[index[0]][index[1]] -= 0.1
        if light_components[index[0]][index[1]] < 0.0:
            light_components[index[0]][index[1]] = 0.0
        print("component[{}][{}]=={}".format(index[0],index[1],light_components[index[0]][index[1]]))
        print("Ambient: {}".format(light_components[0]))
        print("Diffuse: {}".format(light_components[1]))
        print("Specular: {}".format(light_components[2]))


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos




def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0
    


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
