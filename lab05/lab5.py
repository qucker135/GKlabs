#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin, cos, pi, sqrt

viewer = [0.0, 0.0, 10.0]

zeta = 0.0
zi = 0.0

normals_mode = 0

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

light_ambient1 = [0.1, 0.0, 0.0, 1.0]
light_diffuse1 = [0.8, 0.0, 0.0, 1.0]
light_specular1 = [1.0, 1.0, 1.0, 1.0]
light_position1 = [0.0, 10.0, 0.0, 1.0]

att_constant1 = 1.0
att_linear1 = 0.05
att_quadratic1 = 0.001


def x(u,v):
    return ((((-90.0*u + 225.0)*u - 270.0)*u + 180.0)*u - 45.0)*u * cos(pi * v)

def y(u,v):
    return ((160.0*u - 320.0)*u + 160.0)*u*u - 5.0
    # alternatively: return 160.0*u*u*(u-1.0)*(u-1.0) - 5.0

def z(u,v):
    return ((((-90.0*u + 225.0)*u - 270.0)*u + 180.0)*u - 45.0)*u * sin(pi * v)

def x_u(u,v):
    return (-450.0 * u*u*u*u + 900.0*u*u*u - 810.0*u*u + 360.0 * u -45.0) * cos(pi*v)

def x_v(u,v):
    return pi * (90.0*u*u*u*u*u - 225.0*u*u*u*u + 270.0*u*u*u - 180.0*u*u + 45.0*u) * sin(pi * v)

def y_u(u,v):
    return 640.0*u*u*u - 960.0*u*u + 320.0*u

def y_v(u,v):
    return 0.0

def z_u(u,v):
    return (-450.0 * u*u*u*u + 900.0*u*u*u - 810.0*u*u + 360.0 * u -45.0) * sin(pi*v)

def z_v(u,v):
    return -pi * (90.0*u*u*u*u*u - 225.0*u*u*u*u + 270.0*u*u*u - 180.0*u*u + 45.0*u) * cos(pi * v)

def Normal(u,v):
    vec = [y_u(u,v) * z_v(u,v) - y_v(u,v) * z_u(u,v),
        z_u(u,v) * x_v(u,v) - x_u(u,v) * z_v(u,v),
	x_u(u,v) * y_v(u,v) - y_u(u,v) * x_v(u,v)
        ]
    vecLen = sqrt(vec[0]**2.0+vec[1]**2.0+vec[2]**2.0)
    if vecLen != 0.0:
        return [vec[0]/vecLen, vec[1]/vecLen, vec[2]/vecLen]
    else:
        return None

def vec_sum(v1,v2):
    return [v1[i]+v2[i] for i in range(len(v1))]

def vec_diff(v1,v2):
    return [v1[i]-v2[i] for i in range(len(v1))]

def draw_egg_triangles_strip(N):
    global normals_mode
    vertices = [[[x(u,v),y(u,v),z(u,v)] for j in range(N) for v in [j/(N-1)] ] for i in range(N) for u in [i/(N-1)]] 
    normals = [ [ Normal(u,v) for j in range(N) for v in [j/(N-1)] ] for i in range(N) for u in [i/(N-1)]]
    for i in range(N-1):
        glBegin(GL_TRIANGLE_STRIP)
        glColor3fv([0.0, 0.0, 1.0]) #colors[i][j])
        for j in range(N):
            #change to defined table
	    #n = Normal(i/(N-1),j/(N-1))
            n = normals[i][j]
            if n != None:
                if i<N/2:
                    glNormal(n[0],n[1],n[2])
                else:
                    glNormal(-n[0],-n[1],-n[2])
            elif i==0 or i == N-1:
                glNormal(0.0,-1.0,0.0)
            elif i == (N-1)//2:
                glNormal(0.0,1.0,0.0)
            glColor3fv([0.0, 0.0, 1.0]) #colors[i][j])
            glVertex3fv(vertices[i][j]) 
            

            n = normals[i+1][j]
            #n = Normal((i+1)/(N-1),j/(N-1))
            if n != None:
                if i+1<N/2:
                    glNormal(n[0],n[1],n[2])
                else:
                    glNormal(-n[0],-n[1],-n[2])
            glColor3fv([0.0, 0.0, 1.0]) #colors[(i+1)%N][j])
            glVertex3fv(vertices[(i+1)%N][j])
        glEnd()    


    if normals_mode == 1:
        glBegin(GL_LINES)
        glColor3f(0.0, 1.0, 0.0) #green
        for i in range(N):
            for j in range(N):
                if normals[i][j] != None:
                    glVertex3fv(vertices[i][j])
                    glVertex3fv(vec_sum(vertices[i][j],normals[i][j]) if i<N/2 else vec_diff(vertices[i][j],normals[i][j]))
        glEnd()



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

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant1)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear1)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic1)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta
    global phi
    global zeta
    global zi

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
        zi += delta_y * pix2angle
        print("zeta: {}".format(zeta))
        print("zi: {}".format(zeta))
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

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    #glLightfv(GL_LIGHT1, GL_POSITION, light_position)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant1)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear1)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic1)



    #centralna pilka
    
    glRotatef(zeta, 0.0, 1.0, 0.0)
    glRotatef(zi, 0.0, 0.0, 1.0)

    draw_egg_triangles_strip(21)
    #quadric = gluNewQuadric()
    #gluQuadricDrawStyle(quadric, GLU_FILL)
    #gluSphere(quadric, 3.0, 10, 10)
    #gluDeleteQuadric(quadric)

    glRotatef(-zi, 0.0, 0.0, 1.0)
    glRotatef(-zeta, 0.0, 1.0, 0.0)

    light_position = [
        radius * cos(theta * pi/180.0) * cos(phi * pi/180.0),
	radius * sin(phi * pi/180.0),
	radius * sin(theta * pi/180.0) * cos(phi * pi/180.0),
        1.0
	]

    light_position1 = [
        radius * sin(theta * pi/180.0) * cos(phi * pi/180.0),
        radius * cos(theta * pi/180.0) * cos(phi * pi/180.0),
        radius * sin(phi * pi/180.0),
        1.0
        ]
   

  
    

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    #zrodlo swiatla0 
    glTranslate(light_position[0], light_position[1], light_position[2]) 
    
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    glTranslate(-light_position[0], -light_position[1], -light_position[2]) 

    #zrodlo swiatla1 
    glTranslate(light_position1[0], light_position1[1], light_position1[2]) 
    
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    glTranslate(-light_position1[0], -light_position1[1], -light_position1[2]) 



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
    global normals_mode

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
    if key == GLFW_KEY_N and action == GLFW_PRESS:
        normals_mode = 1
    elif key == GLFW_KEY_N and action == GLFW_RELEASE:
        normals_mode = 0


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
