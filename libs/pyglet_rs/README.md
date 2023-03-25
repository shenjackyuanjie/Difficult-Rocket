# pyglet_rs

This is a folder about pyglet_rs.

## What is pyglet_rs?

pyglet_rs is a python library that patches pyglet to use rust to make it faster!

## Notice

**This Folder may be move to an individual repo. here is just a temp location**

## requirements
- python `3.8+`
- pyglet `2.0+`
- pyo3 `0.18.1`
- no more

## status
- still writing

## usage

```python
import pyglet_rs
pyglet_rs.patch_sprite()

import pyglet
...
```

## how to build

```powershell
cd src
./build.ps1
```

## roadmap

- [ ] `pyglet.sprite.Sprite` patch (doing)

- [ ] `pyglet.math.Vec2` patch
- [ ] `pyglet.math.Vec3` patch
- [ ] `pyglet.math.Vec4` patch
- [ ] `pyglet.math.Mat3(tuple)` patch
- [ ] `pyglet.math.Mat4(tuple)` patch

