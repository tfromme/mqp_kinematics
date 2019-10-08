#!/usr/bin/env python
from collections import UserList
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa  # Ignore complaints about Axes3D not being used


class Plot3D:

    def __init__(self, *, xlim=(-100, 400), ylim=(-400, 400), zlim=(-50, 500)):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(*xlim)
        self.ax.set_ylim(*ylim)
        self.ax.set_zlim(*zlim)

        plt.show(block=False)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

        self.plots = custom_list()
        self.get_next_color = self._next_color()

    def update(self, *args):
        """Updates the plot with given points.

        Plot is redrawn with line plots updated to go through given points.
        (Assume base starts at (0,0,0)

        Args:
            End point of each section
        """
        self.fig.canvas.restore_region(self.background)
        points = [(0, 0, 0), *args]
        for i in range(1, len(points)):
            plot = self.plots.setdefault(self, i - 1)  # Because of the extra (0,0,0) the index is off
            current_point = points[i]
            prior_point = points[i - 1]
            plot.set_xdata([prior_point[0], current_point[0]])
            plot.set_ydata([prior_point[1], current_point[1]])
            plot.set_3d_properties([prior_point[2], current_point[2]])

        for i, plot in enumerate(self.plots):
            if i < len(args):
                self.ax.draw_artist(plot)

        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

    def _next_color(self):
        while True:
            yield 'ro-'
            yield 'ro-'
            yield 'go-'
            yield 'go-'
            yield 'bo-'
            yield 'bo-'

    def close(self):
        plt.close(self.fig)


class custom_list(UserList):

    def get(self, index, default=None):
        try:
            return self.data[index]
        except IndexError:
            return default

    def setdefault(self, parent, index):
        try:
            return self.data[index]
        except IndexError:
            default = parent.ax.plot([0, 1], [0, 1], [0, 1], next(parent.get_next_color))[0]
            self.data.append(default)
            return default


if __name__ == '__main__':
    from time import sleep
    plot3d = Plot3D()
    points = [
        [(50, 50, 50), (50, 50, 150), (50, 50, 250), (150, 50, 250), (250, 50, 250), (250, 150, 250)],
        [(50, 50, 50), (50, 50, 150), (50, 50, 250), (150, 50, 250)],
        [(50, 50, 50), (50, 50, 150), (50, 50, 250), (150, 50, 250), (250, 50, 250), (250, 150, 250)],
    ]

    for point in points:
        plot3d.update(*point)
        sleep(5)
