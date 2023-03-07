from ursina import Entity, Vec3, color, Text, Vec2, destroy


class Enemy(Entity):
    def __init__(self, position: Vec3, identifier: str, username: str):
        super(Enemy, self).__init__(
            position=position,
            model='cube',
            origin_y=-0.5,
            collider="box",
            texture="white_cube",
            color=color.color(0, 0, 1),
            scale=Vec3(1,2,1)
        )
        self.name_tag = Text(
            parent=self,
            text=username,
            position=Vec3(0, 1.3, 0),
            billboard=True,
            origin=Vec2(0, 0),
        )

        self.health = 100
        self.id = identifier
        self.username = username

    def update(self):
        try:
            color_saturation = 1 - self.health / 100
        except AttributeError:
            self.health = 100
            color_saturation = 1 - self.health / 100

        self.color = color.color(0, color_saturation, 1)
        if self.health <= 0:
            destroy(self)
