from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

width, height = 800, 600


def init_graphics():
    # OpenGL initialization (no need to call glutMainLoop here)
    glClearColor(0.1, 0.1, 0.1, 1.0)  # Set clear color for background
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    glEnable(GL_MULTISAMPLE)  # Enable anti-aliasing
    glShadeModel(GL_SMOOTH)  # Smooth shading
    gluPerspective(60, (width / height), 0.1, 50.0)  # Perspective view
    glTranslatef(0.0, 0.0, -6.0)  # Set initial view

    # Lighting setup
    glEnable(GL_LIGHTING)
    setup_lighting()

    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)


def setup_lighting():
    glEnable(GL_LIGHT0)
    # Position of the light
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 10.0, 0.0, 0.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])  # Diffuse light
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Specular light
    # Increased ambient light for a brighter scene
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0])

    # Additional light source for better 3D lighting effect
    glEnable(GL_LIGHT1)
    # Light coming from the top-right
    glLightfv(GL_LIGHT1, GL_POSITION, [10.0, 10.0, 10.0, 1.0])
    # Diffuse light for more even lighting
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.6, 0.6, 0.6, 1.0])
    # Specular light for reflections
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])


def draw_small_ball(position, radius):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 0.0, 0.0, 1.0])  # Red
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # White
    glMaterialf(GL_FRONT, GL_SHININESS, 50)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 128, 128)
    gluDeleteQuadric(quad)
    glPopMatrix()


def draw_glass_sphere(radius):
    glPushMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Glass material properties (transparent blue)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [
                 0.6, 0.8, 1.0, 0.5])  # Transparent blue
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [
                 0.8, 0.8, 0.8, 1.0])  # Reflective highlights
    # High shininess for glass effect
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 90)

    # Render the sphere with smooth shading and high segments
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 128, 128)
    gluDeleteQuadric(quad)

    glDisable(GL_BLEND)
    glPopMatrix()


def draw_selected_glass_sphere(radius):
    glPushMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Glass material properties for selected state (transparent green)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [
                 0.0, 1.0, 0.0, 0.7])  # Transparent green to indicate selection
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [
                 1.0, 1.0, 0.0, 1.0])  # Yellow highlights for selected effect
    # High shininess for more reflection
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 100)

    # Render the sphere with smooth shading and high segments
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 128, 128)
    gluDeleteQuadric(quad)

    glDisable(GL_BLEND)
    glPopMatrix()


def draw_grid(down_offset):
    glPushMatrix()
    glDisable(GL_LIGHTING)  # Disable lighting for the grid
    glColor3f(0.3, 0.3, 0.3)  # Soft gray
    grid_size = 30
    grid_step = 1
    glBegin(GL_LINES)
    for x in range(-grid_size, grid_size + 1, grid_step):
        glVertex3f(x, -down_offset, -grid_size)
        glVertex3f(x, -down_offset, grid_size)
    for z in range(-grid_size, grid_size + 1, grid_step):
        glVertex3f(-grid_size, -down_offset, z)
        glVertex3f(grid_size, -down_offset, z)
    glEnd()
    glEnable(GL_LIGHTING)  # Re-enable lighting after drawing the grid
    glPopMatrix()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw the grid and spheres
    draw_grid(0)

    # Draw the smaller ball
    draw_small_ball([0, 0, 0], 0.5)

    # Draw the glass sphere
    draw_glass_sphere(1.0)

    # Optionally, draw the selected glass sphere
    draw_selected_glass_sphere(1.0)

    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)
    gluPerspective(60, (width / height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -6.0)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow("3D Scene")
    init_graphics()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()


if __name__ == "__main__":
    main()
