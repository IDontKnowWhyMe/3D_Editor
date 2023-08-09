from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer, Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Import constants and definitions
        from constants import cube_vertices, edges, grid_size

        self.cube_vertices = cube_vertices
        self.edges = edges

        self.camera_distance = 5.0
        self.rotation_x = 0
        self.rotation_y = 0
        self.last_x = 0
        self.last_y = 0

        self.grid_size = grid_size

        # Define cube faces
        self.faces = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (0, 3, 7, 4),
            (1, 2, 6, 5)
        ]

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(0.0, 0.0, -self.camera_distance)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        glEnable(GL_NORMALIZE)

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 100.0)

        # Draw grid
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)
        for i in range(-self.grid_size, self.grid_size + 1):
            glVertex3f(i, 0, -self.grid_size)
            glVertex3f(i, 0, self.grid_size)
            glVertex3f(-self.grid_size, 0, i)
            glVertex3f(self.grid_size, 0, i)
        glEnd()

        # Draw cube faces
        for face in self.faces:
            glBegin(GL_QUADS)
            for vertex in face:
                glVertex3fv(self.cube_vertices[vertex])
            glEnd()

        self.update()


    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_W:
            self.rotation_x += 5
        elif key == Qt.Key_S:
            self.rotation_x -= 5
        elif key == Qt.Key_A:
            self.rotation_y -= 5
        elif key == Qt.Key_D:
            self.rotation_y += 5

        self.update()

    def wheelEvent(self, event):
        num_degrees = event.angleDelta().y() / 8
        num_steps = num_degrees / 15  # Adjust speed of zoom

        self.camera_distance -= num_steps

        if self.camera_distance < 1.0:
            self.camera_distance = 1.0

        self.update()

    def mousePressEvent(self, event):
        self.last_x = event.x()
        self.last_y = event.y()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_x
        dy = event.y() - self.last_y

        self.rotation_y += dx * 0.5
        self.rotation_x += dy * 0.5

        self.last_x = event.x()
        self.last_y = event.y()

        self.update()
