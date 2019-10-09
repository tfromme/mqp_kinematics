#!/usr/bin/env python

from time import sleep, time
from math import sin, cos
from contextlib import suppress
from multiprocessing import Process, Value


ROTATIONAL_JOINT = 1
TWISTING_JOINT = 2


class Robot:

    def __init__(self):
        self.links = []

    class Link:

        def __init__(self, length_before, length_after, joint_type=ROTATIONAL_JOINT, attach_angle=0, start_angle=0):
            self.length_before = length_before
            self.length_after = length_after
            self.joint_type = joint_type
            self.attach_angle = attach_angle
            self._angle = Value('d', start_angle)
            self._angle_process = None

            if self.joint_type == ROTATIONAL_JOINT:
                c = cos(self.attach_angle)
                s = sin(self.attach_angle)

                self.start_to_joint = (
                    f'[[{c}, {-s}, 0, 0], '
                    f'[{s},  {c}, 0, 0], '
                    f'[0,  0, 1, {self.length_before}], '
                    '[0,  0, 0, 1]]')

                # c and s will get replaced in sympy
                self.joint_to_end = (
                    '[[1, 0, 0, 0], '
                    f'[0, c, -s, {-self.length_after}*s], '
                    f'[0, s, c, {self.length_after}*c], '
                    '[0, 0, 0, 1]]')

        @property
        def angle(self):
            return self._angle.value

        def _go_to_angle_process(self, angle):
            step_size = .1 if (angle > self._angle.value) else -.1
            while abs(self._angle.value - angle) >= .05:
                self._angle.value += step_size
                sleep(.00308641975)

        def go_to_angle(self, angle):
            with suppress(Exception):
                self._angle_process.terminate()
            self._angle_process = Process(target=self._go_to_angle_process, args=(angle,))
            self._angle_process.start()

        def get_transforms(self):
            return self.start_to_joint, self.joint_to_end

    def attach_link(self, *args, **kwargs):
        self.links.append(self.Link(*args, **kwargs))

    def status(self):
        while True:
            for i, link in enumerate(self.links):
                yield i + 1, link.angle

    def set_angle(self, link_number, angle):
        self.links[link_number - 1].go_to_angle(angle)

    def get_transforms(self):
        return [link.get_transforms for link in self.links]


if __name__ == '__main__':
    r = Robot()
    r.attach_link(10, 10)
    link = r.links[0]

    start = time()
    link.go_to_angle(90)
    while time() - start < .5:
        print(link.angle)
        sleep(.01)
    print('shift')
    link.go_to_angle(-30)
    while abs(link.angle + 30) > .1:
        print(link.angle)
        sleep(.01)
    print(time() - start)
