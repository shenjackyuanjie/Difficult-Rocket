import pyglet

window = pyglet.window.Window(width=1000, height=1000)
# a_image = pyglet.image.load('textures/Runtime.png')
pyglet.resource.path = ['../textures']
pyglet.resource.reindex()
b_image = pyglet.resource.image('Runtime.png')
c_image = pyglet.resource.image('Editor/TrashCan.png')


@window.event
def on_draw():
    window.clear()
    b_image.blit(x=500, y=10)
    c_image.blit(x=500, y=600)


pyglet.app.run()
