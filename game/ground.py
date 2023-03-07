from ursina import Entity


class Ground(Entity):
    def __init__(self):
        super(Ground, self).__init__(model='plane', texture='grass', collider='mesh', scale=(100,1,100))