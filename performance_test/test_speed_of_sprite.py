import time

import pyglet

window = pyglet.window.Window(resizable=True)

ball_image = pyglet.image.load('/DR/textures/Atmospheres.png') # 可自定义材质
batch = pyglet.graphics.Batch()

ball_sprites = []
start_t = time.time()
for i in range(1500): # 可自定义数量
    x, y = i * 10, 50
    ball_sprites.append(pyglet.sprite.Sprite(ball_image, x, y, batch=batch))
end_t = time.time()
print(start_t, end_t, end_t-start_t)

a = 0
@window.event
def on_draw():
    start_t = time.time()
    if a:
        for x in ball_sprites:
            x.draw()
    else:
        batch.draw()
    end_t = time.time()
    print(start_t, end_t-start_t)
    print(end_t, pyglet.clock.get_fps(), 'fps')

pyglet.app.run()
