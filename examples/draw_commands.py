import bimpy
import numpy as np

ctx = bimpy.Context()

ctx.init(1200, 800, "Draw Commands Test")

with ctx:
        bimpy.themes.set_light_theme()

DATA_POINTS = bimpy.Int(30)
CLASTERS = bimpy.Int(4)

std = bimpy.Float(0.5)

colors = [0x4b19e6, 0x4bb43c, 0x19e1ff, 0xc88200, 0x3182f5, 0xb41e91, 0xf0f046, 0xf032e6, 0xd2f53c,
                  0xfabebe, 0x008080, 0xe6beff, 0xaa6e28, 0xfffac8, 0x800000, 0xaaffc3, 0x808000, 0xffd8b1,
                  0x000080, 0x808080, 0xFFFFFF, 0x000000]

datapoints = []


def generate_fake_data():
        datapoints.clear()
        for i in range(CLASTERS.value):
                x = np.random.normal(size=(DATA_POINTS.value, 2))
                alpha = np.random.rand()
                scale = std.value * np.random.rand(2) * np.eye(2, 2)
                position = np.random.rand(2) * 5
                rotation = np.array([[np.cos(alpha), np.sin(alpha)], [-np.sin(alpha), np.cos(alpha)]])
                x = np.matmul(x, scale)
                x = np.matmul(x, rotation)
                x += position
                datapoints.append((x, rotation, position, scale))


axis = x = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])


while not ctx.should_close():
        ctx.new_frame()

        bimpy.set_next_window_pos(bimpy.Vec2(20, 20), bimpy.Condition.Once)
        bimpy.set_next_window_size(bimpy.Vec2(800, 600), bimpy.Condition.Once)
        bimpy.begin("Drawings")

        window_pos = bimpy.get_window_pos()

        center = bimpy.Vec2(100, 100) + window_pos
        m = 100.0
        for i in range(len(datapoints)):
                (x, R, P, S) = datapoints[i]

                for j in range(x.shape[0]):
                        point = bimpy.Vec2(x[j, 0], x[j, 1])
                        bimpy.add_circle_filled(point * m + center, 5, 0xAF000000 + colors[i], 100)

                axis_ = np.matmul(axis, S * 2.0)
                axis_ = np.matmul(axis_, R) + P

                bimpy.add_line(
                        center + bimpy.Vec2(axis_[0, 0], axis_[0, 1]) * m,
                        center + bimpy.Vec2(axis_[1, 0], axis_[1, 1]) * m,
                        0xFFFF0000, 1)

                bimpy.add_line(
                        center + bimpy.Vec2(axis_[2, 0], axis_[2, 1]) * m,
                        center + bimpy.Vec2(axis_[3, 0], axis_[3, 1]) * m,
                        0xFFFF0000, 1)

        bimpy.end()

        bimpy.set_next_window_pos(bimpy.Vec2(20, 640), bimpy.Condition.Once)
        bimpy.set_next_window_size(bimpy.Vec2(800, 140), bimpy.Condition.Once)
        bimpy.begin("Controls")

        bimpy.input_int("Data points count", DATA_POINTS)
        bimpy.input_int("Clasters count", CLASTERS)

        bimpy.slider_float("std", std, 0.0, 3.0)

        if bimpy.button("Generate data"):
                generate_fake_data()

        bimpy.end()

        ctx.render()
