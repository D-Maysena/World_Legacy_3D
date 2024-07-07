class Collisions:
    def __init__(self, app, models):
        self.app = app
        self.models = models

    def check_limits(self):
        for model in self.models:
            position, size = model['position'], model['size']
            limits = (size[0] / 2, size[1] / 2)
            bool_x = position[0] - limits[0] < self.app.x < position[0] + limits[0]
            bool_z = position[1] - limits[1] < self.app.z < position[1] + limits[1]

            if bool_x and bool_z:
                return False
        return True
