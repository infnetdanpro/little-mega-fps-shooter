from ursina import Entity, Vec3, math, time, destroy

from game.enemy import Enemy


class Bullet(Entity):
    def __init__(self, position: Vec3, direction: float, x_direction: float, network, damage: int = 20, slave: bool = False):
        speed = 45
        dir_rad = math.radians(direction)
        x_dir_rad = math.radians(x_direction)

        self.velocity = Vec3(
            math.sin(dir_rad) * math.cos(x_dir_rad),
            math.sin(dir_rad),
            math.cos(dir_rad) * math.cos(x_dir_rad),
        ) * speed

        super(Bullet, self).__init__(
            position=position + self.velocity / speed,
            model='sphere',
            collider='box',
            scale=0.2
        )

        self.damage = damage
        self.direction = direction
        self.x_direction = x_direction
        self.slave = slave
        self.network = network

    def update(self):
        self.position += self.velocity * time.dt
        hit_info = self.intersects()

        if hit_info.hit:
            if not self.slave:
                for entity in hit_info.entities:
                    if not isinstance(entity, Enemy):
                        continue
                    self.network.send_health(entity)
            destroy(self)
