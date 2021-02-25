import math

degrees = 45  # clock wise +
position = [1, 1]
i_head = [1, 0]
j_head = [0, 1]

radians = degrees * (math.pi / 180)
cos = math.cos(radians)
sin = math.sin(radians)

rotated_pos = (position[0] * cos - position[1] * sin, position[0] * sin + position[1] * cos)
print(radians, cos, sin)
print(rotated_pos)
