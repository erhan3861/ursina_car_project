from ursina import *
from ursina.shaders import lit_with_shadows_shader

Entity.default_shader = lit_with_shadows_shader

class Car(Entity):
    def __init__(self, position=(0,0,0), **kwargs):
        super().__init__(parent=scene)
        self.position = position
        self.selected = False
        self.collider = "box"
        self.move = False
        self.speed = 20
        self.shift_key_held = False  

        for key, value in kwargs.items():
            setattr(self, key, value)

    def input(self, key):
        if 0 + held_keys["w"] or held_keys["s"]:
            car.move = True
            # if not drive_sound.playing:
            #     drive_sound.play()
        else:
            car.move = False
            # drive_sound.stop()

        if key == "shift":
            if not self.shift_key_held:
                self.speed = 40
                self.shift_key_held = True

        if key == "shift up":
            self.speed = 20
            self.shift_key_held = False

    def update(self):
        if car.selected:
            if self.name == "tyre" and car.move:
                self.rotation_x += (held_keys["w"] - held_keys["s"]) * 200

            if self in [tyre1, tyre2]:
                self.rotation_y += (held_keys["d"] - held_keys["a"]) * 3
                if self.rotation_y > 30:
                    self.rotation_y = 30
                elif self.rotation_y < -30:
                    self.rotation_y = -30

            if self.name == "car":
                if car.move:
                    self.rotation_y += tyre1.rotation_y / 10
                    if -10 < tyre1.rotation_y < 10:
                        self.rotation_y -= tyre1.rotation_y / 10
                self.position += (held_keys["s"] - held_keys["w"]) * (self.forward * car.speed)

# ----------------- application ------
def input(key): 
    if key == "e":
        car.selected = True
        # if not car_start_sound.playing:
        #     car_start_sound.play()  
    elif key == "r": car.selected = False
    elif key == "1": car_window.color = color.rgba(180, 180, 180, 50)
    elif key == "2": car_window.color = color.rgba(1, 1, 180, 50)
    elif key == "3": car_window.color = color.rgba(180, 1, 1, 50) # red green blue alpha
    elif key == "4": car_window.color = color.rgba(1, 180, 1, 50)
    elif key == 'q':
        rotate_camera()

def rotate_camera():
    cam.rotation_y += 180

app = Ursina(borderless=False)

# car_start_sound = Audio('car_start.wav', loop=False, autoplay=False)
# drive_sound = Audio('car_start.wav', loop=True, autoplay=False)

Sky()

ground = Entity(model="plane", texture="asphalt", scale=600, collider="box", texture_scale=(10,10))

car = Car(model="car_test", scale=0.05, name="car", position=Vec3(0.010477, 0, 0.0529), unlit=True)

car_window = Car(model="car_window", parent=car, name="w", color=color.rgba(180, 180, 180, 50)) # parent olarak car ayarlamak
car_window.x += 2

tyre = Car(model="car_tyre", parent=car, name="tyre")
# ön tekerlekler
tyre1 = duplicate(tyre, position=Vec3(91.2364, 33.597, -127.75), collider="box", parent=car)
tyre2 = duplicate(tyre, position=Vec3(-79.542, 33.6717, -127.79), collider="box", parent=car)

# arka tekerlekler
tyre3 = duplicate(tyre, position=Vec3(91.6467, 35.4102, 147.16), collider="box", parent=car)
tyre4 = duplicate(tyre, position=Vec3(-79.542, 35.4102, 147.164), collider="box", parent=car)

tyre.visible = False # tekerleği gizle

cam = EditorCamera(collider="box", rotation_y=180)
cam.y = 10
cam.z = 40

sun = DirectionalLight() # yönlendirilmiş ışık
sun.look_at((1, -1 , -1))

def update():
    if car.selected:
        cam.position = car.position + Vec3(0, 10, 40) # Kamerayı arabayı takip etmesi için güncelle

app.run()
