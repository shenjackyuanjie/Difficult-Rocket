import time

import pyglet

window = pyglet.window.Window(resizable=True)

ball_image = pyglet.image.load('../textures/Atmospheres.png')  # 可自定义材质
batch = pyglet.graphics.Batch()

ball_sprites = []
start_t = time.time()
for i in range(100000):  # 可自定义数量
    x, y = i * 30, 50
    ball_sprites.append(pyglet.sprite.Sprite(ball_image, x, y, batch=batch))
    ball_sprites[i - 1].visible = True
end_t = time.time()
print(start_t, end_t, end_t - start_t)

a = 1


@window.event
def on_draw():
    start_t = time.time()
    batch.draw()
    end_t = time.time()
    print(start_t, end_t - start_t)
    print(end_t, pyglet.clock.get_fps(), 'fps')


pyglet.app.run()
