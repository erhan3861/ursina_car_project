from ursina import *
from ursina.shaders import lit_with_shadows_shader

Entity.default_shader = lit_with_shadows_shader

class Car(Entity):
    def __init__(self, position=(0,0,0), **kwargs):
        super().__init__(parent=scene)
        self.position = position
        self.selected = False # kendimize tanımlıyoruz
        self.collider = "box" # çarpışma özelliğini kutu yap
        self.move = False # yukaı veya aşağı oklara basarsak araba hareket edecek
        self.speed = 1

        for key, value in kwargs.items():
            setattr(self, key, value) # nesnenin özelliklerini ayarla

    def input(self, key):
        if 0 + held_keys["up arrow"] or held_keys["down arrow"]:
            car.move = True  
        else:
            car.move = False
        if key == "tab":
            car.speed += 5
        elif key == "a":
            car.speed -= 5


    def update(self):
        if car.selected:
            # tekerlek ileri veya geri dönmesi
            if self.name == "tyre" and car.move:
                self.rotation_x += (held_keys["down arrow"] - held_keys["up arrow"]) * 100
            # tekerlek sağa veya sola dönmesi
            if self in [tyre1, tyre2]: # ön tekerlekleri
                self.rotation_y += (held_keys["left arrow"] - held_keys["right arrow"]) * 3
                if self.rotation_y > 50: self.rotation_y = 50
                elif self.rotation_y < -50: self.rotation_y = -50

            # arabanın ileri, geri, sağa, sola hareketi
            if self.name == "car":
                if car.move:
                    self.rotation_y += tyre1.rotation_y / 10
                    if  -10 < tyre1.rotation_y < 10: # tekerlek düz durduğunda
                        self.rotation_y -= tyre1.rotation_y / 10
                if not car.intersects(ignore=(tyre,tyre1,tyre2,tyre3,tyre4,ground)).hit:
                    self.position += (held_keys["down arrow"] - held_keys["up arrow"]) * (self.forward * car.speed)
                else:
                    print_on_screen("ignore")

        if self.selected: # eğer self.secim == True ise
            self.x += (held_keys["7"] - held_keys["8"]) * 0.5
            self.y += (held_keys["6"] - held_keys["3"]) * 0.5
            self.z += (held_keys["4"] - held_keys["5"]) * 0.5

        

# ----------------- application ------
def input(key): # app için geçerli
    if key == "1": car.selected = True
    elif key == "2": car.selected = False
    elif key == "b": car_window.color = color.blue
    elif key == "c": car_window.color = color.rgba(27, 139, 180, 50) # red green blue alpha
    elif key == "r": car_window.color = color.red
    elif key == "l": car_window.color = color.black
    elif key == "g":
        car.selected = True
        if not gas_sound.playing:
            gas_sound.play()

        

app = Ursina(borderless = False)

gas_sound = Audio("assets/gas.wav", loop=False, autoplay=False)

Sky()

ground = Entity(model="plane", texture="asphalt", scale=300, collider="box", texture_scale=(10,10))

car = Car(model="car_test", scale=0.05, name="car", position=Vec3(0.010477, 0, 0.0529), unlit=True)

cube = Entity(model="cube", scale=10, position=(2,0,2), collider="box")

car_window = Car(model="car_window", parent=car, name="w", color=color.white) # parent olarak car ayarlamak
car_window.x += 2

tyre = Car(model="car_tyre", parent=car, name="tyre")
# ön tekerlekler
tyre1=duplicate(tyre, position=Vec3(91.2364, 33.597, -127.75), collider="box", parent=car, name="tyre")
tyre2=duplicate(tyre, position=Vec3(-79.542, 33.6717, -127.79), collider="box", parent=car, name="tyre")

# arka tekerlekler
tyre3=duplicate(tyre, position=Vec3(91.6467, 35.4102, 147.16), collider="box", parent=car, name="tyre")
tyre4=duplicate(tyre, position=Vec3(-79.542, 35.4102, 147.164), collider="box", parent=car, name="tyre")

# tekerleği gizle
tyre.visible = False

barrier = Car(model="barrier", name="br", position=Vec3(20, 1.70, 0.0529))

cone = Car(model="cone", name="cone", position=Vec3(40, 0, 10))

cam = EditorCamera(y=5, z=-20)

sun = DirectionalLight() # yönlendirilmiş ışık
sun.look_at((1, -1 , -1))

app.run()