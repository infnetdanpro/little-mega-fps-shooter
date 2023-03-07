from ursina import Entity, Vec3, BoxCollider, color


class Wall(Entity):
    def __init__(self, position: Vec3):
        super(Wall, self).__init__(
            position=position,
            scale=2,
            model='cube',
            texture='grass',
            origin=-0.5
        )
        self.color = color.rgb(120, 120, 120)
        self.collider = BoxCollider(self, size=Vec3(1,2,1))


class Map:
    def __init__(self):
        for y in range(0, 4, 2):
            Wall(Vec3(6, y, 0))
            Wall(Vec3(6, y, 2))
            Wall(Vec3(6, y, 4))
            Wall(Vec3(6, y, 6))
            Wall(Vec3(6, y, 8))

            Wall(Vec3(4, y, 8))
            Wall(Vec3(2, y, 8))
            Wall(Vec3(0, y, 8))
            Wall(Vec3(-2, y, 8))