from ursina import Vec3, color, Vec2, Entity, camera, Text
from ursina.prefabs.first_person_controller import FirstPersonController


class Player(FirstPersonController):
    def __init__(self, position: Vec3):
        super().__init__(position=position, model='cube', jump_height=2.5, jump_duration=0.4, origin_y=2, collider='box', speed=15)

        self.cursor.color = color.rgb(220, 0, 0)

        self.healthbar_pos = Vec2(0, 0.45)
        self.healthbar_size = Vec2(0.8, 0.04)
        self.healthbar_bg = Entity(
            parent=camera.ui,
            model='quad',
            color=color.rgb(0, 255, 0),
            position=self.healthbar_pos,
            scale=self.healthbar_size
        )
        self.health = 100
        self.death_message_shown = False

    def update(self):
        if self.health < 1:
            self.death()
        else:
            super().update()

    def death(self):
        self.death_message_shown = True

        self.rotation = 0
        self.camera_pivot.world_rotation_x = -45
        self.world_position = Vec3(0, 7, -35)
        self.cursor.color = color.rgb(0,0,0,a=0)

        Text(
            text="Potracheno",
            origin=Vec2(0,0),
            scale=3
        )