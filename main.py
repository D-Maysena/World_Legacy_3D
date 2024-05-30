import pygame as pg
import moderngl as mgl
import numpy as np
import sys

class GraphicsEngine:
    def __init__(self, win_size=(800, 600)):
        pg.init()
        self.WIN_SIZE = win_size
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()
        self.clock = pg.time.Clock()

        self.vertices = np.array([
            [-0.5, -0.5],
            [ 0.5, -0.5],
            [ 0.0,  0.5],
        ], dtype='f4')

        self.vbo = self.ctx.buffer(self.vertices)

        self.prog = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_vert;
            void main() {
                gl_Position = vec4(in_vert, 0.0, 1.0);
            }
            """,
            fragment_shader="""
            #version 330
            out vec4 fragColor;
            void main() {
                fragColor = vec4(0.0, 0.0, 0.0, 1.0);
            }
            """,
        )

        self.vao = self.ctx.vertex_array(self.prog, [(self.vbo, '2f', 'in_vert')])

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def render(self):
        self.ctx.clear(0.08, 0.19, 0.18)
        self.vao.render(mgl.TRIANGLES)

    def run(self):
        while True:
            self.check_events()
            self.render()
            self.clock.tick(60)
            pg.display.flip()

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
